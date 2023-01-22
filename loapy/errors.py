class LostArkError(Exception):
    """Base class for all exceptions from Lostark Open API."""

    pass


class Unauthorized(LostArkError):
    """Raised when the API returns a 401 Unauthorized response."""

    pass


class Forbidden(LostArkError):
    """Raised when the API returns a 403 Forbidden response."""

    pass


class NotFound(LostArkError):
    """Raised when the API returns a 404 Not Found response."""

    pass


class InternalServerError(LostArkError):
    """Raised when the API returns a 500 Internal Server Error response."""

    pass


class BadGateway(LostArkError):
    """Raised when the API returns a 502 Bad Gateway response."""

    pass


class ServiceUnavailable(LostArkError):
    """Raised when the API returns a 503 Service Unavailable response."""

    pass


class GatewayTimeout(LostArkError):
    """Raised when the API returns a 504 Gateway Timeout response."""

    pass
