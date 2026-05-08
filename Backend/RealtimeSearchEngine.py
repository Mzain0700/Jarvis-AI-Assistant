from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqApiKey = env_vars.get("GroqApiKey")

client = Groq(api_key=GroqApiKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

if not os.path.exists("Data"):
    os.makedirs("Data")

chatlog_path = r"Data/ChatLog.json"
try:
    with open(chatlog_path, "r", encoding="utf-8") as f:
        messages = load(f)
except FileNotFoundError:
    with open(chatlog_path, "w", encoding="utf-8") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query,advanced=True,num_results=5))
    Answer = f"The Search results for '{query}'are :\n[start]\n"
    # print(results)
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    
    Answer +="[end]"
    return Answer


SystemChatBot = [
    {"role": "system", "content": System},
    {"role" :  "user", "content" : "Hi"},
    {"role" : "assistant","content":"Hello, How Can I help You?"}
    ]

def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data += "Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    
    return data


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def RealtimeSearchEngine(prompt):
    global SystemChatBot,messages

    with open(chatlog_path, "r", encoding="utf-8") as f:
         messages = load(f)

    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role":"user","content":GoogleSearch(prompt)})
    completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer+= chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(chatlog_path, "w", encoding="utf-8") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer)




if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(RealtimeSearchEngine(user_input))
