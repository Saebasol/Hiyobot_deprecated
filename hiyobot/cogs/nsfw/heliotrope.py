import discord
from discord.ext import commands

from hiyobot.bot import Hiyobot
from utils.pagenator import pagenator


class Heliotrope(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        if self.bot.heliotrope_issue and await self.bot.is_owner(ctx.author):
            await ctx.send(
                embed=discord.Embed(
                    title="Heliotrope 서버에 문제가 있어 시도할수 없습니다.",
                    description="이 문제가 계속된다면 [공식 디스코드](https://discord.gg/PSshFYr)로 문의해주세요",
                )
            )
        else:
            return True

    @commands.command(name="번호")
    @commands.is_nsfw()
    async def _info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 히토미에서 해당 작품 정보를 가져옵니다.

        사용할 수 있는 값 : 작품 번호(필수)

        사용 예시 : ``&번호 1496588``
        """
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))

        if embed := await self.bot.mintchoco.info_embed(index):
            return await msg.edit(embed=embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command("검색")
    @commands.is_nsfw()
    async def _search(self, ctx: commands.Context, *, query: str):
        """
        검색을 요청합니다.
        """
        print(query)
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))
        if embeds := await self.bot.mintchoco.search_embed(query):
            return await pagenator(self.bot, ctx, msg, embeds)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command(name="리스트")
    @commands.is_nsfw()
    async def _list(self, ctx: commands.Context, num: int = 1):
        """
        히토미에서 최근 올라온 한국어 작품을 가져옵니다.

        사용할 수 있는 값 : 페이지(입력하지 않을 경우 1)

        사용 예시 : ``&리스트`` 또는 ``&리스트 2``
        """
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))

        if embed := await self.bot.mintchoco.list_embed(num):
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
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))
        if embed := await self.bot.mintchoco.viewer_embed(index):
            await pagenator(self.bot, ctx, msg, embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))

    @commands.command("랭킹")
    @commands.is_nsfw()
    async def _ranking(self, ctx: commands.Context):
        """
        랭킹을 가져옵니다.
        """
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))

        if embed := await self.bot.mintchoco.count_embed():
            return await msg.edit(embed=embed)

        await msg.edit(embed=discord.Embed(title="정보를 찾지 못했습니다."))


def setup(bot: Hiyobot):
    bot.add_cog(Heliotrope(bot))
