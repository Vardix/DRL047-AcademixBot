import json
import os


def get_all_locales(path_to_locales):
    all_in_directory = os.listdir(path_to_locales)
    locales = list()
    for name in all_in_directory:
        if '.json' in name:
            locales.append(name)
    return locales


def get_current_locale(path_to_locale):

    pass


if __name__ == '__main__':
    path = r'D:\projects\DRL047\locales'
    get_all_locales(path_to_locales=path)
    pass
