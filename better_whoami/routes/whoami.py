from dataclasses import dataclass

from litestar import Request, get


@dataclass
class WhoamiResponse:
    connecting_ip: str
    socket_connecting_port: int | None
    url: str
    headers: dict[str, str]


@get(
    "/whoami",
    name="whoami",
    description=(
        "Get information about the incoming request. "
        "Returns only information which the client cannot know for certain. "
        "For example, headers being modified by proxies or load balancers."
    ),
)
async def whoami(request: Request) -> WhoamiResponse:
    return WhoamiResponse(
        connecting_ip=request.client.host if request.client else "unknown",
        socket_connecting_port=request.client.port if request.client else None,
        url=str(request.url),
        headers=dict(request.headers.items()),
    )
