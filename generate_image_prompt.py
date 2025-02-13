import requests
from api_key import load_api_key


HUGGINGFACE_API_KEY = load_api_key('api.txt')
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
def generate_blog_content(content):
    url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = f"You're are creating an image for a blog post. Here's the content of the blog post: {content}. Please return a stable diffusion image prompt to generate the image."
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "No content generated")
                generated_text = generated_text.replace(prompt, "").strip()
                generated_text = generated_text.replace('"', '').strip()
                # print(generated_text)
                return generated_text
            else:
                raise Exception("Unexpected response format:", result)
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}, Response: {response.json()}")
    else:
        raise Exception(f"Failed to generate content: {response.status_code} {response.text}")
