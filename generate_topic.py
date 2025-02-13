import requests
from api_key import load_api_key

HUGGINGFACE_API_KEY = load_api_key("api.txt")
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
# HUGGINGFACE_MODEL = "deepseek-ai/DeepSeek-R1"
def generate_blog_title(topic, link):
    url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    # prompt = f"Generate a catchy and engaging blog title for the topic: '{topic}'"
    prompt = f"You're a blog writer and your job is to turn following news article into an unique SEO optimized blog post. Here's the title of the article {topic}. Here's the URL please read it here: {link}. Based on the information given above please generate a SEO optimized Article title. Parameters: Max 10 words and 1 sentence flow. Do not put quotes around the titles. Only give one titl."
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # return result[0].get("generated_text", "No title generated")
                generated_text = result[0].get("generated_text", "No content generated")
                generated_text = generated_text.replace(prompt, "").strip()
                if "Title Analysis:" in generated_text:
                    generated_text = generated_text.split("Title Analysis:")[0].strip()
                generated_text = generated_text.replace('"', '').strip()
                return generated_text
            else:
                raise Exception("Unexpected response format:", result)
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}, Response: {response.json()}")
    else:
        raise Exception(f"Failed to generate title: {response.status_code} {response.text}")

