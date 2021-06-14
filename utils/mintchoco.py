import time
from random import choice
from typing import Iterable

import discord
from discord.embeds import Embed
from mintchoco.client import API_URL, Client  # type: ignore
from mintchoco.model import (  # type: ignore
    HeliotropeImages,
    HeliotropeInfo,
    Tag,
)


class HeliotropeResolver(Client):
    @staticmethod
    def parse_value_url(value_url_list: Iterable[Tag]):
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

        for file_info in img_list.files:
            num += 1
            embeds.append(
                discord.Embed()
                .set_image(url=file_info.image)
                .set_footer(text=f"{num}/{total} 페이지")
            )

        return embeds

    def make_embed_with_info(self, info: HeliotropeInfo):
        print(info)
        tags_join = (
            ", ".join(self.parse_value_url(info.tags))
            .replace("♀", "\\♀")
            .replace("♂", "\\♂")
        )
        embed = discord.Embed(
            title=info.title,
            description=f"[{info.language.value}]({info.language.url})",
            url=f"https://hitomi.la/galleries/{info.index}.html",
        )
        embed.set_thumbnail(url=f"{API_URL}/proxy/{info.thumbnail}")
        embed.add_field(
            name="번호",
            value=f"[{info.index}](https://hitomi.la/reader/{info.index}.html)",
            inline=False,
        )
        embed.add_field(
            name="타입",
            value=f"[{info.type.value}]({info.type.url})",
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
        print(embed)
        return embed

    async def list_embed(self, number: int):
        heliotrope_lists = await self.list(number)

        if heliotrope_lists.status != 200:
            return

        return [
            self.make_embed_with_info(heliotrope_list)
            for heliotrope_list in heliotrope_lists.list
        ]

    async def info_embed(self, index: int):
        info = await self.info(index)

        if info.status != 200:
            return

        return self.make_embed_with_info(info)

    async def viewer_embed(self, index: int):
        galleryinfo = await self.galleryinfo(index)

        if galleryinfo.status != 200:
            return

        return self.make_viewer_embed(
            await self.images(index), len(list(galleryinfo.files))
        )

    async def search_embed(self, query: str):
        galleryinfo = await self.search(query)

        if galleryinfo.status != 200:
            return

        return [
            self.make_embed_with_info(result)
            for result in galleryinfo.result
        ]

    async def count_embed(self):
        count_info = await self.count()

        if count_info.status != 200:
            return

        return discord.Embed(
            title="히요봇에서 집계된 랭킹입니다.",
            description="\n".join(
                [
                    f"{index}. [{info.title}](https://hitomi.la/galleries/{info.index}.html): {info.count}회"
                    for index, info in enumerate(count_info.list, 1)
                ]
            ),
        )

    async def latency(self):
        heliotrope_latency = time.perf_counter()
        await self.about()
        return heliotrope_latency - time.perf_counter()
