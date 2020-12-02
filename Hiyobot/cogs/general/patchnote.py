import aiohttp
import discord
from discord.ext import commands

import Hiyobot


class PatchNote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="패치노트")
    async def _patchnote(self, ctx: commands.Context):
        """
        패치노트가 올라옵니다.
        중요한 정보가 올라오니 꼭 확인해보세요!

        사용법: ``&패치노트``
        """
        headers = {"Accept": "application/vnd.github.v3+json"}
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://api.github.com/repos/SaidBySolo/Hiyobot/releases/tags/{Hiyobot.__version__}",
                headers=headers,
            ) as r:
                if r.status == 404:
                    return await ctx.send(
                        f"해당 버전 ``{Hiyobot.__version__}``의 릴리즈가 아직 존재하지않아요."
                    )
                response_json = await r.json()

        embed = discord.Embed(
            title="Patch Note", description=f"{response_json['tag_name']}"
        )
        embed.add_field(name=response_json["name"], value=response_json["body"])

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(PatchNote(bot))
