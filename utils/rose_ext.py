import time
from random import choice

import discord
from discord.embeds import Embed
from rose.client import _Client


class RoseExt(_Client):
    def __init__(self, authorization):
        super().__init__(authorization)

    @staticmethod
    def parse_value_url(value_url_list: list):
        if not value_url_list:
            return ["없음"]
        else:
            return [
                f"[{value_url_dict['value']}](https://hitomi.la{value_url_dict.url})"
                for value_url_dict in value_url_list
            ]

    @staticmethod
    def make_viewer_embed(img_list, total) -> list[Embed]:
        embed = []
        num = 0

        for file_info in img_list["images"]:
            num += 1
            embed.append(
                discord.Embed()
                .set_image(url=file_info["url"])
                .set_footer(text=f"{num}/{total} 페이지")
            )

        return embed

    def make_embed_with_info(self, info):
        tags_join = (
            ", ".join(self.parse_value_url(info.tags))
            .replace("♀", "\♀")
            .replace("♂", "\♂")
        )
        embed = discord.Embed(
            title=info.title["value"],
            description=f"[{info.language['value']}]({info.language['url']})",
            url=info.title["url"],
        )
        embed.set_thumbnail(
            url=f"https://doujinshiman.ga/v3/api/proxy/{info.thumbnail}"
        )
        embed.add_field(
            name="번호",
            value=f"[{info.galleryid}](https://hitomi.la/reader/{info.galleryid}.html)",
            inline=False,
        )
        embed.add_field(
            name="타입", value=f"[{info.type['value']}]({info.type['url']})", inline=False
        )
        embed.add_field(
            name="작가", value=",".join(self.parse_value_url(info.artist)), inline=False
        )
        embed.add_field(
            name="그룹", value=",".join(self.parse_value_url(info.group)), inline=False
        )
        embed.add_field(
            name="원작", value=",".join(self.parse_value_url(info.series)), inline=False
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

    async def list_embed(self, number):
        lists = await self.list_(number)
        if lists.status != 200:
            return
        return [self.make_embed_with_info(list_) for list_ in lists.list]

    async def info_embed(self, index):
        info = await self.info(index)

        if info.status != 200:
            return

        return self.make_embed_with_info(info)

    async def random_embed(self):
        index_list = await self.index()

        info = await self.info(choice(index_list))  # type: ignore

        return self.make_embed_with_info(info)

    async def viewer_embed(self, index):
        galleryinfo = await self.galleryinfo(index)

        if galleryinfo.status != 200:
            return

        total = len(galleryinfo.files)
        img_list = await self.images(index)

        return self.make_viewer_embed(img_list, total)

    async def latency(self):
        heliotrope_latency1 = time.perf_counter()
        await self.request("GET", "/")
        heliotrope_latency2 = time.perf_counter()
        return heliotrope_latency2 - heliotrope_latency1
