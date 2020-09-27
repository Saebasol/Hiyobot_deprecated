import os
from utils.pagenator import pagenator
from utils.rose_ext import RoseExt
import discord
from discord.ext import commands


class Heliotrope(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rose = RoseExt(os.environ["heliotrope_auth"])

    @commands.command(name="리스트")
    async def _list(self, ctx, num: int = 1):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        not_found = await self.rose.cache_list_embed(num)
        if not_found:
            await msg.edit(embed=not_found)
        await pagenator(self.bot, ctx, msg, self.rose.cache, "list_embed")

    @commands.command(name="정보")
    async def _info(self, ctx, index: int):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        embed = await self.rose.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="뷰어")
    async def _viewer(self, ctx, index: int):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        not_found = await self.rose.cache_viewer_embed(index)
        if not_found:
            await msg.edit(embed=not_found)
        await pagenator(self.bot, ctx, msg, self.rose.cache, "viewer_embed")

    @commands.command(name="다운로드")
    async def _download(self, ctx, index: int):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        embed = await self.rose.download_embed(ctx.author.id, index)
        await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Heliotrope(bot))