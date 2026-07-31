import google  as genai

API_KEY = "PASTE_YOUR_API_KEY_HERE"

genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("What is Python?")
    print(response.text)

except Exception as e:
    print("ERROR:")
    print(e)
