import asyncio
import os
from utils.rose_ext import RoseExt
import discord
from discord.ext import commands


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rose = RoseExt(os.environ["heliotrope_auth"])

    @commands.command(name="가입")
    async def _register(self, ctx):
        embed = discord.Embed(
            title="개인정보 취급방침 및 약관",
            description="[Discord 지원 서버](https://discord.gg/PSshFYr)",
        )
        embed.add_field(
            name="개인정보 처리의 목적",
            value="히요봇(Hiyobot)은 다음 목적을 위하여 개인정보를 처리하고 있으며, 다음 목적 이외의 용도로는 사용하지 않습니다.\n\n다운로드 횟수 확인, 어뷰징을 하는 사용자 확인",
            inline=False,
        )
        embed.add_field(
            name="수집하는 개인정보 항목", value="디스코드 유저의 고유 ID, 유저의 특정 명령어 요청", inline=False
        )
        embed.add_field(
            name="개인정보 보유 및 이용기간",
            value="디스코드 고유 ID:서비스 종료시까지\n유저의 특정 명령어 요청 횟수:하루마다 초기화",
            inline=False,
        )
        embed.add_field(
            name="이용자 및 법정 대리인의 권리와 행사 방법",
            value="개발자는 정보통신망법 및 개인정보 보호법 등 관계 법령에서 규정하고 있는 이용자의 권리를 충실히 보장합니다.\n"
            "이용자는 언제든지 자신의 개인정보 및 이용 현황을 상시 확인할 수 있으며, 동의 철회 및 정정을 요청할 수 있습니다.",
            inline=False,
        )
        embed.add_field(
            name="개인정보의 파기",
            value="개인정보의 수집 및 이용 목적이 달성 되면, 수집한 개인정보를 신속하고 안전한 방법으로 파기합니다.",
            inline=False,
        )
        embed.add_field(
            name="개인정보 보호책임자",
            value="권리 침해와 개인정보 처리와 관한 불만처리 및 피해구제를 위하여 아래와 같이 개인정보보호 담당자를 지정하고 있습니다.\n\n개인정보 보호 책임자\n\n● 성명:류주헌\n● 직책:총개발자\n● 연락처:solo@doujinshiman.ga",
            inline=False,
        )
        embed.add_field(
            name="개인정보 처리방침 변경 시 고지 의무",
            value="개인정보 처리방침의 변경이 있는 경우 시행 7일 전에 이용자에게 고지합니다.",
            inline=False,
        )
        embed.add_field(
            name="약관 동의",
            value="이 봇을 사용함에 있어서 받는 불이익은 본인에게 있으며,\n개발자에게 책임을 물을 수 없습니다.\n동의하신다면 아래 이모티콘을 누르면 됩니다.",
            inline=False,
        )

        new = await self.rose.register_embed(ctx.author.id, True)

        if new:
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("\U00002705")
            await msg.add_reaction("\U0000274e")

            def check(reaction, user):
                return user == ctx.author and reaction.emoji in [
                    "\U00002705",
                    "\U0000274e",
                ]

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=30
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(title="시간 초과")
                return await msg.edit(embed=embed)
            else:
                if reaction.emoji == "\U0000274e":
                    return await msg.edit(embed=discord.Embed(title="취소하셨습니다."))

                else:
                    response = await self.rose.register_embed(ctx.author.id, False)
                    return await msg.edit(embed=response)
        else:
            return await ctx.send(embed=discord.Embed(title="이미 가입 되었습니다."))


def setup(bot):
    bot.add_cog(Register(bot))