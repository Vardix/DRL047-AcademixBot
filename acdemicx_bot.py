import logging
import time
import sys
import random

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

LEARN = {
    'theory': 'Изучать в режиме теории.',
    'people_shuffle': 'Изучать пациентов в случайном порядке',
    'people_line': 'Изучать пациентов в прямом порядке',
}

KEYBOARDS = {
    'lang': ENABLED_LANG,
    'country': COUNTRIES,
    'learn': LEARN,
}

COMMANDS = {
    'start': 'Данная команда запускает бота и инициализирует стартовые процессы.',
    'learn': 'Изучение учебных материалов.',
    'support': 'Модуль для поддержки врачебных решений.',
    'assistant': 'Личный медицинский ассистент.',
    'help': 'Данная команда вызывает это меню.',
    'settings': 'Данная команда открывает настройки вашей учетной записи.',
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

    bot.delete_message(message.from_user.id, message.message_id)

    if message.text == '/start':
        start_message = 'Добрый день, добро пожаловать.\n' \
                        'Выбреите пожалуйста язык:'

        bot.send_message(
            chat_id=message.chat.id,
            text=start_message,
            # reply_markup=make_lang_keyboard(),
            reply_markup=make_keyboard('lang'),
            parse_mode='HTML'
        )

    elif message.text == '/help':
        help_message = 'Вы выбрали помощь. Список доступных команд:\n'
        for command in COMMANDS.keys():
            help_message += '/' + command + ' - ' + COMMANDS[command] + '\n'

        # bot.reply_to(message, help_message)
        bot.send_message(
            chat_id=message.chat.id,
            text=help_message,
        )

    elif message.text == '/settings':
        # todo: запросы к базе для получения данных
        user_data = {
            'country': 'Russia',
            'lang': 'RU0',  # должен отдавать язык, не код языка
            'status': 'signed',
            # 'status': 'not_signed',
            'med_paper': 'Med map'
        }
        settings_message = 'Информация о Вашем аккаунте.\n' \
                           'Для изменения параметра нажмите на него.'

        bot.send_message(
            chat_id=message.chat.id,
            text=settings_message,
            reply_markup=make_keyboard(user_data, 'account_info'),
            parse_mode='HTML'
        )

    elif message.text == '/learn':
        # todo: запросы к базе для получения данных
        learn_message = 'Выберите режим изучения:'
        bot.send_message(
            chat_id=message.chat.id,
            text=learn_message,
            reply_markup=make_keyboard('learn'),
            parse_mode='HTML'
        )
        pass

    elif message.text == '/support':
        # todo: как оно вообще должно работать?
        support_message = 'Доступ к модулю находиться в разработке.\n' \
                          'Зайдите позже.'
        # bot.reply_to(message, support_message)
        bot.send_message(
            chat_id=message.chat.id,
            text=support_message,
        )

    elif message.text == '/assistant':
        # todo: проверка регистрации пользователя
        # if unauthorized_user:
        # todo: убрать рандом и модуль сверху
        bot.send_message(
            chat_id=message.chat.id,
            text='Just for fun проверка авторизации привязаан к рандому. Нужен другой варинат - попробуйте еще раз.'
        )
        if random.randint(0, 1):
            assistant_pls_register = 'Вы не авторизованы, пожалуйста авторизуйтесь.'
            # bot.reply_to(message, assistant_pls_register)
            bot.send_message(
                chat_id=message.chat.id,
                text=assistant_pls_register,
            )
            link_to_another_service = '!Ссылка для авторизаци:\n' \
                                      'any_think.com'
            bot.send_message(
                chat_id=message.chat.id,
                text=link_to_another_service
            )
        else:
            assistant_message = 'Вы авторизованы, но модуль еще в разработке.'
            # bot.reply_to(message, assistant_message)
            bot.send_message(
                chat_id=message.chat.id,
                text=assistant_message,
            )
        pass

    else:
        text_message = 'Ты как сюда попал?'
        bot.send_message(
            chat_id=message.chat.id,
            text=text_message,
        )


@bot.message_handler()
def return_help(message):
    logging.info('User {0} (user id is {1}) send {2}.'.format(
        'None' if message.from_user.username is None else message.from_user.username,
        message.from_user.id,
        message.text
    ))

    after_query_message = 'Для вызова помощи используйте команду /help.'
    bot.send_message(message.from_user.id, after_query_message)
    # bot.send_message(message.from_user.id, 'Я поймал какое-то ваше сообщение. '
    #                                        'Не волнуйтесь, все будет записано.\n/help для помощи.')


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
                    callback_data="{0}:{1}:{2}".format(id_button, in_key, kb_type[in_key])
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

    # temp_dict = dict()
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handler_query(call):

    logging.info('User {0} (user id is {1}) push {2} button.'.format(
        'None' if call.from_user.username is None else call.from_user.username,
        call.from_user.id,
        call.data
    ))

    if 'lang' in call.data:
        lang = call.data.split(':')[-1]
        # TODO: сохранить языковую настройку сюда
        print(182, lang)
        # print(lang)
        confirmed_lang_message = "Вы выбрали {0} язык.".format(ENABLED_LANG[lang])
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=confirmed_lang_message,
            message_id=call.message.message_id,
            reply_markup='',
        )

        # todo: проверка отправки согласия в базе
        # if soglasie_ne_polusheno:
        if True:
            concept_message = 'Согласие на использование. Не согласны - не используйте.\n' \
                                'Счастья, здоровья и вообще всего доброго.\n' \
                                '\nДля вызова помощи испльзуйте команду /help.'
            bot.send_message(call.from_user.id, concept_message)

    elif 'account_info' in call.data:
        params = call.data.split(':')
        first_param, second_param = params[1], params[2]
        # print(param)
        # todo: разбор настроек
        if first_param == 'country':
            change_country_message = 'Выберите страну:'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=change_country_message,
                message_id=call.message.message_id,
                reply_markup=make_keyboard('country'),
            )
        if first_param == 'lang':
            change_language_message = 'Выберите язык:'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=change_language_message,
                message_id=call.message.message_id,
                # reply_markup=make_lang_keyboard(),
                reply_markup=make_keyboard('lang'),
                parse_mode='HTML'
            )
        if first_param == 'status':
            # todo: login/logout
            change_status_message = 'Тут должен быть вход/выход, но у меня нет данных.'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=change_status_message,
                message_id=call.message.message_id,
                # reply_markup=make_lang_keyboard(),
                reply_markup='',
            )
        if first_param == 'med_paper':
            # todo: login/logout для медицинской карты
            change_medicalcard_message = 'Тут должно быть отображение медкарты, но у меня нет данных.'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=change_medicalcard_message,
                message_id=call.message.message_id,
                # reply_markup=make_lang_keyboard(),
                reply_markup='',
            )

    elif 'country' in call.data:
        param = call.data.split(':')[1]
        # todo: сохраение страны
        country_message = 'Страна {0} для вашего аккаунта установлена.'
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            text=country_message.format(COUNTRIES[param]),
            message_id=call.message.message_id,
            reply_markup='',
        )

    elif 'learn' in call.data:
        # todo: реим изучения
        param = call.data.split(':')[1]
        if param == 'theory':
            learn_theory_message = 'Вы выбрали режим изучения теории.' \
                                   '\nДальнейшая часть находиться в разработке.'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=learn_theory_message,
                message_id=call.message.message_id,
                reply_markup='',
            )
        elif param == 'people_shuffle':
            # todo: вот тут-то и пригодиться randint
            learn_people_shuffle_message = 'Вы выбрали режим изучения случайных пациаентов.' \
                                   '\nДальнейшая часть находиться в разработке.'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=learn_people_shuffle_message,
                message_id=call.message.message_id,
                reply_markup='',
            )
        elif param == 'people_line':
            learn_people_line_message = 'Вы выбрали режим изучения линейных (?) пациентов.' \
                                   '\nДальнейшая часть находиться в разработке.'
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=learn_people_line_message,
                message_id=call.message.message_id,
                reply_markup='',
            )
        pass

    # elif 'med_paper' in call.data:
    #     med_paper = 'Вы открыли медицинскую карту, но она не открылась.'
    #     bot.edit_message_text(
    #         chat_id=call.message.chat.id,
    #         text=med_paper,
    #         message_id=call.message.message_id,
    #         reply_markup='',
    #     )

    # print(call)
    print('255', call.data)
    # print(type(call.data))


# def choose_lang(message):
#     send_text = ''
#     bot.send_message(message.from_user.id, send_text)


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
