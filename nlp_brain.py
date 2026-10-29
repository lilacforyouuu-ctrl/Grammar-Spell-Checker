import os
import requests

def check_grammar(text):
    url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json().get('matches', [])
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Connection error: {e}")
        return []