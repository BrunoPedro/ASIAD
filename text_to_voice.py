from gtts import gTTS
import os
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

input_file = "demofile3.txt"
voice_file = input_file[:-4]+".mp3"

file = open(input_file, 'r', encoding='utf-8').read().replace("\n", " ")

language_code = detect(file)
print(f"Detected Language Code: {language_code}")

try:
    speech = gTTS(text=file, lang=language_code, slow=False)
    speech.save(voice_file)
    
    os.system(f"start {voice_file}")

except ValueError:
    print(f"The detected language '{language_code}' is not supported by gTTS.")
