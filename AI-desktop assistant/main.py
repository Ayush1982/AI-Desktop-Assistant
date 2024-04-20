import speech_recognition as sr
import os
import webbrowser
import google.generativeai as genai
import datetime
import random
import pyttsx3
from pocketsphinx import LiveSpeech, get_model_path
import speech_recognition as sr
import urllib.parse
import json
import re
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("key")

chatStr = ""

def chat(text):
    global chatStr
    chatStr += f"User: {text}\n  AI:"
    temp_response = AI(chatStr)
    chatStr += f"{temp_response}\n"
    print(chatStr)
    say(temp_response)
    return temp_response

def helper(promt):
    
    text_temp = f"Responce for :{promt} \n**************************** \n\n"
    temp_response = AI(text_temp)
    print(temp_response)
    text = text_temp+temp_response
    if not os.path.exists("AI_output"):
        os.mkdir("AI_output")
    with open(f"AI_output/promt- {''.join([str(random.randint(0, 9)) for _ in range(random.randint(10, 15))])}", "w") as f:
        f.write(text)
    
    say(temp_response)
    return temp_response

def AI(text_temp):

    genai.configure(api_key=key)

    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config = generation_config , safety_settings = safety_settings)# type: ignore
    
    prompt_parts = [
        "input: ",
        "output: ",
    ]

    response = model.generate_content(text_temp)
    return (response.text)
    

def open_application(app_name):
    say(f"Opening the {app_name}")
    print(f"Opening the {app_name}")
    os.system("start " + app_name)
    return None
    
def load_websites_from_file(filename):
    with open(filename, 'r') as file:
        websites = json.load(file)
    return websites

def get_url_by_name(name, websites):
    for website in websites:
        if website["name"].lower() == name.lower():
            return website["url"]
    return None

def remove_word(string, word):
    pattern = r'\b' + re.escape(word) + r'\b'
    cleaned_string = re.sub(pattern, '', string)
    return cleaned_string.strip()


def search(text):
    query = urllib.parse.quote_plus(text)
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    print(f"AI : Searching for '{text}' on Google...")
    return None


def textcommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.6
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recognizing...")

        try:
            text = recognizer.recognize_google(audio)  # type: ignore
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            print("Sorry, couldn't request results from Google Speech Recognition service.")
            return None


def say(text):
    engine = pyttsx3.init()
    engine.say(f"AI :{text}")
    engine.runAndWait()
    return None

if __name__ == '__main__':
    print("---starting----")

    while True:
        query = textcommand()
        websites = load_websites_from_file('websites.json')
 
        if query:

            if "what is the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"Sir, the current time is {strfTime}")
                say(f"Sir, the current time is {strfTime}")

            elif "search" in query.lower():
                query_temp = remove_word(query, "search")
                search(query_temp)
                #continue

            elif "open app" in query.lower():
                query_temp = remove_word(query, "open app")
                open_application(f"{query_temp}.exe")
                exit(1)
        
            elif "open music" in query.lower():
                query_temp = remove_word(query, "open music")
                path = r"\music" + f"\{query_temp}" + ".mp3" # type: ignore
                os.startfile(path)
                #continue

            elif "open video" in query.lower():
                query_temp = remove_word(query, "open video")
                path = r"\video" + f"\{query_temp}" + ".mp4" # type: ignore
                os.startfile(path)
                #continue
        
            elif "help" in query.lower():
                print("AI: Helping you sir...")
                helper(query)
                #continue
        
            elif "tell" in query.lower():
                print("AI: Helping you sir...")
                helper(query)
                #continue

            elif "open" in query.lower():
                query_temp = remove_word(query, "open")
                sites = get_url_by_name(query_temp, websites)

                if sites:
                    print("AI: URL:", sites)
                    say(f"Opening {sites} sir...")
                    webbrowser.open(sites)
                    #continue
                
                else:
                    print("AI: Website not found.")
                    #continue
        
            elif "shut down" in query.lower():
                print("AI: Shutting down...")
                say("shutting down")
                os.system("shutdown /s /t 1")
        
            elif "quit" in query.lower():
                print("AI: Quitting...")
                say("quitting")
                exit(1)

            else:
                print("AI: Activating chat mode")
                say("chat mode activating")
                chat(query)