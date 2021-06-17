import asyncio
import re
import time
from datetime import datetime

import aiohttp
import discord
from bs4 import BeautifulSoup

from utils.request import Request


class PixivInfoModel:
    def __init__(self, bookmark, comment, id, like, title, username, upload_date, view):
        self.bookmark = bookmark
        self.comment = comment
        self.id = id
        self.like = like
        self.title = title
        self.username = username
        self.upload_date = upload_date
        self.view = view


class PixivIllustModel:
    def __init__(self, id, title, url, username, rank=None, is_r18=False):
        self.id = id
        self.title = title
        self.url = url
        self.username = username
        self.rank = rank
        self.is_r18 = is_r18

    @classmethod
    def generate_pixiv_ranking_info(cls, info_list: list):
        for info in info_list:
            yield cls(
                info["illust_id"],
                info["title"],
                info["url"],
                info["user_name"],
                info["rank"],
            )


class PixivRequester(Request):
    async def get(self, endpoint, include_body=False, **kwargs):
        resp = await super().get("https://www.pixiv.net" + endpoint, "json", **kwargs)
        if resp.status != 200:
            return None
        if include_body:
            return resp.body["body"]
        return resp.body

    @staticmethod
    def shuffle_image_url(url: str):
        url_parse_regex = re.compile(
            r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)"
        )

        parsed_url: list[str] = url_parse_regex.findall(url)[0]

        prefix = parsed_url[0]
        main_url = parsed_url[1].replace(".", "_")
        type_ = parsed_url[2]
        image = parsed_url[3].replace("/", "_")

        return f"{prefix}_{type_}{main_url}_{image}"

    async def get_ranking(self, mode: str):
        return await (
            self.get(
                "/ranking.php",
                params={"format": "json", "content": "illust", "mode": mode},
            )
        )

    async def get_original_url(self, index: int):
        resp = await self.get(f"/ajax/illust/{index}/pages", True)
        if not resp:
            return "https://cdn.discordapp.com/attachments/848196621194756126/848196685389365268/unnamed_1.png"
        illust_url = resp[0]["urls"]["original"]
        return f"https://beta.doujinshiman.ga/v4/api/proxy/{self.shuffle_image_url(illust_url)}"

    async def get_info(self, index: int):
        resp = await self.get(f"/ajax/illust/{index}", True)
        if not resp:
            return discord.Embed(title="해당 작품은 삭제되었거나 존재하지 않는 작품 ID입니다.")
        return PixivInfoModel(
            resp["bookmarkCount"],
            resp["illustComment"],
            resp["id"],
            resp["likeCount"],
            resp["title"],
            resp["userName"],
            resp["uploadDate"],
            resp["viewCount"],
        )

    async def get_illust(self, index: int):
        resp = await self.get(f"/ajax/illust/{index}", True)
        if not resp:
            return discord.Embed(title="해당 작품은 삭제되었거나 존재하지 않는 작품 ID입니다.")
        return PixivIllustModel(
            resp["id"],
            resp["title"],
            resp["urls"]["original"],
            resp["userName"],
            is_r18=resp["tags"]["tags"][0]["tag"] == "R-18",
        )


class PixivResolver(PixivRequester):
    @staticmethod
    def html2text(html: str):
        soup = BeautifulSoup(html, "html.parser")
        text_parts = soup.findAll(text=True)
        return "".join(text_parts)

    @staticmethod
    def recompile_date(date: str):
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y년 %m월 %d일")

    async def make_info_embed(self, info: PixivInfoModel):
        embed = discord.Embed(
            title=info.title,
            url=f"https://www.pixiv.net/artworks/{info.id}",
            color=0x008AE6,
        )
        embed.set_image(url=await self.get_original_url(info.id))
        embed.add_field(name="설명", value=self.html2text(info.comment), inline=True)
        embed.add_field(name="작가", value=info.username, inline=True)
        embed.set_footer(
            text=f"👍 {info.like} ❤️ {info.bookmark} 👁️ {info.view} • 업로드 날짜 {self.recompile_date(info.upload_date)}"
        )
        return embed

    async def make_illust_embed(self, info: PixivIllustModel):
        if info.rank:
            title = f"#{info.rank} | {info.title}"
        else:
            title = info.title
        embed = discord.Embed(description=info.id, color=0x008AE6)
        embed.set_author(name=title, url=f"https://www.pixiv.net/artworks/{info.id}")
        embed.set_image(
            url=f"https://beta.doujinshiman.ga/v4/api/proxy/{self.shuffle_image_url(info.url)}"
        )
        embed.set_footer(text=f"Illust by {info.username}")
        return embed

    async def handle(self, resp, type):
        if isinstance(resp, discord.Embed):
            return resp

        if type == "illust":
            return await self.make_illust_embed(resp)
        elif type == "info":
            return await self.make_info_embed(resp)

    async def illust_embed(self, index: int, is_nsfw: bool):
        info = await self.get_illust(index)
        if info.is_r18 and is_nsfw == False:
            return discord.Embed(title="R-18 일러스트는 연령 제한 채널에서만 확인하실 수 있습니다.")
        return await self.handle(info, "illust")

    async def info_embed(self, index: int):
        info = await self.get_info(index)
        return await self.handle(info, "info")

    async def ranking_embed(self, mode):
        ranking = await self.get_ranking(mode)
        rank_embed = list(
            await asyncio.gather(
                *list(
                    map(
                        self.make_illust_embed,
                        PixivIllustModel.generate_pixiv_ranking_info(
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
