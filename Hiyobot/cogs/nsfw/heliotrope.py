import os

import discord
from discord.ext import commands

from utils.pagenator import pagenator
from utils.rose_ext import RoseExt


class Heliotrope(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rose = RoseExt(os.environ["heliotrope_auth"])

    @commands.command(name="리스트")
    @commands.is_nsfw()
    async def _list(self, ctx: commands.Context, num: int = 1):
        """
        히토미에서 최근 올라온 한국어 작품을 가져옵니다.

        인자값: 페이지(기본값:1)

        사용법: ``&리스트`` ``&리스트 2``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요")
        )
        not_found = await self.rose.cache_list_embed(num)
        if not_found:
            await msg.edit(embed=not_found)
        await pagenator(self.bot, ctx, msg, self.rose.cache, "list_embed")

    @commands.command(name="번호")
    @commands.is_nsfw()
    async def _info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 히토미에서 해당 작품정보를 가져옵니다.

        인자값: 작품 번호(필수)

        사용법: ``&번호 1496588``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요")
        )
        embed = await self.rose.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="랜덤")
    @commands.is_nsfw()
    async def _random(self, ctx: commands.Context):
        """
        랜덤 으로 작품 정보 하나를 가져옵니다.

        인자값: 없음

        사용법: ``&랜덤``
        """
        msg: discord.Message = await ctx.send(
            embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요")
        )
        embed = await self.rose.random_embed()
        await msg.edit(embed=embed)

    # @commands.command(name="뷰어")
    # @commands.is_nsfw()
    # async def _viewer(self, ctx: commands.Context, index: int):
    #     """
    #     작품 번호를 입력하면 디스코드 내에서 보여줍니다.

    #     인자값: 작품 번호(필수)

    #     사용법: ``&뷰어 1496588``
    #     """
    #     msg: discord.Message = await ctx.send(
    #         embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요")
    #     )
    #     not_found = await self.rose.cache_viewer_embed(index, ctx.author.id)
    #     if not_found:
    #         await msg.edit(embed=not_found)
    #     await pagenator(self.bot, ctx, msg, self.rose.cache, "viewer_embed")


def setup(bot: commands.Bot):
    bot.add_cog(Heliotrope(bot))
