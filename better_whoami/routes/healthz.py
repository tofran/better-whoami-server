from typing import Literal

from litestar import get


@get(
    "/healthz",
    name="healthz",
    description="Always returns OK, use this to check for service availability/readiness.",
    tags=["Health"],
    response_model=Literal["OK"],
)
async def healthz() -> str:
    return "OK"
