
from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

# Connect to Docker Ollama
client = Client(
    host="http://127.0.0.1:11434"
)
# This is how api creates
@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

@app.post("/chat")
def chat(message: str = Body(..., description="The message")):

    # Send the message to the Ollama model and get the response
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    # Return the response from the Ollama model
    return {"response": response.message.content}
