import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set your API keys and email credentials here
NEWS_API_KEY = "goo"
OPENWEATHER_APP_ID = "hh"
TMDB_API_KEY = "dd"
EMAIL = "owaisahmad445566@gmail.com"
PASSWORD = "password"

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognition function
def take_command(prompt="How can I help you?"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return None

# Helper functions
def find_my_ip():
    try:
        ip_address = requests.get('https://api64.ipify.org?format=json').json()
        return ip_address["ip"]
    except Exception as e:
        print(f"Error: {e}")
        return None

def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except Exception as e:
        return f"Error: {e}"

def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

# Fetch latest news
def get_latest_news():
    try:
        res = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
        articles = res.get("articles", [])
        return [article["title"] for article in articles[:5]]
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_weather_report(city):
    try:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid").json()
        weather = res["weather"][0]["main"]
        temperature = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        return weather, f"{temperature}℃", f"{feels_like}℃"
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def get_trending_movies():
    try:
        res = requests.get(
            f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
        results = res.get("results", [])
        return [r["original_title"] for r in results[:5]]
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_random_joke():
    try:
        headers = {'Accept': 'application/json'}
        res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
        return res["joke"]
    except Exception as e:
        print(f"Error: {e}")
        return "I couldn't fetch a joke for you right now."

def get_random_advice():
    try:
        res = requests.get("https://api.adviceslip.com/advice").json()
        return res['slip']['advice']
    except Exception as e:
        print(f"Error: {e}")
        return "I couldn't fetch advice for you right now."

# Interactive menu
if __name__ == "__main__":
    speak("Welcome! I am your virtual assistant. How can I help you?")
    while True:
        command = take_command("Please tell me what you want to do or say exit to quit.")
        if command:
            if "ip address" in command:
                ip = find_my_ip()
                if ip:
                    speak(f"Your IP Address is {ip}.")
                    print(f"Your IP Address is: {ip}")

            elif "search on wikipedia" in command:
                speak("What should I search for?")
                query = take_command()
                if query:
                    results = search_on_wikipedia(query)
                    speak("Here is what I found on Wikipedia.")
                    print(results)
                    speak(results)

            elif "search on youtube" in command:
                speak("What should I play on YouTube?")
                video = take_command()
                if video:
                    kit.playonyt(video)

            elif "search on google" in command:
                speak("What should I search on Google?")
                query = take_command()
                if query:
                    kit.search(query)

            elif "news" in command:
                news = get_latest_news()
                if news:
                    speak("Here are the top 5 news headlines.")
                    for headline in news:
                        print(headline)
                        speak(headline)
                else:
                    speak("I couldn't fetch the news at the moment.")

            elif "weather" in command:
                speak("Which city?")
                city = take_command()
                if city:
                    weather, temp, feels_like = get_weather_report(city)
                    if weather:
                        speak(f"The weather in {city} is {weather} with a temperature of {temp}.")
                        print(f"Weather: {weather}, Temperature: {temp}, Feels Like: {feels_like}")
                    else:
                        speak("I couldn't fetch the weather for you right now.")

            elif "joke" in command:
                joke = get_random_joke()
                speak(joke)
                print(joke)

            elif "advice" in command:
                advice = get_random_advice()
                speak(advice)
                print(advice)

            elif "exit" in command:
                speak("Goodbye! Have a great day.")
                break

            else:
                speak("I did not understand. Please try again.")
