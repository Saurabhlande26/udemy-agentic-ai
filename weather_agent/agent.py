
import json
from ollama import Client
from dotenv import load_dotenv
import requests

load_dotenv()

client = Client(
    host="http://127.0.0.1:11434"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return f"something went wrong"

SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using structured
START, PLAN and OUTPUT steps.

You work on START, PLAN and OUTPUT steps.

You need to first PLAN what needs to be done.
The PLAN can be multiple steps.

Once you think enough PLAN has been done,
finally you can give an OUTPUT.
You can also call a tool if required from the of the list of available tools.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives an input),
  PLAN (that can be multiple times), and finally OUTPUT.

Output JSON Format:

{
    "step": "START" | "PLAN" | "OUTPUT", | "TOOL",
    "content": "string"
}

Availvable Tools:
- get_weather: Takes city name as input string and returns the weather info about the city.
Example:

START: Hey, Can you solve 2 + 3 * 5 / 10

PLAN: Seems like user is interested in a math problem.

PLAN: Looking at the problem, we should solve this using BODMAS.

PLAN: Yes, BODMAS is the correct thing to be done here.

PLAN: First we must multiply 3 * 5 which is 15.

PLAN: Now the new equation is 2 + 15 / 10.

PLAN: We must perform divide that is 15 / 10 = 1.5.

PLAN: Now the new equation is 2 + 1.5.

PLAN: Now finally let's perform the add 3.5.

OUTPUT: The answer is 3.5.

Provide concise planning summaries rather than private
internal reasoning.
"""

print("\n\n")

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

user_query = input("➡️ ")

message_history.append({
    "role": "user",
    "content": user_query
})

while True:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🚀", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break
