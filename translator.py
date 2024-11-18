import os
import re
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="auto", target="en")

project_path = '/Users/g_fediun/Projects/foodgram/frontend/src/'

string_pattern = re.compile(r'(["\'])(.*?)(["\'])')
jsx_pattern = re.compile(r'>\s*([^<{}]+?)\s*<')


def translate_text(match):
    original_string = match.group(2)

    if original_string.strip():
        translated_string = translator.translate(original_string)
        return f'{match.group(1)}{translated_string}{match.group(3)}'
    return match.group(0)


def translate_jsx_text(match):
    original_string = match.group(1)

    if original_string.strip():
        translated_string = translator.translate(original_string)
        return f'>{translated_string}<'
    return match.group(0)


for root, dirs, files in os.walk(project_path):
    for file in files:
        if file.endswith(('.js', '.jsx', '.html')):
            file_path = os.path.join(root, file)
            print(f"Translating {file}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            translated_content = re.sub(string_pattern, translate_text, content)
            translated_content = re.sub(jsx_pattern, translate_jsx_text, translated_content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)

            print(f"Finished translating {file}")

print("Translation completed.")
