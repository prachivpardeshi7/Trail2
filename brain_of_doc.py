from dotenv import load_dotenv
import os
import base64
from groq import Groq

# Step 1: Load .env and get API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 2: Encode image as base64
def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Analyze image with Groq multimodal model
def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)  # ✅ Pass API key here

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }}
            ]
        }
    ]

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return chat_completion.choices[0].message.content

# Step 4: Call everything (only for testing purposes)
if __name__ == "__main__":
    # Change this to your actual image file
    image_path = "acne.jpg"

    # Prompt and model name
    query = "Is there something wrong with my face?"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"

    # Encode and analyze
    try:
        encoded = encode_image(image_path)
        response = analyze_image_with_query(query, model, encoded)
        print("\n🩺 Doctor's Response:\n", response)
    except Exception as e:
        print("❌ Error:", e)

