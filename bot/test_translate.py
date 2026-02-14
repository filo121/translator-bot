import requests

# Public LibreTranslate API endpoint
LIBRE_URL = "https://translate.mentality.rip/translate"

# Test message
text_to_translate = "hello"
target_lang = "fr"

try:
    response = requests.post(
        LIBRE_URL,
        data={
            "q": text_to_translate,
            "source": "auto",
            "target": target_lang,
            "format": "text"
        },
        timeout=10
    )
    response.raise_for_status()
    print("API Response:", response.json())
except Exception as e:
    print("Error calling translation API:", e)
