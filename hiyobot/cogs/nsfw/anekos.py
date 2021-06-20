import random
from typing import Any

import discord
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import command

from hiyobot.bot import Hiyobot
from utils.anekos import URL, nsfw_tags, sfw_tags


class Nekos(Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @command(name="네코", aliases=["neko"])
    async def _neko(
        self,
        ctx: Context,
        tag: Any = None,
    ):
        """
        귀여운 네코미미를 보여줍니다. 태그를 사용해서 검색도 가능합니다.

        사용할 수 있는 값 : 태그(선택)

        사용 예시 : ``&네코`` 또는 ``&네코 wallpaper``
        """
        embed = discord.Embed(colour=0xC44BAB)
        embed.set_footer(
            text="With Nekos.life",
            icon_url="https://avatars.githubusercontent.com/u/34457007?s=200&v=4",
        )
        if tag:
            if tag in ["도움말", "help"]:
                embed = discord.Embed(title="사용할 수 있는 태그 목록입니다.")
                embed.add_field(name="전연령 태그", value="\n".join(sfw_tags))
                if ctx.channel.is_nsfw():  # type:ignore
                    embed.add_field(name="성인 태그", value="\n".join(nsfw_tags))
                return await ctx.send(embed=embed)

            if not ctx.channel.is_nsfw():  # type:ignore
                if tag in nsfw_tags:
                    return await ctx.send(
                        "해당 태그는 성인 태그인 것 같습니다. 연령 제한이 설정된 채널에서 사용해주세요."
                    )
            if tag not in sfw_tags or tag not in nsfw_tags:
                return await ctx.send("해당 태그는 없어요! 태그는 ``&네코 도움말``을 통해 확인하실 수 있어요.")
        else:
            tag = random.choice(sfw_tags if not ctx.channel.is_nsfw() else nsfw_tags)  # type: ignore

        img_url = (await self.bot.request.get(URL + f"/{tag}", "json")).body["url"]
        await ctx.send(embed=embed.set_image(url=img_url))


def setup(bot: Hiyobot):
    bot.add_cog(Nekos(bot))
