import asyncio
import re

import aiohttp
import discord
from discord.ext import commands

from Hiyobot.bot import Hiyobot


class Auth(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="api")
    async def _api(self, ctx: commands.Context, *purpose):
        if not purpose:
            return await ctx.send("사용할 목적을 적어주셔야해요!")
        async with aiohttp.ClientSession(
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"token {self.bot.github_token}",
            }
        ) as cs:
            async with cs.post(
                "https://doujinshiman.ga/v3/api/register",
                json={"user_id": ctx.author.id},
                headers={"Verification": f"check {self.bot.verify}"},
            ) as res:
                if res.status == 200:
                    r = await res.json()
                    return await ctx.send(
                        f"이미 등록되어있어요: ``{r['api_key']}``", delete_after=10
                    )
            async with cs.get(
                f"https://api.github.com/repos/Saebasol/register/issues"
            ) as r:
                response = await r.json()
                for body in response:
                    if ctx.author.id == int(
                        re.findall(r"user id: ``(.+?)``", str(body["body"]))[0]
                    ):
                        msg = await ctx.send(
                            embed=discord.Embed(title="이미 요청하셨네요. 기존 요청을 취소할까요?")
                        )
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❎")
                        try:
                            reaction, user = await self.bot.wait_for(
                                "reaction_add",
                                check=lambda reaction, user: (user.id == ctx.author.id)
                                and (reaction.emoji in ["✅", "❎"])
                                and (reaction.message.id == msg.id),
                                timeout=30,
                            )
                        except asyncio.TimeoutError:
                            return await msg.edit(
                                embed=discord.Embed(title="시간이 만료됬어요")
                            )
                        else:
                            if reaction.emoji == "❎":
                                return await msg.edit(
                                    embed=discord.Embed(title="취소 되었어요")
                                )
                            else:
                                async with cs.patch(
                                    body["url"], json={"state": "closed"}
                                ) as r:
                                    if r.status == 200:
                                        response = await r.json()
                                        return await msg.edit(
                                            embed=discord.Embed(
                                                title="성공적으로 요청했어요.",
                                                description=f"[이곳]({response['html_url']})에서 확인하실수 있을거에요.",
                                            )
                                        )

            msg = await ctx.send(
                embed=discord.Embed(
                    title="⚠️경고! 해당 명령어는 개발자전용 명령어 입니다.",
                    description="실행시 디스코드의 닉네임, 생성일, 유저 아이디가 전송됩니다.\n계속하시겠습니끼?",
                    color=discord.Color.red(),
                )
            )
            await msg.add_reaction("✅")
            await msg.add_reaction("❎")
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: (user.id == ctx.author.id)
                    and (reaction.emoji in ["✅", "❎"])
                    and (reaction.message.id == msg.id),
                    timeout=30,
                )
            except asyncio.TimeoutError:
                return await msg.edit(embed=discord.Embed(title="시간이 만료됬어요"))
            else:
                if reaction.emoji == "❎":
                    return await msg.edit(embed=discord.Embed(title="취소 되었어요"))

            json = {
                "title": f"{ctx.author} has requested to use the Heliotrope",
                "body": f"""
# The information is as follows

name: ``{ctx.author}``

user id: ``{ctx.author.id}``

created_at: ``{ctx.author.created_at}``

purpose: ``{' '.join(purpose)}``

Request to use API, so please approve it.
""",
            }
            async with cs.post(
                f"https://api.github.com/repos/Saebasol/register/issues",
                json=json,
            ) as r:
                if r.status != 201:
                    return await msg.edit(
                        embed=discord.Embed(title="생성중 문제가 발생한거 같아요.")
                    )
                else:
                    response = await r.json()
                    await msg.edit(
                        embed=discord.Embed(
                            title="성공적으로 요청했어요.",
                            description=f"[이곳]({response['html_url']})에서 확인하실수 있을거에요.",
                        )
                    )


def setup(bot: Hiyobot):
    bot.add_cog(Auth(bot))
