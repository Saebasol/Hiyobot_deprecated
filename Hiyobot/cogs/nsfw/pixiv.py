import discord
from discord.ext import commands

from utils.pixiv import PixivExt
from utils.pixiv import is_r18
from utils.pagenator import pagenator


embed_r18 = discord.Embed(title="해당 일러스트는 R-18 인 것 같습니다.\n연령 제한이 설정된 채널에서 사용해주세요.")


class Pixiv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pixiv = PixivExt()

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
        if not ctx.channel.nsfw:
            if await is_r18(index):
                return await msg.edit(embed=embed_r18)
        embed = await self.pixiv.illust_embed(index)
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
        if not ctx.channel.nsfw:
            if await is_r18(index):
                return await msg.edit(embed=embed_r18)
        embed = await self.pixiv.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="픽시브랭킹")
    async def _pixiv_ranking(self, ctx: commands.Context, mode: str = "daily"):
        """
        픽시브 랭킹을 가져옵니다.

        사용할 수 있는 값 : 모드(입력하지 않을 경우 일일)

        사용 예시 : ``&픽시브랭킹`` 또는 ``&픽시브랭킹 주간/월간``
        """
        if mode == "주간":
            mode = "weekly"
        elif mode == "월간":
            mode = "monthly"
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        await self.pixiv.cache_ranking_embed(mode)
        await pagenator(self.bot, ctx, msg, self.pixiv.cache, "pixiv_ranking_embed")


def setup(bot: commands.Bot):
    bot.add_cog(Pixiv(bot))