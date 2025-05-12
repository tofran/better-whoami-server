import grp
import os
import pwd
from dataclasses import dataclass

from litestar import get


@dataclass
class UserInfo:
    username: str
    group: str
    uid: int
    gid: int


@get(
    "/user_info",
    name="user_info",
    description="Get user information",
)
async def user_info() -> UserInfo:
    try:
        uid = os.geteuid()
        gid = os.getegid()
        username = pwd.getpwuid(uid).pw_name
        groupname = grp.getgrgid(gid).gr_name
        return UserInfo(
            username=username,
            uid=uid,
            gid=gid,
            group=groupname,
        )

    except (OSError, KeyError):
        return UserInfo(
            username="unknown",
            uid=os.geteuid(),
            gid=os.getegid(),
            group="unknown",
        )
