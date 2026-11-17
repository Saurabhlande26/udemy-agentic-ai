
from ollama import Client
import json

client = Client(
    host="http://127.0.0.1:11434"
)

SYSTEM_PROMPT = """
You are an expert AI assistant.

Follow these steps:
1. START: The user's input, handled by the application.
2. PLAN: Provide a short, high-level plan for solving the query.
3. OUTPUT: Provide the final answer.

Rules:
- Return exactly one JSON object per response.
- Every response must contain "step" and "content".
- Never return an empty JSON object.
- Never generate START yourself.
- Only generate the step requested by the application.
- Do not repeat previous steps.
- For arithmetic, follow correct operator precedence.
- Keep PLAN concise and OUTPUT accurate.

JSON examples:

{"step": "PLAN", "content": "Apply arithmetic operator precedence."}

{"step": "OUTPUT", "content": "The answer is 3.5."}
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "step": {
            "type": "string",
            "enum": ["PLAN", "OUTPUT"]
        },
        "content": {
            "type": "string",
            "minLength": 1
        }
    },
    "required": ["step", "content"],
    "additionalProperties": False
}

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def generate_step(expected_step):
    max_retries = 3

    for attempt in range(max_retries):
        instruction = (
            f"Generate the {expected_step} step now. "
            "Return both step and content as valid JSON."
        )

        if attempt > 0:
            instruction += (
                " Your previous response did not match "
                "the required structure or step."
            )

        messages = message_history + [
            {
                "role": "user",
                "content": instruction
            }
        ]

        response = client.chat(
            model="gemma:2b",
            messages=messages,
            format=RESPONSE_SCHEMA,
            options={
                "temperature": 0
            }
        )

        raw_result = response["message"]["content"]

        print("RAW RESULT:", repr(raw_result))

        try:
            parsed_result = json.loads(raw_result)
        except json.JSONDecodeError:
            print("Invalid JSON response.")
            continue

        step = parsed_result.get("step")
        content = parsed_result.get("content")

        if (
            step != expected_step
            or not isinstance(content, str)
            or not content.strip()
        ):
            print("Invalid step or missing content.")
            continue

        message_history.append({
            "role": "assistant",
            "content": raw_result
        })

        return content

    raise RuntimeError(
        f"Failed to generate a valid {expected_step} step."
    )


print("\n")

user_query = input("➡️ ")

message_history.append({
    "role": "user",
    "content": user_query
})

print("🚀 START:", user_query)

try:
    plan = generate_step("PLAN")
    print("🧠 PLAN:", plan)

    output = generate_step("OUTPUT")
    print("🤖 OUTPUT:", output)

except RuntimeError as error:
    print("Error:", error)

print("\n")
