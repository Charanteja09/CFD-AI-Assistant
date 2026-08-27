from ollama import chat


response = chat(
    model="gemma4",
    messages=[
        {
            "role": "user",
            "content": "Explain Reynolds number in simple words."
        }
    ]
)


print(response.message.content)