import logging
import time
import sys

import telebot
from telebot import types

import CONFIG


logging.basicConfig(
    level=CONFIG.LOGGER_LEVEL,
    format="%(asctime)s [%(threadName)s] [%(funcName)s] [%(levelname)s]  %(message)s",
    filename=CONFIG.PATH_TO_LOG
)

bot = telebot.TeleBot(CONFIG.TOKEN)


@bot.message_handler(commands=[
    'start', 'help',
])
def commands(message):
    logging.info('User {0} (user id is {1}) send {2}.'.format(
        'None' if message.from_user.username is None else message.from_user.username,
        message.from_user.id,
        message.text
    ))

    if message.text == '/start':
        start_message = 'Добрый день, добро пожаловать.'

        # bot.send_message(message.from_user.id, 'first message')
        bot.reply_to(message, start_message)
    elif message.text == '/help':
        help_message = 'Вы выбрали помощь.'

        bot.reply_to(message, help_message)


def main_loop():
    bot.polling(True)
    while True:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info('\nExiting by user request.\n')
        sys.exit(0)
