''' Author- Jagu Manish || Python Programming Internship at Oasis Infobyte

------------------ TASK 1  - VOICE ASSISTANT BEGINNER -----------------------
Description:
For Beginners: Create a basic voice assistant that can perform simple tasks based on voice commands. Implement features like responding to "Hello" and providing predefined responses, telling the time or date, and searching the web for information based on user queries.
For Advanced: Develop an advanced voice assistant with natural language processing capabilities. Enable it to perform tasks such as sending emails, setting reminders, providing weather updates, controlling smart home devices, answering general knowledge questions, and even integrating with third-party APIs for more functionality.
Key Concepts and Challenges:
1. Speech Recognition: Learn how to recognize and process voice commands using speech recognition libraries or APIs.
2. Natural Language Processing (for Advanced): Implement natural language understanding to interpret and respond to user queries.
3. Task Automation (for Advanced): Integrate with various APIs and services to perform tasks like sending emails or fetching weather data.
4. User Interaction: Create a user-friendly interaction design that allows users to communicate with the assistant via voice commands.
5. Error Handling: Handle potential issues with voice recognition, network requests, or task execution.
6. Privacy and Security (for Advanced): Address security and privacy concerns when handling sensitive tasks or personal information.
7. Customization (for Advanced): Allow users to personalize the assistant by adding custom commands or integrations.

IDE used: Pycharm
Tip: Use VS Code for better performance.

'''
import speech_recognition as sr # type: ignore
import pyttsx3 #type: ignore
import datetime
import webbrowser
import os
import pywhatkit # type: ignore
import random
import shutil
import time
import wikipedia # type: ignore
from threading import Thread
import requests  # type: ignore


recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine_speaking = False  # Flag to track the speech engine state


def initialize_reminder_file():
    try:
        with open('reminders.txt', 'r') as file:
            pass
    except FileNotFoundError:
        with open('reminders.txt', 'w') as file:
            pass

initialize_reminder_file()

def speak(text):
    global engine_speaking
    if not engine_speaking:
        engine_speaking = True
        try:
            engine.say(text)
            engine.runAndWait()
        except RuntimeError:
            print("Error: Speech engine is already running.")
        finally:
            engine_speaking = False


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}\n")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return "None"
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return "None"
        return command.lower()

def respond_to_greeting(command):
    greetings = ["hello", "hi", "hey", "yo"]
    if any(greeting in command for greeting in greetings):
        speak("Hello! My name is Nova! How can I assist you today?")
        return True
    return False

def my_name(command):
    if "your name" in command:
        my_name = "Nova"
        speak(f"My name is {my_name}")
        return True
    return False

def tell_time(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
        return True
    return False

def tell_date(command):
    if "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")
        return True
    return False

def search_web(command):
    if "search for" in command:
        query = command.replace("search for", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return True
        else:
            speak("What would you like to search for?")
            return True
    return False

def open_application(command):
    if "open" in command:
        if "browser" in command:
            speak("Opening web browser")
            webbrowser.open("https://www.google.com")
            return True
        elif "notepad" in command or "text editor" in command:
            speak("Opening text editor")
            os.system("notepad" if os.name == "nt" else "gedit")
            return True
        elif "calculator" in command or "calculate" in command:
            speak("Opening Calculator")
            if os.name == "nt":
                os.system("calc")
            else:
                os.system("gnome-calculator" if shutil.which("gnome-calculator") else "bc")
            return True
        elif "chrome" in command:
            speak("Opening Chrome...")
            try:
                if os.name == "nt":
                    os.startfile("chrome")
                elif os.name == "posix":
                    os.system("google-chrome")
                else:
                    webbrowser.get("chrome").open_new_tab("https://www.google.com")
            except Exception as e:
                speak("Unable to open Chrome. Please make sure it's installed.")
                print(e)
            return True

    return False

def get_weather(command):
    if "weather" in command or "weather updates" in command or "weather report" in command:
        speak("Please provide a city name")
        city = listen().title()
        if city == 'None':
            return False

        api_key = 'c68f176b517e991a72bd973a671ed26b'
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
        if weather_data.status_code == 200:
            data = weather_data.json()
            status = data['weather'][0]['main']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            speak(f"Weather Conditions in {city}")

            print(f"Temperature: {temp}ºF")
            print(f"Status : {status}")
            print(f"Pressure: {pressure} hPa")
            print(f"Humidity: {humidity}%")

            speak(f"Temperature: {temp} Fahrenheit")
            speak(f"Status : {status}")
            speak(f"Pressure: {pressure} hectopascal")
            speak(f"Humidity: {humidity} percent")
        else:
            speak("Sorry, I couldn't retrieving the weather data. Please check the city name and try again.")
        return True
    return False

def set_reminder(command):
    if "remind me" in command or "set a reminder" in command:
        speak("What should I remind you about?")
        reminder = listen()
        if reminder != "None":
            speak("When should I remind you? Please say the time in HH:MM or HHMM format.")
            reminder_time = listen()
            if reminder_time != "None":
                reminder_time = reminder_time.replace(" ", "")  # Remove any spaces

                # Convert time from HHMM to HH:MM
                if len(reminder_time) == 4 and reminder_time.isdigit():
                    reminder_time = f"{reminder_time[:2]}:{reminder_time[2:]}"
                try:
                    reminder_time = datetime.datetime.strptime(reminder_time, "%H:%M").time()
                    reminder_datetime = datetime.datetime.combine(datetime.datetime.now(), reminder_time)
                    if reminder_datetime < datetime.datetime.now():
                        reminder_datetime += datetime.timedelta(days=1)
                    speak(f"Reminder set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}")
                    with open('reminders.txt', 'a') as file:
                        file.write(f"{reminder_datetime.strftime('%Y-%m-%d %H:%M')} - {reminder}\n")
                    Thread(target=check_reminder, args=(reminder, reminder_datetime)).start()
                    return True
                except ValueError:
                    speak("I couldn't understand the time format. Please try setting the reminder again.")
                    return False
    return False

def check_reminder(reminder, reminder_datetime):
    while True:
        if datetime.datetime.now() >= reminder_datetime:
            speak(f"Reminder: {reminder}")
            break
        time.sleep(10)

def tell_joke(command):
    if "joke" in command:
        jokes = ["Why don't scientists trust atoms? Because they make up everything!", "What do kids play when their mom is using the phone? Bored games.",
                "What do you call an ant who fights crime? A vigilANTe!" , "Why are snails slow? Because they’re carrying a house on their back.", " What’s the smartest insect? A spelling bee!",
                "What does a storm cloud wear under his raincoat? Thunderwear.", "What is fast, loud and crunchy? A rocket chip.", "What do you call a couple of chimpanzees sharing an Amazon account? PRIME-mates.",
                "Why did the teddy bear say no to dessert? Because she was stuffed.", "Why did the soccer player take so long to eat dinner? Because he thought he couldn’t use his hands.",
                "Name the kind of tree you can hold in your hand? A palm tree!", "What has ears but cannot hear? A cornfield.", "What’s a cat’s favorite dessert? A bowl full of mice-cream.",
                'What did the policeman say to his hungry stomach? “Freeze. You’re under a vest.”', "What did the left eye say to the right eye? Between us, something smells!",
                "What do you call a guy who’s really loud? Mike.", "Why do birds fly south in the winter? It’s faster than walking!", "What did the lava say to his girlfriend? 'I lava you!'",
                "Why did the student eat his homework? Because the teacher told him it was a piece of cake.", "What did Yoda say when he saw himself in 4k? HDMI.",
                "What’s Thanos’ favorite app on his phone? Snapchat.", "Sandy’s mum has four kids; North, West, East. What is the name of the fourth child? Sandy, obviously!",
                "What is a room with no walls? A mushroom.", 'What did one math book say to the other? “I’ve got so many problems.”', "What do you call two bananas on the floor? Slippers.",
                "A plane crashed in the jungle and every single person died. Who survived? Married couples.", "What do you call a Star Wars droid that takes the long way around? R2 detour.",
                "What goes up and down but doesn’t move? The staircase."]
        random_joke = random.choice(jokes)
        speak(random_joke)
        return True
    return False

def play_rhyme(command):
    rhymes =["""Baa, baa black sheep
Have you any wool
Yes sir, yes sir
Three bags full.

One for my master
And one for my dame
And one for the little boy
Who lives down the lane.""",
             """Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the King’s horses and all the King’s men,
Couldn’t put Humpty together again.""",
             """Jack and Jill went up the hill
To fetch a pail of water.
Jack fell down and broke his crown,
And Jill came tumbling after.
""",
             """Old MacDonald had a farm, E I E I O,
And on his farm he had a cow, E I E I O.
With a moo moo here and a moo moo there,
Here a moo, there a moo, everywhere a moo moo.
Old MacDonald had a farm, E I E I O.
""",
             """Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.
"""]
    if "poem" in command or "poetry" in command or "poem" in command or "nursery rhyme" in command or "kid's rhyme" in command or "rhyme" in command:
        selected_rhyme = random.choice(rhymes)
        speak(selected_rhyme)
        return True
    return False

def play_yt_video(command):
    if 'play' in command:
        speak('Opening YouTube...')
        query = command.replace('play', '').strip()
        pywhatkit.playonyt(query)
        return True
    return False

def answer_question(command):
    if "who is" in command or "who was" in command or "what is" in command:
        query = command.replace("who is", "").replace("what is", "").replace("who was", "").strip()
        if query:
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(f"Here is what I found: {result}")
                return True
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple meanings. Please be more specific.")
                print(f"DisambiguationError: {e.options}")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find any information on that topic.")
            except wikipedia.exceptions.WikipediaException as e:
                speak("Sorry, I couldn't retrieve the information.")
                print(f"WikipediaException: {e}")
    return False

def main():
    while True:
        command = listen()
        if command == "None":
            continue

        if "stop" in command or "bye" in command:
            speak("Good bye..! See you later!")
            break
        
        if my_name(command):
            continue
        
        if get_weather(command):
            continue

        if respond_to_greeting(command):
            continue

        if tell_time(command):
            continue

        if tell_date(command):
            continue

        if search_web(command):
            continue

        if open_application(command):
            continue

        if set_reminder(command):
            continue

        if tell_joke(command):
            continue

        if play_rhyme(command):
            continue

        if play_yt_video(command):
            continue

        if answer_question(command):
            continue

        speak("Sorry, I can't help with that.")


hour = datetime.datetime.now().hour
if 0 <= hour < 12:
    va_greeting = "Good Morning!"
elif 12 <= hour < 16:
    va_greeting = "Good Afternoon!"
else:
    va_greeting = "Good Evening!"

speak(f"{va_greeting} Voice assistant activated. How can I help you?")
main()
