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

#from config import API_KEY, BASE_URL, MODEL
from config import API_KEY, BASE_URL, MODEL, PRICE_IN, PRICE_OUT


client = anthropic.Anthropic(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM = "You are a concise, friendly assistant."

history: list[dict] = []
total_in = 0
total_out = 0

while True:
    user = input("you> ").strip()

    if user in {"/quit", "exit"}:
        break
    if user == "/tokens":
        cost = (
            total_in / 1_000_000*PRICE_IN 
            + total_out / 1_000_000 * PRICE_OUT
        )
        print( 
            f"input={total_in}"
            f"output={total_out}"
            f"estimated_cost = ${cost:.4f}"
        )
        continue

    history.append(
        {
            "role": "user",
            "content": user,
        }
    )

    # response = client.messages.create(
    #     model=MODEL,
    #     max_tokens=800,
    #     system=SYSTEM,
    #     messages=history,
    # )

    # reply = response.content[0].text

    #print("bot>", reply)

    with client.messages.stream(
        model=MODEL,
        max_tokens=800,
        system=SYSTEM,
        messages=history,
    ) as stream:
        print("bot> ", end="")

        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)

        print()

        final = stream.get_final_message()

    reply = "".join(
        block.text
        for block in final.content
        if block.type == "text"
    )
    total_in += final.usage.input_tokens
    total_out += final.usage.output_tokens

    history.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )