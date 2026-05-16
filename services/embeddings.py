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
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"HuggingFace API Error: "
            f"{response.status_code} - {response.text}"
        )

    try:
        data = response.json()

    except Exception:
        raise Exception(
            f"Invalid HF response: {response.text}"
        )

    if isinstance(data, dict) and data.get("error"):
        raise Exception(data["error"])

    if isinstance(data, list) and isinstance(data[0], list):
        return data[0]

    return data