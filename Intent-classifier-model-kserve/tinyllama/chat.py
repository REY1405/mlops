import requests

while True:
    prompt = input("You: ")

    r = requests.post(
        "http://localhost:7000/v1/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
    )

    print("Bot:", r.json()["choices"][0]["message"]["content"])