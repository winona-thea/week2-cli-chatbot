# import anthropic

# from config import API_KEY, BASE_URL, MODEL


# client = anthropic.Anthropic(
#     api_key=API_KEY,
#     base_url=BASE_URL,
# )

# response = client.messages.create(
#     model=MODEL,
#     max_tokens=300,
#     messages=[
#         {
#             "role": "user",
#             "content": "Say hello in 5 words",
#         }
#     ],
# )

# print(response.content[0].text)
# print(response.usage)

import anthropic

from config import API_KEY, BASE_URL, MODEL


client = anthropic.Anthropic(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM = "You are a concise, friendly assistant."

history: list[dict] = []


while True:
    user = input("you> ").strip()

    if user in {"/quit", "exit"}:
        break

    history.append(
        {
            "role": "user",
            "content": user,
        }
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=SYSTEM,
        messages=history,
    )

    reply = response.content[0].text

    print("bot>", reply)

    history.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )