import logging

from telegram.bot import Bot

from .. import config

logger = logging.getLogger(__name__)

bot = Bot(config.TELEGRAM_TOKEN)


def telegram_message(chat_id, message):
    return bot.send_message(chat_id, message)


def telegram_admin(message):
    return bot.send_message(config.MY_CHAT_ID, message)
