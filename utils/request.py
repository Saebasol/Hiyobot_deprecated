from dataclasses import dataclass
from typing import Any, Literal, Optional

from aiohttp import ClientSession


@dataclass
class Response:
    status: int
    body: Any


class Request:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None

    async def request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        return_method: Literal["json", "text", "read"],
        **kwargs: Any
    ):
        if not self.session:
            self.session = ClientSession()

        response = await self.session.request(method, url, **kwargs)
        return Response(response.status, await getattr(response, return_method)())

    async def get(
        self, url: str, return_method: Literal["json", "text", "read"], **kwargs: Any
    ):
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self, url: str, return_method: Literal["json", "text", "read"], **kwargs: Any
    ):
        return await self.request("POST", url, return_method, **kwargs)
