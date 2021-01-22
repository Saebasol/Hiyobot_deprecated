import discord
from discord.ext import commands

from Hiyobot.bot import Hiyobot
from utils.pagenator import pagenator


class Heliotrope(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="번호")
    @commands.is_nsfw()
    async def _info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 히토미에서 해당 작품 정보를 가져옵니다.

        사용할 수 있는 값 : 작품 번호(필수)

        사용 예시 : ``&번호 1496588``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )

        embed = await self.bot.rose.info_embed(index)
        if embed:
            return await msg.edit(embed=embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command(name="랜덤")
    @commands.is_nsfw()
    async def _random(self, ctx: commands.Context):
        """
        랜덤으로 작품 정보 하나를 가져옵니다.

        사용 예시 : ``&랜덤``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed = await self.bot.rose.random_embed()
        await msg.edit(embed=embed)

    @commands.command(name="리스트")
    @commands.is_nsfw()
    async def _list(self, ctx: commands.Context, num: int = 1):
        """
        히토미에서 최근 올라온 한국어 작품을 가져옵니다.

        사용할 수 있는 값 : 페이지(입력하지 않을 경우 1)

        사용 예시 : ``&리스트`` 또는 ``&리스트 2``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요")
        )
        embed = await self.bot.rose.list_embed(num)

        if embed:
            return await pagenator(self.bot, ctx, msg, embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command(name="뷰어")
    @commands.is_nsfw()
    async def _viewer(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 디스코드 내에서 보여줍니다.

        인자값: 작품 번호(필수)

        사용법: ``&뷰어 1496588``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요.")
        )
        embed = await self.bot.rose.viewer_embed(index)
        if embed:
            await pagenator(self.bot, ctx, msg, embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))


def setup(bot: Hiyobot):
    bot.add_cog(Heliotrope(bot))
