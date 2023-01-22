from asyncio import Future, create_task, sleep
from collections import deque
from logging import getLogger
from time import time
from typing import Any, ClassVar, List, Literal, Mapping, Optional

import ujson
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
from .types.armories import (
    ArmoryAvatar,
    ArmoryCard,
    ArmoryEngraving,
    ArmoryEquipment,
    ArmoryGem,
    ArmoryProfile,
    ArmorySkill,
    Collectible,
    ColosseumInfo,
)
from .types.auctions import Auction, AuctionOption, RequestAuctionItems
from .types.characters import CharacterInfo
from .types.guilds import GuildRanking
from .types.markets import MarketItem, MarketList, MarketOption, RequestMarketItems
from .types.news import Event

logger = getLogger("loapy.http")


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

            logger.info(
                "Unexpected rate limit exceeded, remaining capacity initialized"
            )

        elif self.remaining == 0:
            logger.info(
                "Expected to exceed rate limit, Preemptive rate limiting started."
            )

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


class LostArkRest:
    BASE: ClassVar[str] = "https://developer-lostark.game.onstove.com"

    __slots__ = ("token", "__session", "__ratelimit")

    def __init__(self, token: str) -> None:
        self.token = token

        self.__session: Optional[ClientSession] = None
        self.__ratelimit: RateLimit = RateLimit()

    def __create_session(self) -> ClientSession:
        return ClientSession(self.BASE)

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        *,
        json: Any = None,
        params: Optional[Mapping[str, str]] = None,
    ):
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
                data=None if json is not None else ujson.dumps(json),
                params=params,
            ) as response:
                logger.debug(f"{method} {endpoint} returned {response.status}")

                self.__ratelimit.update(response)

                if response.status == 200:
                    body = await response.text()

                    return ujson.loads(body)

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

    # https://developer-lostark.game.onstove.com/getting-started#API-NEWS

    async def fetch_events(self) -> List[Event]:
        """Returns a list of events on progress."""

        return await self.request("GET", "/News/Event")

    # https://developer-lostark.game.onstove.com/getting-started#API-CHARACTERS

    async def fetch_characters(self, character_name: str) -> List[CharacterInfo]:
        """Returns all character profiles for an account."""

        return await self.request("GET", f"/characters/{character_name}/siblings")

    # https://developer-lostark.game.onstove.com/getting-started#API-ARMORIES

    async def fetch_profile(self, character_name: str) -> ArmoryProfile:
        """Returns a summary of the basic stats by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/profiles"
        )

    async def fetch_equipment(self, character_name: str) -> List[ArmoryEquipment]:
        """Returns a summary of the items equipped by a character name."""
        return await self.request(
            "GET", f"/armories/characters/{character_name}/equipment"
        )

    async def fetch_avatars(self, character_name: str) -> List[ArmoryAvatar]:
        """Returns a summary of the avatars equipped by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/avatars"
        )

    async def fetch_combat_skills(self, character_name: str) -> List[ArmorySkill]:
        """Returns a summary of the combat skills by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/combat-skills"
        )

    async def fetch_engravings(self, character_name: str) -> ArmoryEngraving:
        """Returns a summary of the engravings equipped by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/engravings"
        )

    async def fetch_cards(self, character_name: str) -> ArmoryCard:
        """Returns a summary of the cards equipped by a character name."""

        return await self.request("GET", f"/armories/characters/{character_name}/cards")

    async def fetch_gems(self, character_name: str) -> ArmoryGem:
        """Returns a summary of the gems equipped by a character name."""

        return await self.request("GET", f"/armories/characters/{character_name}/gems")

    async def fetch_colosseums(self, character_name: str) -> ColosseumInfo:
        """Returns a summary of the proving grounds by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/colosseums"
        )

    async def fetch_collectibles(self, character_name: str) -> List[Collectible]:
        """Returns a summary of the collectibles by a character name."""

        return await self.request(
            "GET", f"/armories/characters/{character_name}/collectibles"
        )

    # https://developer-lostark.game.onstove.com/getting-started#API-AUCTIONS

    async def fetch_auction_options(self) -> AuctionOption:
        """Returns search options for the auction house."""

        return await self.request("GET", "/auctions/options")

    async def fetch_auction_items(
        self, request_auction_items: RequestAuctionItems
    ) -> Auction:
        """Returns all active auctions with search options."""

        return await self.request(
            "POST",
            "/auctions/items",
            json={"requestAuctionItems": request_auction_items},
        )

    # https://developer-lostark.game.onstove.com/getting-started#API-GUILDS

    async def fetch_guilds(
        self,
        server_name: Literal["루페온", "실리안", "아만", "카마인", "카제로스", "아브렐슈드", "카단", "니나브"],
    ) -> List[GuildRanking]:
        """Returns a list of guild rankings by a server."""

        return await self.request(
            "GET", f"/guilds/rankings", params={"serverName": server_name}
        )

    # https://developer-lostark.game.onstove.com/getting-started#API-MARKETS

    async def fetch_market_options(self) -> MarketOption:
        """Returns search options for the market."""

        return await self.request("GET", "/markets/options")

    async def fetch_market_item(self, item_id: int) -> List[MarketItem]:
        """Returns a market item by ID."""

        return await self.request("GET", f"/markets/items/{item_id}")

    async def fetch_market_items(
        self, request_market_items: RequestMarketItems
    ) -> List[MarketList]:
        """Returns a list of market items by search options."""

        return await self.request(
            "POST", "/markets/items", json={"requestMarketItems": request_market_items}
        )
