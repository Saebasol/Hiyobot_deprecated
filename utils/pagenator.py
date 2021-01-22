import asyncio
from contextlib import suppress

import discord
from discord.embeds import Embed
from discord.ext.commands.context import Context
from discord.message import Message

from Hiyobot.bot import Hiyobot


async def pagenator(
    bot: Hiyobot,
    ctx: Context,
    msg: Message,
    embed_list: list[Embed],
):
    num = 0

    total = len(embed_list)

    def check(reaction: discord.Reaction, user: discord.User):
        return (user.id == ctx.author.id) and (reaction.emoji in ["▶", "◀", "❎"])

    await msg.edit(embed=embed_list[num])
    await msg.add_reaction("❎")
    await msg.add_reaction("◀")
    await msg.add_reaction("▶")

    async def pass_permission_error(msg: discord.Message, emoji, author):
        with suppress(Exception):
            await msg.remove_reaction(emoji, author)

    while not bot.is_closed():
        try:
            reaction, user = await bot.wait_for(
                event="reaction_add", check=check, timeout=80.0
            )
            if user.id != ctx.author.id or reaction.message.id != msg.id:
                continue

        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        if reaction.emoji == "❎":
            await msg.clear_reactions()
            return

        elif reaction.emoji == "▶":
            num += 1

            if num > total - 1:
                num = 0

            await msg.edit(embed=embed_list[num])
            await pass_permission_error(msg, "▶", ctx.author)

        elif reaction.emoji == "◀":
            num -= 1
            if num < 0:
                num = total - 1

            await msg.edit(embed=embed_list[num])
            await pass_permission_error(msg, "◀", ctx.author)
