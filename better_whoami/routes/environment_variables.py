import os

from litestar import get
from litestar.response import Response


@get(
    "/envs",
    name="environment_variables",
    description="Get the server environment variables.",
)
async def environment_variables() -> dict[str, str] | Response:
    if os.getenv("EXPOSE_ENV_VARS", "false").lower() == "true":
        return dict(os.environ)

    return Response(
        content="Set EXPOSE_ENV_VARS=true to expose the environment variables.",
        status_code=400,
    )
