import os
import json

languages = ['en', 'es']
translations = {}


def get_translations_file(file_name: str):
    return os.path.join(os.path.dirname(__file__), file_name)


for language in languages:
    with open(get_translations_file(f'{language}.json'), 'r') as file:
        translations[language] = json.load(file)

default_translations = translations['es']


def get_translations(lang):
    return translations.get(lang, default_translations)


def get_email_contents(lang, type: str):
    return get_translations(lang).get("emails").get(type, {
        "subject": "",
        "content": ""
    })
