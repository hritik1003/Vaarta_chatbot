import requests
from fastapi import FastAPI
app = FastAPI()


API_KEY = "f86669644364436f848f60dd16c89a76"


def get_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': "IN",
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    articles = response.json()["articles"]
    headlines = [article["title"] for article in articles]
    return headlines

