import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

base_url = os.getenv("BASE_URL")
import requests


def chat():
    return base_url 


def query():
    txt_ = input()
    return txt_


while True:
    try:
        payload = {"input_text": query()}

        response = requests.post(chat(), json=payload)
        print(response.json())
    except KeyboardInterrupt:
        break

