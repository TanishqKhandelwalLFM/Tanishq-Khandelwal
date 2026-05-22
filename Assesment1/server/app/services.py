import requests
from app.config import API_URL
from app.models import Post

def get_posts():

    response = requests.get(API_URL)

    data = response.json()

    validated = [
        Post(**post)
        for post in data
    ]

    return validated