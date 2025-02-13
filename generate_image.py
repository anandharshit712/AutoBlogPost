import requests
import os
from api_key import load_api_key

output_dir = "generated_blogs"
os.makedirs(output_dir, exist_ok=True)

HUGGINGFACE_API_KEY = load_api_key('api.txt')
def generate_image(image_prompt):
    image_model = "stabilityai/stable-diffusion-3.5-large"
    url = f"https://api-inference.huggingface.co/models/{image_model}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = image_prompt
    response = requests.post(url, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        image_path = os.path.join(output_dir, "generated_image.png")
        with open(image_path, "wb") as f:
            f.write(response.content)
        image_name = os.path.basename(image_path)
        return image_name
    else:
        raise Exception(f"Failed to generate image: {response.status_code} {response.text}")
