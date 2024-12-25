from fastapi import FastAPI, HTTPException, Request
import logging
import os
# Instead of just importing openai, import the OpenAI class
# (Make sure you have a compatible version of the openai package installed)
from openai import OpenAI

from middleware import register_middleware

# Initialize FastAPI application
app = FastAPI()
register_middleware(app)

# Logging
logging.basicConfig(level=logging.INFO)

# Example in-memory storage (for demo)
processed_messages = {}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize your OpenAI client with the given API key
client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/username/bot/1000")
async def process_message(request: Request):
    """
    Endpoint для приёма сообщений, обращения к OpenAI и возвращения ответа.
    """
    try:
        # Get the payload
        payload = await request.json()
        logging.info(f"Received message for processing: {payload}")

        platform = payload.get("platform")
        message_text = payload.get("message_text")

        if not platform or not message_text:
            raise HTTPException(status_code=400, detail="Missing required fields in payload")

        # Build the messages array
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Respond in a natural, human-like way. "
                    "If someone asks 'who are you?', respond: 'I'm Islambek, I'm a seller of books'."
                )
            },
            {
                "role": "user",
                "content": message_text
            }
        ]

        # Call your desired model
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Extract only the 'content' from the bot's response
        response_content = completion.choices[0].message.content
        print(response_content)

        # Store in memory (demo) — optional
        processed_messages[message_text] = {
            "platform": platform,
            "message_text": message_text,
            "response_text": response_content,
        }


        json_resp = {"status": "success", "reply": response_content}
        logging.info(f"Replying with: {json_resp}")
        return json_resp

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing the message")
