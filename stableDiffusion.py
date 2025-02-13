import requests
def load_api_key(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if "HUGGINGFACE_API_KEY" in line:
                return line.split("=")[1].strip().strip("\"")
    raise Exception("API key not found in the file")
api_key = load_api_key("api.txt")
model = "stabilityai/stable-diffusion-3.5-large"


def generateImage(prompt):
    response = requests.post(
    f"https://api-inference.huggingface.co/models/{model}",
    headers={"Authorization": f"Bearer {api_key}"},
    json=prompt
    )

    if response.status_code == 200:
        with open("image.png", "wb") as f:
            f.write(response.content)
        print("Image saved as image.png")
    else:
        print("Failed:", response.status_code, response.text)
