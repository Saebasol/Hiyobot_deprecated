import time

import aiohttp
import discord


class HiyobiTagsModel:
    def __init__(self, artists, characters, groups, _id, parodys, tags, title):
        self.artists = artists
        self.characters = characters
        self.groups = groups
        self.id = _id
        self.parodys = parodys
        self.tags = tags
        self.title = title

    @classmethod
    def generator_hiyobi_info(cls, list_: list):
        for info in list_:
            yield cls(
                info["artists"],
                info["characters"],
                info["groups"],
                info["id"],
                info["parodys"],
                info["tags"],
                info["title"],
            )


class HiyobiRequester:
    @staticmethod
    async def request(method, endpoint, json=None):
        url = "https://api.hiyobi.me" + endpoint
        async with aiohttp.ClientSession() as cs:
            async with cs.request(method, url, json=json) as r:
                if r.status == 404:
                    return None
                response = await r.json(content_type=None)
            return response

    async def get_list(self, num):
        response = await self.request("GET", f"/list/{num}")
        return response

    async def get_info(self, index) -> HiyobiTagsModel:
        response = await self.request("GET", f"/gallery/{index}")
        return HiyobiTagsModel(
            response["artists"],
            response["characters"],
            response["groups"],
            response["id"],
            response["parodys"],
            response["tags"],
            response["title"],
        )

    async def post_search(self, data):
        response = await self.request("POST", "/search", {"search": data})
        return response


class HiyobiExt(HiyobiRequester):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def parse_value_url(value_url_list: list):
        if not value_url_list:
            return ["없음"]
        else:
            return [f"{value_url_dict['display']}" for value_url_dict in value_url_list]

    def make_embed_with_info(self, info: HiyobiTagsModel):
        tags_join = ",".join(self.parse_value_url(info.tags))
        embed = discord.Embed(
            title=info.title,
            description=info.id,
            url=f"https://hiyobi.me/reader/{info.id}",
        )
        embed.set_thumbnail(url=f"https://cdn.hiyobi.me/tn/{info.id}.jpg")
        embed.add_field(
            name="작가", value=",".join(self.parse_value_url(info.artists)), inline=False
        )
        embed.add_field(
            name="그룹", value=",".join(self.parse_value_url(info.groups)), inline=False
        )
        embed.add_field(
            name="원작", value=",".join(self.parse_value_url(info.parodys)), inline=False
        )
        embed.add_field(
            name="캐릭터",
            value=",".join(self.parse_value_url(info.characters)),
            inline=False,
        )
        embed.add_field(
            name="태그",
            value=tags_join if len(tags_join) <= 1024 else "표시하기에는 너무 길어요.",
            inline=False,
        )
        return embed

    # FIXME: Need handle
    async def info_embed(self, index: int):
        info = await self.get_info(index)
        return self.make_embed_with_info(info)

    async def list_embed(self, number: int):
        lists = await self.get_list(number)
        if lists["count"] == 0:
            return
        return [
            self.make_embed_with_info(model)
            for model in HiyobiTagsModel.generator_hiyobi_info(lists["list"])
        ]

    async def search_embed(self, search_keyword: list):
        lists = await self.post_search(search_keyword)
        if lists["count"] == 0:
            return
        return [
            self.make_embed_with_info(model)
            for model in HiyobiTagsModel.generator_hiyobi_info(lists["list"])
        ]

    async def latency(self):
        hiyobi_latency1 = time.perf_counter()
        await self.request("GET", "/")
        hiyobi_latency2 = time.perf_counter()
        return hiyobi_latency2 - hiyobi_latency1
