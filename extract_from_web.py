from bs4 import BeautifulSoup
import requests
import random

def extract_topic_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a"])
    topics = [headline.get_text() for headline in headlines if len(headline.get_text()) > 5]
    if topics:
        chosen_topic = random.choice(topics)
        print(f"Selected topic: {chosen_topic}")
        return chosen_topic
    else:
        return "The Future of AI in Content Creation"


