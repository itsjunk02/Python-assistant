from email import message
from http import server
import pyttsx3  # text to speech
import datetime
import speech_recognition as sr
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import clipboard
import os
import pyjokes
import time as tt
import psutil
from nltk.tokenize import word_tokenize
import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

engine = pyttsx3.init()  # initial function
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 210)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("The current date is : ")
    speak(date)
    speak(month)
    speak(year)


def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")


def wishme():
    greeting()
    speak("Welcome back!")
    speak("How may I help you?")


# wishme()
def takeCommandCMD():
    query = input("How may I help you?\n")
    return query


def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query

# def ask():
    
#     user_query = takeCommandMic().lower

#     URL = "https://www.google.co.in/search?q=" + user_query

#     headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
#     }

#     page = requests.get(URL, headers=headers)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     result = soup.find(class_='Z0LcW XcVN5d').get_text()
#     print(result)


def sendwhatsmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone=' +
            phone_no + '&text='+Message)
    sleep(10)
    pyautogui.press('enter')


def searchgoogle():
    speak("What should I search for?")
    search = takeCommandMic()
    wb.open('https://www.google.com/search?q='+search)


def searchwiki():
    speak("Which section should I search for on Wikipedia?")
    sea = takeCommandMic()
    cachedStopWords = stopwords.words("english")
    sea = ' '.join([word for word in sea.split() if word not in cachedStopWords])
    wb.open('https://en.wikipedia.org/wiki/'+sea)


def news():
    newsapi = NewsApiClient(api_key='1d5332f32913425ebfaf3f86becf7de0')
    speak("What topic do you need the news about?")
    topic = takeCommandMic()
    data = newsapi.get_top_headlines(q=topic,
                                     language='en',
                                     page_size=5)
    newsdata = data['articles']
    for x, y in enumerate(newsdata):
        print(f'{x}.) {y["description"]}')
        speak((f'{x}.) {y["description"]}'))

    speak("That is it for now, I will update you in some time")


def seltxt2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


def screenshot():
    name_img = tt.time()
    name_img = f'C:\\Users\\ADMIN\\Downloads\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()


def cpuUsage():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)


if __name__ == "__main__":  # main function
    wishme()

    while True:
        query = takeCommandMic().lower()
        query = word_tokenize(query)
        print(query)

        if 'date' in query:
            date()

        elif 'message' in query:
            user_name = {
                'Sanjeev': '+91 91523 98442'
            }
            try:
                speak("To whom do you want to send the Whatsapp message?")
                name = takeCommandMic()
                phone_no = user_name[name]
                speak("What is the message?")
                message = takeCommandMic()
                sendwhatsmsg(phone_no, message)
                speak("Message has been sent")
            except Exception as e:
                print(e)
                speak("Unable to send the message")

        elif 'wikipedia' in query:
            speak("Searching on wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)

        elif 'search' in query:
            searchgoogle()

        elif 'youtube' in query:
            speak("What should I search for on Youtube?")
            topic = takeCommandMic()
            pywhatkit.playonyt(topic)

        elif 'news' in query:
            news()

        elif 'read' in query:
            seltxt2speech()

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'screenshot' in query:
            screenshot()
            speak("Done!")

        elif 'section' in query:
            searchwiki()

        elif 'cpu' in query:
            cpuUsage()

        elif 'offline' in query:
            quit()
