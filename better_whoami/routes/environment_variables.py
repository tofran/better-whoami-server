import os

from litestar import get


@get(
    "/envs",
    name="environment_variables",
    description="Get the server environment variables.",
)
async def environment_variables() -> dict[str, str]:
    return dict(os.environ)
