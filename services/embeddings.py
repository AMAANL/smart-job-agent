import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def get_embedding(text):

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": text
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"HuggingFace API Error: "
            f"{response.status_code} - {response.text}"
        )

    data = response.json()

    if isinstance(data, list):

        if len(data) > 0 and isinstance(data[0], list):
            return data[0]

        return data

    raise Exception(f"Unexpected response: {data}")