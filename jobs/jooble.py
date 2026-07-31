import requests
from django.conf import settings


def search_jooble(query="Python Developer", page=1):
    """
    Search jobs using Jooble API.
    Returns a dictionary with a 'jobs' list.
    """

    url = f"https://jooble.org/api/{settings.JOOBLE_API_KEY}"

    payload = {
        "keywords": query,
        "location": "",
        "page": page
    }

    try:
        headers = {
    "Content-Type": "application/json"
}

        response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=30
)
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print("Jooble Error:", e)
        return {
            "jobs": []
        }