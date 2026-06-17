import chainlit as cl
import requests

@cl.on_message
async def main(message: cl.Message):

    response = requests.post(
        "http://localhost:7000/v1/chat/completions",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            "max_tokens": 300
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]

    await cl.Message(
        content=answer
    ).send()