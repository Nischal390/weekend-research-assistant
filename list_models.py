import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def list_models():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    for model in client.models.list():
        print(f"Name: {model.name}, Supported Actions: {model.supported_actions}")

if __name__ == "__main__":
    list_models()
