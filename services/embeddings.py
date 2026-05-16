import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = (
    "https://api-inference.huggingface.co/"
    "pipeline/feature-extraction/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def get_embedding(text):

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": text
        }
    )

    embedding = response.json()

    return embedding