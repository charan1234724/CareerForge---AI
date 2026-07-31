import requests
from django.conf import settings


def search_adzuna(query="Python Developer", page=1):

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

    params = {

        "app_id": settings.ADZUNA_APP_ID,

        "app_key": settings.ADZUNA_APP_KEY,

        "what": query,

        "results_per_page": 20,

    }

    try:

        response = requests.get(

            url,

            params=params,

            timeout=30

        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return {

            "results": []

        }