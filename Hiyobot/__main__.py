import os

from Hiyobot.bot import bot, load_cogs

load_cogs(bot)
bot.run(os.environ["token"])
