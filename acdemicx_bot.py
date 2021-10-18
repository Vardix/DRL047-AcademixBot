import logging
import time
import sys

import telebot
from telebot import types

import CONFIG

ENABLED_LANG = {
    'RU0': 'русский 0', 'RU1': 'русский 1', 'RU2': 'русский 2',
    # 'RU3', 'RU4', 'RU5',
    # 'RU6', 'RU7', 'RU8',
    # 'RU9', 'UA0', 'UA1',
}

COUNTRIES = {
    'RU': 'Россия',
    'UA': 'Украiна',
    'USA': 'USA'
}

ACCOUNT_INFO = {
    'country': 'Страна',
    'lang': 'Язык',  # ВЕРНУТЬ ЯЗЫК, НЕ КОД!
    'status': 'Учетная запись',
    # 'status': 'not_signed',
    'med_paper': 'Медицинская карта'
}

KEYBOARDS = {
    'lang': ENABLED_LANG,
    'country': COUNTRIES,
}

COMMANDS = {
    'start': 'Данная команда запускает бота и инициализирует стартовые процессы.',
    'help': 'Данная команда вызывает это меню.',
    'settings': 'Данная команда открывает настройки вашей учетной записи.',
    # 'start': '',
    # 'start': '',
}


logging.basicConfig(
    level=CONFIG.LOGGER_LEVEL,
    format="%(asctime)s [%(threadName)s] [%(funcName)s] [%(levelname)s]  %(message)s",
    filename=CONFIG.PATH_TO_LOG
)

bot = telebot.TeleBot(CONFIG.TOKEN)


@bot.message_handler(commands=COMMANDS.keys())
def commands(message):
    logging.info('User {0} (user id is {1}) send {2}.'.format(
        'None' if message.from_user.username is None else message.from_user.username,
        message.from_user.id,
        message.text
    ))

    if message.text == '/start':
        start_message = 'Добрый день, добро пожаловать.\n' \
                        'Выбреите пожалуйста язык:'

        # bot.send_message(message.from_user.id, 'first message')
        # bot.reply_to(message, start_message)

        bot.send_message(
            chat_id=message.chat.id,
            text=start_message,
            # reply_markup=make_lang_keyboard(),
            reply_markup=make_keyboard('lang'),
            parse_mode='HTML'
        )

        # bot.register_next_step_handler(message, choose_lang)

    elif message.text == '/help':
        help_message = 'Вы выбрали помощь. Список доступных команд:\n'
        for command in COMMANDS.keys():
            help_message += '/' + command + ' - ' + COMMANDS[command] + '\n'

        bot.reply_to(message, help_message)

    elif message.text == '/settings':
        # todo: запросы к базе для получения данных
        # страна
        # язык
        # статус аккаунта (логин/логофф)
        # успеваемость?
        # медкарта
        user_data = {
            'country': 'Россия',
            'lang': 'RU0',  # должен отдавать язык, не код языка
            'status': 'signed',
            # 'status': 'not_signed',
            'med_paper': 'Я даже не знаю, что здесь должно быть.'
        }
        settings_message = 'Информация о Вашем аккаунте.\n' \
                           'Для изменения параметра нажмите на него.'

        bot.send_message(
            chat_id=message.chat.id,
            text=settings_message,
            # reply_markup=make_lang_keyboard(),
            reply_markup=make_keyboard(user_data, 'account_info'),
            parse_mode='HTML'
        )
        pass

    else:
        text_message = 'Ты как сюда попал?'
        bot.send_message(
            chat_id=message.chat.id,
            text=text_message,
        )


# def choose_lang(message):
#     send_text = ''
#     bot.send_message(message.from_user.id, send_text)


def make_keyboard(kb_type, id_button=None):
    markup = types.InlineKeyboardMarkup()
    if isinstance(kb_type, str):
        for in_key in KEYBOARDS[kb_type].keys():
            # print(KEYBORDS[kb_type][in_key])
            # print("{0}:{1}".format(kb_type, in_key))
            markup.add(
                types.InlineKeyboardButton(
                    text=KEYBOARDS[kb_type][in_key],
                    callback_data="{0}:{1}".format(kb_type, in_key)
                ),
            )

    elif isinstance(kb_type, dict) and id_button == 'account_info':
        for in_key in kb_type.keys():
            # if in_key == 'lang':
            markup.add(
                types.InlineKeyboardButton(
                    text=ACCOUNT_INFO[in_key] + ' - ' + kb_type[in_key],
                    callback_data="{0}:{1}".format(id_button, in_key)
                ),
            )

    elif isinstance(kb_type, dict) and id_button is not None:
        for in_key in kb_type.keys():
            markup.add(
                types.InlineKeyboardButton(
                    text=kb_type[in_key],
                    callback_data="{0}:{1}".format(id_button, in_key)
                ),
            )

    temp_dict = dict()
    return markup


# def make_menu_keyboard():
#     keyword = 'home_menu'
#     markup = types.InlineKeyboardMarkup()
#     for lang in ENABLED_LANG.keys():
#         markup.add(
#             types.InlineKeyboardButton(
#                 text=ENABLED_LANG[lang],
#                 callback_data="{0}:{1}".format(keyword, lang)
#             ),
#         )
#
#     return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    logging.info('User {0} (user id is {1}) push {2} button.'.format(
        'None' if call.from_user.username is None else call.from_user.username,
        call.from_user.id,
        call.data
    ))

    if 'lang' in call.data:
        lang = call.data.split(':')[1]
        # TODO: сохранить языковую настройку сюда
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="Вы выбрали {0} язык.".format(ENABLED_LANG[lang]),
            message_id=call.message.message_id,
            reply_markup='',
        )

        # todo: проверка отправки согласия в базе
        # if soglasie_ne_polusheno:
        if True:
            text_message = 'Согласие на использование. Не согласны - не используйте.\n' \
                           'Счастья, здоровья и вообще всего доброго.'
            bot.send_message(call.from_user.id, text_message)

        pass

    elif 'account_info' in call.data:
        param = call.data.split(':')[1]
        # print(param)
        # todo: разбор настроек
        if param == 'country':
            change_country_message = 'Выберите страну:'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=change_country_message,
                message_id=call.message.message_id,
                reply_markup=make_keyboard('country'),
            )
        if param == 'lang':
            pass
        if param == 'status':
            pass
        if param == 'med_paper':
            pass

    elif 'country' in call.data:
        # todo: диалог сохранения и сохраение страны
        print(call.data)

    # print(call)
    # print(call.data)
    # print(type(call.data))


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
