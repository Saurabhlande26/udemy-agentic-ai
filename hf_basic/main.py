from transformers import pipeline

pipe = pipeline(
    "image-text-to-text",
    model="HuggingFaceTB/SmolVLM2-256M-Video-Instruct",
    device="mps"
)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"
            },
            {
                "type": "text",
                "text": "What animal is on the candy?"
            }
        ]
    }
]

result = pipe(
    text=messages,
    max_new_tokens=50
)

answer = result[0]["generated_text"][-1]["content"]

print("AI Answer:", answer)