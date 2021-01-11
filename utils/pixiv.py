import time

import aiocache
import aiohttp
import discord
import re


def shuffle_image_url(url: str):
    url_parse_regex = re.compile(
        r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)")

    parsed_url: list[str] = url_parse_regex.findall(url)[0]

    prefix = parsed_url[0]
    main_url = parsed_url[1].replace(".", "_")
    type_ = parsed_url[2]
    image = parsed_url[3].replace("/", "_")

    main = f"{prefix}_{type_}{main_url}_{image}"

    return main

def recompile_date(date):
    regex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    match = regex.search(date)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    return f'{year}년 {month}월 {day}일'


async def request(method, endpoint, json=None):
    url = "https://www.pixiv.net/" + endpoint
    async with aiohttp.ClientSession() as cs:
        async with cs.request(method, url, json=json) as r:
            if r.status == 404:
                return None
            response = await r.json(content_type=None)
            return response


async def get_original_url(illust_id):
    resp = await request("GET", f"ajax/illust/{illust_id}/pages")
    url = resp["body"][0]["urls"]["original"]
    return url


async def get_user_icon(user_id):
    resp = await request("GET", f"ajax/user/{user_id}")
    return resp["body"]["image"]


async def is_r18(illust_id):
    resp = await request("GET", f"ajax/illust/{illust_id}")
    return True if resp["body"]["tags"]["tags"][0]["tag"] == "R-18" else False


class PixivExt:
    def __init__(self):
        self.cache = aiocache.Cache()

    async def illust_embed(self, illust_id):
        resp = await request("GET", f"ajax/illust/{illust_id}")
        user_id = resp["body"]["userId"]
        user_name = resp["body"]["userName"]
        user_icon = await get_user_icon(user_id)
        url = await get_original_url(illust_id)
        embed = discord.Embed()
        embed.set_image(url=f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(url)}")
        embed.set_author(
            name=resp["body"]["illustTitle"],
            icon_url=user_icon,
            url=f"https://www.pixiv.net/artworks/{illust_id}"
        )
        embed.set_footer(text=f"Illust by {user_name}")
        return embed

    async def info_embed(self, illust_id):
        resp = await request("GET", f"ajax/illust/{illust_id}")
        url = await get_original_url(illust_id)
        """
        tags = [t["translation"]["en"] for t in resp["body"]["tags"]["tags"]]
        tag = ", ".join(tags)
        """
        embed = discord.Embed(
            title=resp["body"]["illustTitle"],
            description=resp["body"]["userName"],
            url=f"https://www.pixiv.net/artworks/{illust_id}"
        )
        embed.set_thumbnail(url=f"https://doujinshiman.ga/v3/api/proxy/{shuffle_image_url(url)}")
        embed.add_field(
            name="설명", value=resp["body"]["illustComment"], inline=False
        )
        embed.add_field(
            name=":thumbsup:", value=resp["body"]["likeCount"]
        )
        embed.add_field(
            name=":heart:", value=resp["body"]["bookmarkCount"]
        )
        embed.add_field(
            name=":eye:", value=resp["body"]["viewCount"]
        )
        """
        embed.add_field(
            name="태그",
            value=tag if len(tag) <= 1024 else "표시하기에는 너무 길어요."
        )
        """
        embed.set_footer(text=recompile_date(resp["body"]["uploadDate"]))
        return embed

    async def ranking_embed(self, mode):
        resp = await request("GET", f"ranking.php?format=json&content=illust&mode={mode}")

    async def latency(self):
        pixiv_latency1 = time.perf_counter()
        await request("GET", "/")
        pixiv_latency2 = time.perf_counter()
        return pixiv_latency2 - pixiv_latency1