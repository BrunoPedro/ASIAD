import googletrans
from googletrans import Translator

def translate_text_file(input_file, output_file, dest_lang='pt'):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = []

    for line in lines:
        detected = translator.detect(line.strip())
        source_lang = detected.lang

        translation = translator.translate(line.strip(), src=source_lang, dest=dest_lang)
        translated_lines.append(translation.text)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(translated_lines))

    print(f"Translation saved to {output_file}")

file_to_translate = "demofile3.txt"
translated_file = file_to_translate[:-4]+"_pt-PT.txt"
translate_text_file(file_to_translate, translated_file, dest_lang='pt')