import requests
from django.conf import settings


BASE_URL = "https://jobs.indianapi.in"


def search_indianapi(query, page=1):

    headers = {
        "x-api-key": settings.INDIAN_API_KEY
    }

    params = {
        "query": query,
        "page": page,
    }

    try:
        response = requests.get(
            f"{BASE_URL}/jobs",
            headers=headers,
            params=params,
            timeout=30
        )
        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("Indian API Error:", e)
        return {"jobs": []}