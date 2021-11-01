import json
import os


def get_locale_names(path_to_locales):
    all_in_directory = os.listdir(path_to_locales)
    locales = list()
    for name in all_in_directory:
        if '.json' in name:
            locales.append(name)
    return locales


def get_all_locales_data(path_to_locale, locale_names):

    locales = dict()

    for locale_file_name in locale_names:
        locale_full_path = os.path.join(path_to_locale, locale_file_name)
        with open(locale_full_path, 'r', encoding='utf-8') as file:
            locale_data = json.load(file)
            locales[locale_file_name.replace('.json', '')] = locale_data

    return locales


if __name__ == '__main__':
    path = r'D:\projects\DRL047\locales'
    loc_names = get_locale_names(path_to_locales=path)
    loc_data = get_all_locales_data(path_to_locale=path, locale_names=loc_names)

    pass
