import requests
import json

from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv(
    "STACK_URL"
)

# print(url)

response = requests.get(url)

for title in response.json()['items']:
    print(title['title'])
