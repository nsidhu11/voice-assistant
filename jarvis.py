
import datetime
from pydoc import Doc
import pyttsx3
import speech_recognition as sr 
import pyaudio
import wikipedia as wp
import webbrowser
import os, sys, subprocess
import smtplib, ssl
import json
import spotipy

# sapi5 - SAPI5 on Windows
# nsss - NSSpeechSynthesizer on Mac OS X
# espeak - eSpeak on every other platform
engine =pyttsx3.init('nsss')

# checking the different voices and printing them
voices=engine.getProperty('voices')

# List of voices in nsss - NSSpeechSynthesizer
# index name gender age
# 0 Alex VoiceGenderMale 35
# 1 Alice VoiceGenderFemale 35
# 2 Alva VoiceGenderFemale 35
# 3 Amelie VoiceGenderFemale 35
# 4 Anna VoiceGenderFemale 35
# 5 Carmit VoiceGenderFemale 35
# 6 Damayanti VoiceGenderFemale 35
# 7 Daniel VoiceGenderMale 35
# 8 Diego VoiceGenderMale 35
# 9 Ellen VoiceGenderFemale 35
# 10 Fiona VoiceGenderFemale 35
# 11 Fred VoiceGenderMale 30
# 12 Ioana VoiceGenderFemale 35
# 13 Joana VoiceGenderFemale 35
# 14 Jorge VoiceGenderMale 35
# 15 Juan VoiceGenderMale 35
# 16 Kanya VoiceGenderFemale 35
# 17 Karen VoiceGenderFemale 35
# 18 Kyoko VoiceGenderFemale 35
# 19 Laura VoiceGenderFemale 35
# 20 Lekha VoiceGenderFemale 35
# 21 Luca VoiceGenderMale 35
# 22 Luciana VoiceGenderFemale 35
# 23 Maged VoiceGenderMale 35
# 24 Mariska VoiceGenderFemale 35
# 25 Mei-Jia VoiceGenderFemale 35
# 26 Melina VoiceGenderFemale 35
# 27 Milena VoiceGenderFemale 35
# 28 Moira VoiceGenderFemale 35
# 29 Monica VoiceGenderFemale 35
# 30 Nora VoiceGenderFemale 35
# 31 Paulina VoiceGenderFemale 35
# 32 Rishi VoiceGenderMale 35
# 33 Samantha VoiceGenderFemale 35
# 34 Sara VoiceGenderFemale 35
# 35 Satu VoiceGenderFemale 35
# 36 Sin-ji VoiceGenderFemale 35
# 37 Tessa VoiceGenderFemale 35
# 38 Thomas VoiceGenderMale 35
# 39 Ting-Ting VoiceGenderFemale 35
# 40 Veena VoiceGenderFemale 35
# 41 Victoria VoiceGenderFemale 35
# 42 Xander VoiceGenderMale 35
# 43 Yelda VoiceGenderFemale 35
# 44 Yuna VoiceGenderFemale 35
# 45 Yuri VoiceGenderMale 35
# 46 Zosia VoiceGenderFemale 35
# 47 Zuzana VoiceGenderFemale 35



#  setting the desired voice 
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishMe():
    hour=int(datetime.datetime.now().hour)
    
    if hour>=0 and hour<12:
        speak("Good Morning!")    
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!") 
    
    # speak("Hi Nav, Welcome to jarvis project")


def takeCommand():
    #takes audio input from the used and convert it to string
    
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
    try: 
        print("Recognizing...")
        query=r.recognize_google(audio)
        print(f"User said:{query}\n")
    except Exception as e:
        # print (e)
        print("Say that again please...")
        return "None"
    
    return query

def playSpotify():
    username = '6lxwnrth4scgqknfxmdmjhz8b'
    clientID = 'bc089ca65a7e4a5fad5157fd79f7794c'
    clientSecret = '68daa938ba3f4216a85ba631496c32fd'
    redirect_uri = 'http://google.com/callback/'
 
    try:
        oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
        token_dict = oauth_object.get_access_token()
        token = token_dict['access_token']
        spotifyObject = spotipy.Spotify(auth=token)
        user_name = spotifyObject.current_user()
        print(json.dumps(user_name, sort_keys=True, indent=4))
        speak("Welcome to Spotify. What you would like to listen.")
        search_song = takeCommand().lower()
        results = spotifyObject.search(search_song, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song = song_items[0]['external_urls']['spotify']
        speak(f"Playing your song in browser")
        webbrowser.open(song)
        speak("Thank you for visiting spotify")
    except Exception as e:
        print(e)
        speak("Sorry! Cann't play your music.")

def openApp():
    speak("Which application you would like to open")
    appName=takeCommand().lower()
    os.system(f"open /Applications/{appName}.app ")
    speak(f"Opening {appName}")
    
def sendEMail():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    speak("Please Enter your email address and press enter.")
    sender_email = input("Please Enter your email address and press enter")  # Enter your address
    speak("Please enter the recievers email address and press enter")
    receiver_email = input("Please enter the recievers email address and press enter") # Enter receiver address
    speak("Type your password and press enter ")
    password = input("Type your password and press enter: ")
    speak("What you would like to send")
    message = takeCommand()
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        speak("Email Sent.")
    except Exception as e:
        print(e)
        speak("Sorry, I'm not able to send you email.")
        
    
           
    
if __name__=="__main__":
    wishMe()
    while 1:
        query=takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query=query.replace("wikipedia","")
            results=wp.summary(query,sentences=2)
            speak("According to wikipedia")
            speak(results)
        if 'open youtube' in query:
            webbrowser.get("safari").open("https://www.youtube.com/")
        if 'open stackoverflow' in query:
            webbrowser.get("safari").open("https://stackoverflow.com/")
        if 'open google' in query:
            webbrowser.get("safari").open("https://google.com/")
        if 'play music' in query:
            playSpotify()
        if "the time" in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        if "open application" in query:
            openApp()
        if "send email" in query:
            sendEMail()
           
                        

            
            
            
            
        
    
    
    
