from dataclasses import dataclass
from typing import Any, Literal, Optional

from aiohttp import ClientSession


@dataclass
class Response:
    status: int
    body: Any


class Request:
    async def request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        return_method: Literal["json", "text", "read"],
        **kwargs: Any
    ):
        async with ClientSession() as client_session:
            async with client_session.request(method, url, **kwargs) as response:
                return Response(
                    response.status, await getattr(response, return_method)()
                )

    async def get(
        self, url: str, return_method: Literal["json", "text", "read"], **kwargs: Any
    ):
        return await self.request("GET", url, return_method, **kwargs)

    async def post(
        self, url: str, return_method: Literal["json", "text", "read"], **kwargs: Any
    ):
        return await self.request("POST", url, return_method, **kwargs)
