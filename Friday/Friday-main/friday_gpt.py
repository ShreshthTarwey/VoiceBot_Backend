import speech_recognition as sr
from gtts import gTTS  # Google Text To speech 
import playsound
import os
import webbrowser   #to open external links
import wikipedia    # to link information 
import sys          # to system related tasks
import difflib      #difference and similarity
import pywhatkit as kit      #instantly sent msg on whatsapp and youtube
import datetime        #for date and time
import requests      #urls open krta h
import pyautogui       #system settings like mouse and keyboard control
import screen_brightness_control as sbc   #for brightness
# import smtplib
# from email.mime.text import MIMEText

weather_api = "a81ca8d6205343c43a0dc71253ba7ff9"  
weather_url = "https://api.openweathermap.org/data/2.5/weather?"
url = "https://openrouter.ai/api/v1/chat/completions"

def speak(text):                         
    print("Friday said:", text)     # whatever she speaks it will start with "friday said"
    tts = gTTS(text=text, lang="en", slow=False)
    filename = "her_voice.mp3"
    tts.save(filename)       # Make her_voice.mp3
    playsound.playsound(filename)  # play and run it
    os.remove(filename)      # after done , delete the file
    
recognizer = sr.Recognizer()
def listen():
    with sr.Microphone() as source:   # collects the input
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # enhance input
        recognizer.energy_threshold = 300  # to remove unwanted noise from input
        recognizer.dynamic_energy_threshold = False 

        audio = recognizer.listen(source)     # records my voice

        try:
            command = recognizer.recognize_google(audio, language="en-in")    # intakes my input and then recognize it
            print("Shivaji said:", command)
            return command.lower()
        except:
            speak("Sorry, I could not understand.")
            return ""
        
def myCommand(c):

    if "open settings" in c.lower():
        os.system("start ms-settings:")       #open setting
    elif "open file manager" in c.lower():
        os.system("explorer")                 #open file explorer

    elif "volume up" in c.lower():            #volume increase
        pyautogui.press("volumeup")
    elif "volume down" in c.lower():            #volume decrease
        pyautogui.press("volumedown")
    elif "chup ho ja" in c.lower():
        pyautogui.press("volumemute")           #mute

    elif "brightness up" in c.lower():
        sbc.set_brightness(min(sbc.get_brightness()[0] + 20, 100))   #brightness increase by 20%
    elif "brightness down" in c.lower():
        sbc.set_brightness(max(sbc.get_brightness()[0] - 20, 0))     #brightness decrease by 20%
    elif "brightness ful" in command.lower():
        sbc.set_brightness(100)                                     #full brightness
    elif "brightness zero" in command.lower():
        sbc.set_brightness(0)                                       #zero brightness

    elif "time" in c.lower():
        time = datetime.datetime.now().strftime("%H:%M %p")
        speak(f"Current time is {time}")                        #speaks time
    elif "date today" in c.lower():
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")                              #speaks day and date

    elif "open" in c.lower():
        topic = c.lower().replace("open", "").strip()        #if you say "open *****"
        speak(f"Opening {topic}")
        webbrowser.open(f"https://{topic}.com")           #open your **** in webbrowser


    elif "send message" in c.lower():
        speak("Kisko message bhejna hai?")                #person
        name = listen()
        speak("Message kya bheju?")                      #message
        msg = listen()
        kit.sendwhatmsg_instantly("+91**********", msg)       #instantly sends the message
        speak(f"Message sent to {name}")

    elif "weather" in c.lower():
        city = c.lower().replace("weather in", "").replace("what is the weather in", "").replace("weather", "").strip()
        if city == "":                             #if city is not definded
           city = "Faridabad"                      #then default city
        report = get_weather(city)
        speak(report)                              #speaks temp

    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "", 1).strip()  
        if song:  
           speak(f"Playing {song} on YouTube...")
           kit.playonyt(song)                    #play song on youtube
        else:
            speak("Boss, batao kaunsa gana play karna hai.")

    elif "my playlist" in c.lower():
            speak("opening your playlist")
            webbrowser.open("https://open.spotify.com/playlist/7LAjNHRgIIpuPXWrtbDJ21?si=X8t6bF_vQzq9AVHiVjJcMw")

    elif "google" in c.lower() or "search" in c.lower():
        speak("Kya Search Karu")    
        topic = listen()                                             # wait for your topic 
        webbrowser.open(f"https://www.google.com/search?q={topic}")
        speak(f"Here is what I found for {topic}")

    elif "information" in c.lower():
        speak("Kya Jan na hai apko?")
        topic = listen()
        try:
            info = wikipedia.summary(topic, sentences=2)       # search topic on wikipedia and summarize it upto 2 sentences 
            speak(info)
        except:
            speak("Sorry, I couldn't find anything on that.")

    elif "tum best ho" in c.lower():
        speak("Thank You , Ye mere boss ki vajah se hai")            # 😁😁     

    else:
        reply = chat_with_openrouter(command)                #otherwise text sent to gpt
        speak(reply)

def chat_with_openrouter(prompt):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",     #api and url of openrouter 
        headers={"Authorization": "Bearer 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",},
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are Friday, Shivaji's personal AI assistant."},      #gpt should act as
                {"role": "user", "content": prompt}]},          #command for gpt
        timeout=8)
    res = r.json()                            #responds to the output by gpt
    return res.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ No response")     #conversion and prints the output

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    res = requests.get(url).json()          #interpret in the app with the command
    if res.get("main"):                   #if city is present in app list
        temp = res["main"]["temp"]        #find its temp
        return f"{city.title()} ka temperature {temp}°C hai Boss"    #print temp along with its name
    return "Weather data nahi mila"
    
if __name__ == "__main__":
    speak("Activating Friday...")                     # Engine is heating up

    while True:
        try:
            with sr.Microphone() as source:           # listens to my voice
                print("Listening for wake word...")   # Wait for "Friday"
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)    # how much time it will listen and recognize the input
            word = recognizer.recognize_google(audio)  # Will Match the word
 
            if word.lower() == "friday":
                speak("Yes Boss")                       # Speak Yes boss , if true
                
                while True:
                    command = listen()                  # listen the command and give it to def function
                    if command != "":
                        myCommand(command)
        except Exception as e:                           # display error as "e" not show red error
            print("Error:", e)                          
