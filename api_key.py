def load_api_key(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if "HUGGINGFACE_API_KEY" in line:
                return line.split("=")[1].strip().strip("\"")
    raise Exception("API key not found in the file")
