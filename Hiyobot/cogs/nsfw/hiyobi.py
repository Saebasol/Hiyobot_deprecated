from utils.pagenator import pagenator
from utils.hiyobi import HiyobiExt
import discord
from discord.ext import commands


class Hiyobi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hiyobi = HiyobiExt()

    @commands.command(name="히요비리스트")
    async def _hiyobi_list(self, ctx, num: int = 1):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        not_found = await self.hiyobi.cache_list_embed(num)
        if not_found:
            await msg.edit(embed=not_found)
        await pagenator(self.bot, ctx, msg, self.hiyobi.cache, "hiyobi_list_embed")

    @commands.command(name="히요비정보")
    async def _hiyobi_info(self, ctx, index: int):
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        embed = await self.hiyobi.info_embed(index)
        await msg.edit(embed=embed)

    @commands.command(name="히요비검색")
    async def _hiyobi_search(self, ctx, *keyword):
        search = list(keyword)
        msg = await ctx.send(embed=discord.Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))
        not_found = await self.hiyobi.cache_search_embed(search)
        if not_found:
            await msg.edit(embed=not_found)
        await pagenator(self.bot, ctx, msg, self.hiyobi.cache, "hiyobi_search_embed")


def setup(bot):
    bot.add_cog(Hiyobi(bot))