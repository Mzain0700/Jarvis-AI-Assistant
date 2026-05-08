from AppOpener import close, open as appopen    
from webbrowser import open as webopen         
# from pywhatkit import search, playonyt          
from dotenv import dotenv_values                  
from bs4 import BeautifulSoup              
from rich import print                            
from groq import Groq                            
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import urllib.parse
import yt_dlp
import re
from youtube_search import YoutubeSearch

env_vars = dotenv_values(".env")
GroqApiKey = env_vars.get("GroqApiKey")  


classes = [
    "ZcUbWf", "hgKElC", "LTK0o SY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", 
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "O5uR6d LTK0o", "vL2Y6d", "webanswers-webanswers_table__webanswers-table", 
    "dDoNo ikb4Bb gsrt", "sXLa0e", "LWKfKe", "vQF4g", "q3vWpe", "kno-rdesc", "SPZz6b"
]


useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'


client = Groq(api_key=GroqApiKey)


professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don’t hesitate to ask.",
]


messages = []


SystemChatBot = [
    {
        "role": "system",
        "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters."
    }
]


# def GoogleSearch(Topic):
#     search(Topic) 
#     return True 

def GoogleSearch(Topic):
    try:
        query = urllib.parse.quote_plus(Topic)
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return True
    except Exception as e:
        print(f"Google search error: {e}")
        return False

def Content(Topic):
    def OpenNotepad(file_path):
        subprocess.Popen(['notepad.exe', file_path])
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": prompt})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic:str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)
    

    filename = rf"Data/{Topic.lower().replace(' ', '')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
        
    OpenNotepad(filename)
    return True


def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic.replace(' ', '+')}"
    webbrowser.open(Url4Search)
    return True

# def PlayYoutube(query):
#     playonyt(query)
#     return True

# def PlayYoutube(query):
#     try:
#         ydl_opts = {
#             'quiet': True,
#             'default_search': 'ytsearch1',  # Only return 1 result
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(query, download=False)

#             # Handle if 'entries' exists (playlist/search)
#             if 'entries' in info:
#                 video_url = info['entries'][0]['webpage_url']
#             else:
#                 # If a single video is directly returned
#                 video_url = info.get('webpage_url')

#             if video_url:
#                 webbrowser.open(video_url)
#                 return True
#             else:
#                 print("No video URL found.")
#                 return False

#     except Exception as e:
#         print(f"yt-dlp error: {e}")
#         return False

def PlayYoutube(query):
    try:
        # Get the first video result
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            video_id = results[0]['id']
            webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")
            return True
        else:
            # Fallback to search if no results found
            query_encoded = urllib.parse.quote_plus(query)
            webbrowser.open(f"https://www.youtube.com/results?search_query={query_encoded}")
            return False
    except Exception as e:
        print(f"YouTube playback error: {e}")
        return False    
 
def OpenApp(app, sess=requests.Session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        def extract_links(html):
            if not html:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {'User-Agent': useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app)
        if html:
            links = extract_links(html)[0]
            webopen(links)
             
        return True
    

def CloseApp(app):
    if "chrome" in app.lower():
        return False  # Skip Chrome
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False


def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    
    def unmute():
        keyboard.press_and_release("volume mute")
    
    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")
    
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True


async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
    
        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command.removeprefix("close ")))
        
        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command.removeprefix("play ")))
        
        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command.removeprefix("content ")))
        
        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")))
        
        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")))
        
        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command.removeprefix("system ")))
        
        else:
            print(f"No function found for: {command}")
    
    results = await asyncio.gather(*funcs, return_exceptions=True)
    for result in results:
        yield result


async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    # Test commands
    asyncio.run(Automation([
        # "open notepad",
        # "google search Python programming",
        "play afsana youngster music",
        # "content How to write a formal letter",

    ]))