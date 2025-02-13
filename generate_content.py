import requests
from api_key import load_api_key

HUGGINGFACE_API_KEY = load_api_key('api.txt')
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
def generate_blog_content(topic):
    url = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = f"Generate an article on the given topic. Here's the title of the article: {topic}. You're a blog writer and you are turning the article given above into an unique seo-optimized blog post .The title is already written so please start with the body of the article. Formatting: Use H1,H2 and H3 headers Use HTML : You choose what to bold and bullet ponts . Make sure if you want to bold anything put in <br></br> tags and <li></li> tags for bullet points. Parameters: This blog post and it should be approx 1000 word long.Include an introduction, key points, and conclusion. Ensure it is engaging and informative."
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "No content generated")
                generated_text = generated_text.replace(prompt, "").strip()
                # print(generated_text)
                return generated_text
            else:
                raise Exception("Unexpected response format:", result)
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}, Response: {response.json()}")
    else:
        raise Exception(f"Failed to generate content: {response.status_code} {response.text}")

# generate_blog_content("AI and Wearable Tech: How They’re Revolutionizing Fitness in 2025")
