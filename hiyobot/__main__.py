import os

from Hiyobot.bot import bot, load_cogs

load_cogs(bot)

if token := os.environ.get("token"):
    bot.run(token)
