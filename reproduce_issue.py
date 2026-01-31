import requests
import json

url = 'http://127.0.0.1:5000/tutor'

payload = {
    "question": "how the calcus works",
    "year_level": "Year 12",
    "chat_history": [],
    "profile": {
        "name": "Alex Thompson",
        "year_of_birth": 2007,
        "class_level": "A-levels",
        "subject_focus": "Mathematics",
        "likes": "Gaming, strategy games, puzzle games",
        "dislikes": "Long lectures, overly formal tone, condescending explanations"
    }
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:", response.json())
except Exception as e:
    print(f"Error: {e}")
