import ollama
import requests
import base64
import os
from bs4 import BeautifulSoup
from stableDiffusion import generateImage

# Directory setup
output_dir = "generated_blogs"
os.makedirs(output_dir, exist_ok=True)

# Ollama LLM Model Configuration
OLLAMA_TEXT_MODEL = "mistral"
OLLAMA_IMAGE_MODEL = "stable-diffusion"

# Function to extract the blog topic from a news site
def extract_topic_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all("h3")
    if headlines:
        return headlines[0].get_text()
    else:
        return "The Future of AI in Content Creation"

# Function to generate blog content
def generate_blog_content(topic):
    client = ollama.Client()
    prompt = f"Write a detailed blog post on the topic: '{topic}'. Include an introduction, key points, and conclusion."
    response = client.generate(model=OLLAMA_TEXT_MODEL, prompt=prompt)
    return response['text']

# Function to save the blog post as an HTML file
def save_blog_as_html(title, content, image_path):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <img src="{image_path}" alt="Blog Image" style="width:100%;max-width:600px;">
        <div>
            <p>{content.replace('\n', '<br>')}</p>
        </div>
    </body>
    </html>
    """
    file_path = os.path.join(output_dir, "blog_post1.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Blog post saved at: {file_path}")

# Main execution
def main():
    news_url = "https://news.google.com/search?q=fitness"
    print("Extracting topic from news site...")
    topic = extract_topic_from_url(news_url)

    print(f"Generating blog content for topic: {topic}")
    blog_content = generate_blog_content(topic)

    print("Generating blog image...")
    prompt = {"inputs": ""}
    generateImage(prompt)

    print("Saving blog as HTML...")
    save_blog_as_html(topic, blog_content, "image.png")

if __name__ == "__main__":
    main()
