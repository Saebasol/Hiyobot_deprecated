import asyncio

import discord


async def pagenator(bot, ctx, msg, cache_class, list_name):
    num = 0
    embed_list = await cache_class.get(list_name)

    total = len(embed_list)

    def check(reaction: discord.Reaction, user: discord.User):
        return (user.id == ctx.author.id) and (reaction.emoji in ["▶", "◀", "❎"])

    await msg.edit(embed=embed_list[num])
    await msg.add_reaction(emoji="❎")
    await msg.add_reaction("◀")
    await msg.add_reaction("▶")

    async def pass_permission_error(msg, emoji, author):
        try:
            await msg.remove_reaction(emoji, author)
        except:
            pass

    while True:
        try:
            reaction, user = await bot.wait_for(
                event="reaction_add", check=check, timeout=80.0
            )
            if user.id != ctx.author.id or reaction.message.id != msg.id:
                continue

        except asyncio.TimeoutError:
            await cache_class.clear()
            await msg.clear_reactions()
            return

        else:
            if reaction.emoji == "❎":
                await cache_class.clear()
                await msg.clear_reactions()
                return

            elif reaction.emoji == "▶":

                total = total

                num += 1

                if num > total - 1:
                    num = 0

                await msg.edit(embed=embed_list[num])
                await pass_permission_error(msg, "▶", ctx.author)

            elif reaction.emoji == "◀":

                total = total

                num -= 1
                if num < 0:
                    num = total - 1

                await msg.edit(embed=embed_list[num])
                await pass_permission_error(msg, "◀", ctx.author)
