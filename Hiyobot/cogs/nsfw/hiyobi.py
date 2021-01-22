import discord
from discord.ext import commands

from Hiyobot.bot import Hiyobot
from utils.pagenator import pagenator


class Hiyobi(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="히요비번호")
    @commands.is_nsfw()
    async def _hiyobi_info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 히요비에서 해당 작품정보를 가져옵니다.

        사용할 수 있는 값 : 작품 번호(필수)

        사용 예시 : ``&히요비번호 1496588``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed = await self.bot.hiyobi.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="히요비리스트")
    @commands.is_nsfw()
    async def _hiyobi_list(self, ctx: commands.Context, num: int = 1):
        """
        히요비에서 최근 올라온 작품을 가져옵니다.

        사용할 수 있는 값 : 페이지(입력하지 않을 경우 1)

        사용 예시 : ``&히요비리스트`` 또는 ``&히요비리스트 2``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed_list = await self.bot.hiyobi.list_embed(num)

        if embed_list:
            return await pagenator(self.bot, ctx, msg, embed_list)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command(name="히요비검색")
    @commands.is_nsfw()
    async def _hiyobi_search(self, ctx: commands.Context, *keyword):
        """
        히요비에서 작품을 검색합니다.

        사용할 수 있는 값 : 검색할 키워드(필수)

        사용 예시 : ``&히요비검색 파이하드``
        """
        search = list(keyword)
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed_list = await self.bot.hiyobi.search_embed(search)

        if embed_list:
            return await pagenator(self.bot, ctx, msg, embed_list)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))


def setup(bot: Hiyobot):
    bot.add_cog(Hiyobi(bot))
