from os import getenv

from hiyobot.bot import run

if token := getenv("DISCORD_BOT_TOKEN"):
    run(token)
