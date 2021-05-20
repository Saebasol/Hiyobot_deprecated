import asyncio
import aiohttp
import discord
from bs4 import BeautifulSoup
import re
import time


class PixivInfoModel:
    def __init__(self, bookmark, comment, id, like, title, username, date, view):
        self.bookmark = bookmark
        self.comment = comment
        self.id = id
        self.like = like
        self.title = title
        self.username = username
        self.date = date
        self.view = view


class PixivIllustModel:
    def __init__(self, id, title, url, username, rank=None):
        self.id = id
        self.title = title
        self.url = url
        self.username = username
        self.rank = rank

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


class PixivRequester:
    @staticmethod
    async def request(method, endpoint, **kwargs):
        url = "https://www.pixiv.net" + endpoint
        async with aiohttp.ClientSession() as cs:
            async with cs.request(method, url, **kwargs) as r:
                if r.status != 200:
                    return None
                return await r.json(content_type=None)

    async def get_ranking(self, mode: str):
        return await self.request(
            "GET",
            "/ranking.php",
            params={"format": "json", "content": "illust", "mode": mode},
        )

    async def get_original_url(self, index: int):
        resp = await self.request("GET", f"/ajax/illust/{index}/pages")
        return resp["body"][0]["urls"]["original"]

    async def get_info(self, index: int):
        resp = await self.request("GET", f"/ajax/illust/{index}")
        if resp["error"]:
            return discord.Embed(title="해당 작품은 삭제되었거나 존재하지 않는 작품 ID입니다.")
        return PixivInfoModel(
            resp["body"]["bookmarkCount"],
            resp["body"]["illustComment"],
            resp["body"]["id"],
            resp["body"]["likeCount"],
            resp["body"]["title"],
            resp["body"]["userName"],
            resp["body"]["uploadDate"],
            resp["body"]["viewCount"],
        )

    async def get_illust(self, index: int):
        resp = await self.request("GET", f"/ajax/illust/{index}")
        if resp["error"]:
            return discord.Embed(title="해당 작품은 삭제되었거나 존재하지 않는 작품 ID입니다.")
        return PixivIllustModel(
            resp["body"]["id"],
            resp["body"]["title"],
            resp["body"]["urls"]["original"],
            resp["body"]["userName"],
        )


class PixivExt(PixivRequester):
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

    @staticmethod
    def html2text(html: str):
        soup = BeautifulSoup(html, "html.parser")
        text_parts = soup.findAll(text=True)
        return "".join(text_parts)

    async def make_info_embed(self, info: PixivInfoModel):
        illust_url = await self.get_original_url(info.id)
        embed = discord.Embed(
            title=info.title,
            url=f"https://www.pixiv.net/artworks/{info.id}",
            color=0x008AE6,
        )
        embed.set_image(
            url=f"https://beta.doujinshiman.ga/v4/api/proxy/{self.shuffle_image_url(illust_url)}"
        )
        embed.add_field(name="설명", value=self.html2text(info.comment), inline=True)
        embed.add_field(name="작가", value=info.username, inline=True)
        embed.set_footer(
            text=f"👍 {info.like} ❤️ {info.bookmark} 👁️ {info.view} • 업로드 날짜 {self.recompile_date(info.uploadDate)}"
        )
        return embed

    async def make_illust_embed(self, info: PixivIllustModel, is_ranking: bool = False):
        illust_url = await self.get_original_url(info.id)
        title = f"#{info.rank} | {info.title}" if is_ranking else info.title
        embed = discord.Embed(description=info.id, color=0x008AE6)
        embed.set_author(name=title, url=f"https://www.pixiv.net/artworks/{info.id}")
        embed.set_image(
            url=f"https://beta.doujinshiman.ga/v4/api/proxy/{self.shuffle_image_url(illust_url)}"
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

    async def illust_embed(self, index: int):
        info = await self.get_illust(index)
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
                        True,
                    )
                )
            )
        )
        return rank_embed

    async def latency(self):
        pixiv_latency = time.perf_counter()
        await self.request("GET", "/ajax")
        return time.perf_counter() - pixiv_latency
