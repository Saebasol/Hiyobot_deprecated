import discord
from discord.ext.commands import command
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context

import hiyobot
from hiyobot.bot import Hiyobot


class PatchNote(Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @command(name="패치노트")
    async def _patchnote(self, ctx: Context, version: str = None):
        """
        패치노트가 올라옵니다.
        중요한 정보가 올라오니 꼭 확인해보세요!

        사용 예시 : ``&패치노트`` ``&패치노트 3.0.0``
        """
        r = await self.bot.request.get(
            f"https://api.github.com/repos/Saebasol/Hiyobot/releases/tags/{version or hiyobot.__version__}",
            "json",
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        if r.status == 404:
            return await ctx.send(f"해당 버전 ``{hiyobot.__version__}``의 릴리즈가 아직 존재하지 않아요.")
        embed = discord.Embed(title="Patch Note", description=f"{r.body['tag_name']}")
        embed.add_field(name=r.body["name"], value=r.body["body"])
        await ctx.send(embed=embed)


def setup(bot: Hiyobot):
    bot.add_cog(PatchNote(bot))
