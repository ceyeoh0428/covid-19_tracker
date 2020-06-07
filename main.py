import pyttsx3
import speech_recognition as sr

import re
from data import Data

API_KEY = 'tvgybGbTX8ZK'
PROJECT_TOKEN = 'taXuH9Wyd9tO'
RUN_TOKEN = 't72OZhtW8Ypg'


# pyttsx3 speak not working
def speak(text):
    engine = pyttsx3.init('dummy')
    engine.say(text)
    engine.runAndWait()
# speak('Hello')


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('Exception', str(e))
    return said.lower()


def main():
    data = Data(API_KEY, PROJECT_TOKEN)
    print('Program Is Running')
    END_PHRASE = 'stop'
    country_list = data.get_country_list()
    #[\w\s]+ cannot have space!!!
    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ death"): data.get_total_death,
        re.compile("[\w\s]+ total death"): data.get_total_death
    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases in [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ death in [\w\s]+"): lambda country: data.get_country_data(country)['total_death'],
    }

    UPDATE_COMMANDS = 'update'

    while True:
        print('Listening...')
        text = get_audio()
        # text = 'what is the total cases in malaysia'
        print(text)
        result = None

        for pat, func in COUNTRY_PATTERNS.items():
            if pat.match(text):
                words = text.split(' ')
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

        for pat, func in TOTAL_PATTERNS.items():
            if pat.match(text):
                result = func()
                break

        if text == UPDATE_COMMANDS:
            result = 'data is being updating'
            data.update_data()

        if result:
            print(result)
        # break

        # stop loop
        if text.find(END_PHRASE) != -1:
            print('thank you')
            break


main()
# 6 June 2020, 4.33PM
# 6,861,716 cases in the world
# 398,483 death in the world
# 8,266 cases in Malaysia
# 116 death in Malaysia

# 6 June 2020, 9.54PM
# 6,885,114 cases in the world

# 6 June 2020, 9.57PM
# 6,885,120 cases in the world

# 7 June 2020, 2.00PM
# 6,982,883 cases in the world
# 402,273 death in the world
# 8,303 cases in Malaysia
# 117 death in Malaysia
