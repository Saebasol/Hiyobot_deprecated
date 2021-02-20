import time
from random import choice
from typing import Iterable

import discord
from discord.embeds import Embed
from rose import Client  # type: ignore
from rose.model import (  # type: ignore
    HeliotropeImages,
    HeliotropeInfo,
    HeliotropeValueData,
)


class RoseExt(Client):
    @staticmethod
    def parse_value_url(value_url_list: Iterable[HeliotropeValueData]):
        if value_url_list:
            return [
                f"[{value_url_dict.value}](https://hitomi.la{value_url_dict.url})"
                for value_url_dict in value_url_list
            ]

        return ["없음"]

    @staticmethod
    def make_viewer_embed(img_list: HeliotropeImages, total: int) -> list[Embed]:
        embeds = []
        num = 0

        for file_info in img_list.images:
            num += 1
            embeds.append(
                discord.Embed()
                .set_image(url=file_info.url)
                .set_footer(text=f"{num}/{total} 페이지")
            )

        return embeds

    def make_embed_with_info(self, info: HeliotropeInfo):
        tags_join = (
            ", ".join(self.parse_value_url(info.tags))
            .replace("♀", "\\♀")
            .replace("♂", "\\♂")
        )
        embed = discord.Embed(
            title=info.title.__next__().value,
            description=f"[{info.language.__next__().value}]({info.language.__next__().url})",
            url=info.title.__next__().url,
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
            name="타입",
            value=f"[{info.type.__next__().value}]({info.type.__next__().url})",
            inline=False,
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

    async def list_embed(self, number: int):
        lists = await self.list_(number)
        if lists.status != 200:
            return
        return [self.make_embed_with_info(list_) for list_ in lists.list]

    async def info_embed(self, index: int):
        info = await self.info(index)

        if info.status != 200:
            return

        return self.make_embed_with_info(info)

    async def random_embed(self):
        index_list = await self.index()

        info = await self.info(choice(index_list))

        return self.make_embed_with_info(info)

    async def viewer_embed(self, index: int):
        galleryinfo = await self.galleryinfo(index)

        if galleryinfo.status != 200:
            return

        return self.make_viewer_embed(
            await self.images(index), len(list(galleryinfo.files))
        )

    async def latency(self):
        heliotrope_latency1 = time.perf_counter()
        await self.request("GET", "/")
        heliotrope_latency2 = time.perf_counter()
        return heliotrope_latency2 - heliotrope_latency1
