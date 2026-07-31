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
from datetime import datetime
import anthropic
from pydantic import BaseModel
from config import API_KEY, BASE_URL, MODEL, PRICE_IN, PRICE_OUT


client = anthropic.Anthropic(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM = "You are a concise, friendly assistant."

MAX_TURNS = 2

class Transcript(BaseModel):
    saved_at: datetime
    system: str
    turns: list[dict]

def capped(messages: list[dict]) -> list[dict]:
    recent_messages = messages[-MAX_TURNS * 2:]

    if recent_messages and recent_messages[0]["role"] == "assistant":
        recent_messages = recent_messages[1:]

    return recent_messages

history: list[dict] = []

total_in = 0
total_out = 0

while True:
    user = input("you> ").strip()

    if user in {"/quit", "exit"}:
        break
    if user == "/tokens":
        cost = (
            total_in / 1_000_000 * PRICE_IN 
            + total_out / 1_000_000 * PRICE_OUT
        )
        print( 
            f"input={total_in} "
            f"output={total_out} "
            f"estimated_cost = ${cost:.4f}"
        )
        continue
    if user == "/save":
        transcript = Transcript(
            saved_at=datetime.now(),
            system=SYSTEM,
            turns=history,
        )

        path = f"transcript-{transcript.saved_at:%Y%m%d-%H%M%S}.json"

        with open(path, "w", encoding="utf-8") as file:
            file.write(transcript.model_dump_json(indent=2))

        print("saved", path)
        continue
    if user == "/reset":
        history.clear()
        total_in = 0
        total_out = 0

        print("Conversation and token counters reset.")
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
        messages=capped(history),
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