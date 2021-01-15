import asyncio
import re
import time

import aiocache
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


async def get_info(index) -> PixivModel:
    resp = await request("GET", f"ajax/illust/{index}")
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


def shuffle_image_url(url: str):
    url_parse_regex = re.compile(r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)")

    parsed_url: list[str] = url_parse_regex.findall(url)[0]

    prefix = parsed_url[0]
    main_url = parsed_url[1].replace(".", "_")
    type_ = parsed_url[2]
    image = parsed_url[3].replace("/", "_")

    main = f"{prefix}_{type_}{main_url}_{image}"

    return main


def recompile_date(date):
    regex = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    match = regex.search(date)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    return f"{year}년 {month}월 {day}일"


async def request(method, endpoint, json=None):
    url = "https://www.pixiv.net/" + endpoint
    async with aiohttp.ClientSession() as cs:
        async with cs.request(method, url, json=json) as r:
            if r.status == 404:
                return None
            response = await r.json(content_type=None)
            return response


async def get_ranking(mode):
    return await request("GET", f"ranking.php?format=json&content=illust&mode={mode}")


async def get_original_url(index):
    resp = await request("GET", f"ajax/illust/{index}/pages")
    url = resp["body"][0]["urls"]["original"]
    return url


async def is_r18(index):
    resp = await request("GET", f"ajax/illust/{index}")
    return True if resp["body"]["tags"]["tags"][0]["tag"] == "R-18" else False


async def make_illust_embed(info: PixivModel):
    illust_url = await get_original_url(info.id)
    embed = discord.Embed(description=info.id, color=0x008AE6)
    embed.set_image(
        url=f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(illust_url)}"
    )
    embed.set_author(name=info.title, url=f"https://www.pixiv.net/artworks/{info.id}")
    embed.set_footer(text=f"Illust by {info.username}")

    return embed


async def make_ranking_illust_embed(info: PixivRankingModel):
    illust_url = await get_original_url(info.id)
    embed = discord.Embed(description=info.id, color=0x008AE6)
    embed.set_image(
        url=f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(illust_url)}"
    )
    embed.set_author(name=f"#{info.rank} | {info.title}")
    embed.set_footer(text=f"Illust by {info.username}")

    return embed


async def make_info_embed(info: PixivModel):
    illust_url = await get_original_url(info.id)
    embed = discord.Embed(
        title=info.title,
        description=info.username,
        url=f"https://www.pixiv.net/artworks/{info.id}",
        color=0x008AE6,
    )
    embed.set_thumbnail(
        url=f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(illust_url)}"
    )
    embed.add_field(name="설명", value=info.comment, inline=False)
    embed.add_field(name=":thumbsup:", value=info.like)
    embed.add_field(name=":heart:", value=info.like)
    embed.add_field(name=":eye:", value=info.view)
    embed.set_footer(text=recompile_date(info.uploadDate))

    return embed


class PixivExt:
    def __init__(self):
        self.cache = aiocache.Cache()

    async def illust_embed(self, index):
        info = await get_info(index)
        return await make_illust_embed(info)

    async def info_embed(self, index):
        info = await get_info(index)
        return await make_info_embed(info)

    async def cache_ranking_embed(self, mode):
        ranking = await get_ranking(mode)
        embed_coroutine_list = [
            make_ranking_illust_embed(model)
            for model in PixivRankingModel.generator_pixiv_ranking_info(
                ranking["contents"]
            )
        ]
        done, _ = await asyncio.wait(embed_coroutine_list)
        embed = [d.result() for d in done]

        await self.cache.set("pixiv_ranking_embed", embed)

    async def latency(self):
        pixiv_latency1 = time.perf_counter()
        await request("GET", "/ajax")
        pixiv_latency2 = time.perf_counter()
        return pixiv_latency2 - pixiv_latency1
