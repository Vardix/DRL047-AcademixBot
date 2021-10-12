import os
import logging

import TOKEN


PATH = r'/Users/owl/Pycharm/PycharmProjects/DRL047-AcademixBot'
PATH_TO_LOG = os.path.join(PATH, 'log.log')
LOGGER_LEVEL = logging.DEBUG
OVERWRITE_LOG = False

TOKEN = TOKEN.TOKEN

if OVERWRITE_LOG:
    try:
        os.remove(PATH_TO_LOG)
    except FileNotFoundError:
        pass

