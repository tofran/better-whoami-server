import os

from litestar import Litestar, Router
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec.external_documentation import ExternalDocumentation

from better_whoami.routes.connectivity import check_connectivity
from better_whoami.routes.environment_variables import environment_variables
from better_whoami.routes.healthz import healthz
from better_whoami.routes.system_info import system_info
from better_whoami.routes.user_info import user_info
from better_whoami.routes.whoami import whoami

APP_VERSION = os.getenv("APP_VERSION", "0.0.1-untagged")

app = Litestar(
    debug=False,
    openapi_config=OpenAPIConfig(
        title="Better Whoami server",
        description="An HTTP service that returns information about the system it is running on and incoming requests",
        version=APP_VERSION,
        external_docs=ExternalDocumentation(
            url="https://github.com/tofran/better-whoami-server",
            description="Source code",
        ),
        path="/",
    ),
    route_handlers=[
        Router(
            path="/",
            tags=["Whoami"],
            route_handlers=[
                whoami,
                check_connectivity,
                environment_variables,
                user_info,
                system_info,
            ],
        ),
        healthz,
    ],
)
