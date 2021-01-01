import os
import sys

from Hiyobot.bot import bot, load_cogs

sys.path.append(os.path.abspath("Hiyobot"))


def test_load():
    failed = load_cogs(bot)
    assert len(failed) == 0
