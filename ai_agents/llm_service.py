import requests
from django.conf import settings


def ask_llm(prompt):

    try:

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=60
        )

        # Print raw response for debugging
        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code != 200:
            return f"AI service unavailable.\n\n{response.text}"

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        return f"AI service unavailable.\n\n{str(e)}"