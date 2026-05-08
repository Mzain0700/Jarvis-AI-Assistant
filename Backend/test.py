# TestAPI.py
import requests
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
API_KEY = env_vars.get("HuggingFaceAPIKey")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "inputs": "a beautiful flower garden, 4K quality, maximum sharpness, ultra high detail"
}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    with open("test_image.jpg", "wb") as f:
        f.write(response.content)
    print("Image saved successfully!")
else:
    print(f"Error: {response.status_code}")
    print(response.text)