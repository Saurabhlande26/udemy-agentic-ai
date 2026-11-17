
from ollama import Client
import requests

client = Client(
    host="http://127.0.0.1:11434"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return f"something went wrong"


def main():
    user_query = input("> ")

    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    print(response.message.content)


if __name__ == "__main__":
   print( get_weather("New York"))
