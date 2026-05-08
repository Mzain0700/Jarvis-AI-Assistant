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
messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Urdu, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

if not os.path.exists("Data"):
    os.makedirs("Data")

chatlog_path = r"Data/ChatLog.json"
try:
    with open(chatlog_path, "r", encoding="utf-8") as f:
        messages = load(f)
except FileNotFoundError:
    with open(chatlog_path, "w", encoding="utf-8") as f:
        dump([], f, indent=4)



SystemChatBot = [{"role": "system", "content": System}]

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data= f"Please Use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth :{month}\nYear: {year}\n"
    data +=f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def ChatBot(Query):
    try:
        with open(chatlog_path, "r", encoding="utf-8") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = ""
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                Answer += delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(chatlog_path, "w", encoding="utf-8") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(chatlog_path, "w", encoding="utf-8") as f:
            dump([], f, indent=4)
        return ChatBot(Query)


if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
