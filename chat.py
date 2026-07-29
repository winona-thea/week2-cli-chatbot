import anthropic

from config import API_KEY, BASE_URL, MODEL


client = anthropic.Anthropic(
    api_key=API_KEY,
    base_url=BASE_URL,
)

response = client.messages.create(
    model=MODEL,
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "Say hello in 5 words",
        }
    ],
)

print(response.content[0].text)
print(response.usage)