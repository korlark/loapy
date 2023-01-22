from asyncio import Future, create_task, sleep
from collections import deque
from time import time
from typing import ClassVar, Literal, Optional

from aiohttp import ClientResponse, ClientSession
from typing_extensions import Self

from . import __version__
from .errors import (
    BadGateway,
    Forbidden,
    GatewayTimeout,
    InternalServerError,
    LostArkError,
    NotFound,
    ServiceUnavailable,
    Unauthorized,
)


class RateLimit:
    def __init__(self) -> None:
        self.limit: int = 1
        self.remaining: int = 1
        self.reset_at: Optional[int] = None

        self.loaded: bool = False
        self.pending: int = 0

        self.__queue: deque[Future] = deque()
        self.__waiting: Optional[Future] = None

    @property
    def expired(self) -> bool:
        return self.reset_at is not None and self.reset_at <= time()

    def update(self, response: ClientResponse) -> None:
        if "X-RateLimit-Limit" in response.headers:
            self.limit = int(response.headers["X-RateLimit-Limit"])

        if "X-RateLimit-Remaining" in response.headers:
            remaining = int(response.headers["X-RateLimit-Remaining"])

            if self.loaded:
                self.remaining = min(remaining, self.limit - self.pending)
            else:
                self.remaining = int(response.headers["X-RateLimit-Remaining"])
                self.loaded = True

        if "X-RateLimit-Reset" in response.headers:
            self.reset_at = int(response.headers["X-RateLimit-Reset"])

        if response.status == 429:
            self.remaining = 0
            self.reset_at = int(time()) + int(response.headers["Retry-After"])

    def reset(self) -> None:
        self.remaining = self.limit - self.pending
        self.reset_at = None
        self.loaded = False

    def __run(self, length: int = 1) -> None:
        x = 0
        while self.__queue:
            item = self.__queue.popleft()
            if not item.done():
                item.set_result(None)
                x += 1

            if x >= length:
                break

    async def __aenter__(self) -> Self:
        if self.expired:
            self.reset()

        while self.remaining <= 0:
            future = Future()
            self.__queue.append(future)
            await future

        self.remaining -= 1
        self.pending += 1

        return self

    async def __cleaner(self) -> None:
        if self.reset_at is None:
            return

        # Compensates for unknown error between X-RateLimit-Reset and actual reset time
        await sleep(self.reset_at - time() + 1)

        self.reset()
        self.__run(self.remaining)

    async def __aexit__(self, *_) -> None:
        self.pending -= 1

        if not self.__waiting or self.__waiting.done():
            if self.remaining <= self.pending:
                self.__waiting = create_task(self.__cleaner())
            else:
                self.__run(self.remaining - self.pending)


class LostArk:
    BASE: ClassVar[str] = "https://developer-lostark.game.onstove.com"

    def __init__(self, token: str) -> None:
        self.token = token

        self.__session: Optional[ClientSession] = None
        self.__ratelimit: RateLimit = RateLimit()

    def __create_session(self) -> ClientSession:
        return ClientSession(self.BASE)

    async def request(self, method: Literal["GET", "POST"], endpoint: str):
        if self.__session is None:
            self.__session = self.__create_session()

        async with self.__ratelimit:
            async with self.__session.request(
                method,
                endpoint,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}",
                    "User-Agent": f"Loapy (https://github.com/korlark/loapy) {__version__}",
                },
            ) as response:
                self.__ratelimit.update(response)

                if response.status == 200:
                    return await response.json(content_type=None)

                elif response.status == 401:
                    raise Unauthorized()
                elif response.status == 403:
                    raise Forbidden()
                elif response.status == 404:
                    raise NotFound()
                elif response.status == 500:
                    raise InternalServerError()
                elif response.status == 502:
                    raise BadGateway()
                elif response.status == 503:
                    raise ServiceUnavailable()
                elif response.status == 504:
                    raise GatewayTimeout()
                else:
                    raise LostArkError(f"Unexpected status code: {response.status}")
