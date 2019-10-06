import logging

from telegram.bot import Bot

from .. import config

logger = logging.getLogger(__name__)

bot = Bot(config.TELEGRAM_TOKEN)


def send_message(chat_id, text):
    return bot.send_message(chat_id, text)


def send_me(text):
    return bot.send_message(config.MY_CHAT_ID, text)
