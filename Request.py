import requests

response = requests.post("http://127.0.0.1:5000/chat", json={
    "messages": [
        {"role": "user", "content": "Hello GPT!"}
    ]
})

print("Response:", response.json())
