import discord
from discord.ext import commands

from Hiyobot.bot import Hiyobot
from utils.pagenator import pagenator

embed_r18 = discord.Embed(title="현재 R-18 일러스트는 확인이 불가능합니다.")


class Pixiv(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="픽시브")
    async def _pixiv_view(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 픽시브에서 해당 작품을 가져와 보여줍니다.

        사용할 수 있는 값 : 작품 번호(필수)

        사용 예시 : ``&픽시브 86094006``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed = await self.bot.pixiv.illust_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="픽시브정보")
    async def _pixiv_info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 픽시브에서 해당 작품정보를 가져옵니다.

        사용할 수 있는 값 : 작품 번호(필수)

        사용 예시 : ``&픽시브정보 86094006``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed = await self.bot.pixiv.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="픽시브랭킹")
    async def _pixiv_ranking(self, ctx: commands.Context, mode: str = "일간"):
        """
        픽시브 랭킹을 가져옵니다.

        사용할 수 있는 값 : 모드(입력하지 않을 경우 일일)

        사용 예시 : ``&픽시브랭킹`` 또는 ``&픽시브랭킹 주간/월간``
        """
        mode_dict = {"주간": "weekly", "월간": "monthly", "일간": "daily"}

        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )

        if param := mode_dict.get(mode):
            rank_embed = await self.bot.pixiv.ranking_embed(param)
            await pagenator(self.bot, ctx, msg, rank_embed)
        else:
            return await ctx.send("잘못된 값입니다. ``&도움말``을 입력해서 확인해주세요.")


def setup(bot: Hiyobot):
    bot.add_cog(Pixiv(bot))
