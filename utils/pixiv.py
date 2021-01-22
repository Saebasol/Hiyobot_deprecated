import asyncio
import datetime
import re
import time

import aiohttp
import discord


class PixivModel:
    def __init__(self, bookmark, comment, _id, like, title, username, uploadDate, view):
        self.bookmark = bookmark
        self.comment = comment
        self.id = _id
        self.like = like
        self.title = title
        self.username = username
        self.uploadDate = uploadDate
        self.view = view


class PixivRankingModel:
    def __init__(self, _id, rank, title, url, username):
        self.id = _id
        self.rank = rank
        self.title = title
        self.url = url
        self.username = username

    @classmethod
    def generator_pixiv_ranking_info(cls, list_: list):
        for info in list_:
            yield cls(
                info["illust_id"],
                info["rank"],
                info["title"],
                info["url"],
                info["user_name"],
            )


class PixivRequester:
    @staticmethod
    async def request(method, endpoint, **kwargs):
        url = "https://www.pixiv.net" + endpoint
        async with aiohttp.ClientSession() as cs:
            async with cs.request(method, url, **kwargs) as r:
                if r.status != 200:
                    return None
                response = await r.json(content_type=None)
                return response

    async def get_ranking(self, mode: str):
        return await self.request(
            "GET",
            f"/ranking.php",
            params={"format": "json", "content": "illust", "mode": mode},
        )

    async def get_original_url(self, index: int):
        resp = await self.request("GET", f"/ajax/illust/{index}/pages")
        url = resp["body"][0]["urls"]["original"]
        return url

    async def get_info(self, index: int):
        resp = await self.request("GET", f"/ajax/illust/{index}")
        if resp["error"]:
            return discord.Embed(title="결과가 없습니다. 정확히 입력했는지 확인해주세요.")
        elif resp["body"]["tags"]["tags"][0]["tag"] == "R-18":
            return discord.Embed(title="현재 R-18 일러스트는 확인이 불가능합니다.")
        else:
            return PixivModel(
                resp["body"]["bookmarkCount"],
                resp["body"]["illustComment"],
                resp["body"]["id"],
                resp["body"]["likeCount"],
                resp["body"]["title"],
                resp["body"]["userName"],
                resp["body"]["uploadDate"],
                resp["body"]["viewCount"],
            )


class PixivExt(PixivRequester):
    @staticmethod
    def shuffle_image_url(url: str):
        parsed_url = re.search(
            r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)", url
        )
        prefix = parsed_url.group(0)
        main_url = parsed_url.group(1).replace(".", "_")
        _type = parsed_url.group(2)
        image = parsed_url.group(3).replace("/", "_")

        return f"{prefix}_{_type}{main_url}_{image}"

    @staticmethod
    def recompile_date(date: str):
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime(
            "%Y년 %m월 %d일"
        )

    async def make_illust_embed(self, info: PixivModel):
        illust_url = await self.get_original_url(info.id)
        embed = discord.Embed(description=info.id, color=0x008AE6)
        embed.set_image(
            url=f"https://doujinshiman.ga/v3/api/proxy/{self.shuffle_image_url(illust_url)}"
        )
        embed.set_author(
            name=info.title, url=f"https://www.pixiv.net/artworks/{info.id}"
        )
        embed.set_footer(text=f"Illust by {info.username}")

        return embed

    async def make_ranking_illust_embed(self, info: PixivRankingModel):
        illust_url = await self.get_original_url(info.id)
        embed = discord.Embed(
            url=f"https://www.pixiv.net/artworks/{info.id}",
            description=info.id,
            color=0x008AE6,
        )
        embed.set_image(
            url=f"https://doujinshiman.ga/v3/api/proxy/{self.shuffle_image_url(illust_url)}"
        )
        embed.set_author(name=f"#{info.rank} | {info.title}")
        embed.set_footer(text=f"Illust by {info.username}")

        return embed

    async def make_info_embed(self, info: PixivModel):
        illust_url = await self.get_original_url(info.id)
        embed = discord.Embed(
            title=info.title,
            url=f"https://www.pixiv.net/artworks/{info.id}",
            color=0x008AE6,
        )
        embed.set_image(
            url=f"https://doujinshiman.ga/v3/api/proxy/{self.shuffle_image_url(illust_url)}"
        )
        embed.add_field(name="설명", value=info.comment, inline=True)
        embed.add_field(name="작가", value=info.username, inline=True)
        embed.set_footer(
            text=f"👍 {info.like} ❤️ {info.bookmark} 👁️ {info.view} • 업로드 날짜 {self.recompile_date(info.uploadDate)}"
        )

        return embed

    async def handle(self, resp, type):
        if isinstance(resp, discord.Embed):
            return resp

        if type == "illust":
            return await self.make_illust_embed(resp)
        elif type == "info":
            return await self.make_info_embed(resp)

    async def illust_embed(self, index):
        info = await self.get_info(index)
        return await self.handle(info, "illust")

    async def info_embed(self, index):
        info = await self.get_info(index)
        return await self.handle(info, "info")

    async def ranking_embed(self, mode):
        ranking = await self.get_ranking(mode)
        rank_embed = list(
            await asyncio.gather(
                *list(
                    map(
                        self.make_ranking_illust_embed,
                        PixivRankingModel.generator_pixiv_ranking_info(
                            ranking["contents"]
                        ),
                    )
                )
            )
        )
        return rank_embed

    async def latency(self):
        pixiv_latency = time.perf_counter()
        await self.request("GET", "/ajax")
        return time.perf_counter() - pixiv_latency
