import requests
import base64
import os
from bs4 import BeautifulSoup

# Directory setup
output_dir = "generated_blogs"
os.makedirs(output_dir, exist_ok=True)

# Hugging Face API Configuration
def load_api_key(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if "HUGGINGFACE_API_KEY" in line:
                return line.split("=")[1].strip().strip("\"")
    raise Exception("API key not found in the file")
HUGGINGFACE_API_KEY = load_api_key("api.txt")
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

# Function to extract the blog topic from a news site
def extract_topic_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all("h3")
    if headlines:
        return headlines[0].get_text()
    else:
        return "The Future of AI in Content Creation"

def generate_blog_content(topic):
    url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": f"Write a detailed blog post on the topic: '{topic}'. Include an introduction, key points, and conclusion."}

    response = requests.post(url, headers=headers, json=payload)

    # Check response
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "No generated text found")
            else:
                raise Exception("Unexpected response format:", result)
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}, Response: {response.json()}")
    else:
        raise Exception(f"Failed to generate content: {response.status_code} {response.text}")

# Function to generate an image related to the blog topic using Hugging Face API
def generate_image(prompt):
    image_model = "stabilityai/stable-diffusion-3.5-large"
    url = f"https://api-inference.huggingface.co/models/{image_model}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        image_path = os.path.join(output_dir, "generated_image.png")
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    else:
        raise Exception(f"Failed to generate image: {response.status_code} {response.text}")

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
    file_path = os.path.join(output_dir, "blog_post.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Blog post saved at: {file_path}")

# Main execution
def generate_blog_with_image(topic):
    print(f"Generating blog content for topic: {topic}")
    blog_content = generate_blog_content(topic)

    print("Generating blog image...")
    image_path = generate_image(topic)

    print("Saving blog as HTML...")
    save_blog_as_html(topic, blog_content, "generated_image.png")

if __name__ == "__main__":
    news_url = "https://news.google.com/search?q=AI"
    print("Extracting topic from news site...")
    topic = extract_topic_from_url(news_url)
    generate_blog_with_image(topic)
