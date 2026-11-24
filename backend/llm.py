import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv("../.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def get_ai_response(user_text):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response.choices[0].message.content


# ADD THIS BELOW
def generate_response(intent, memory):

    prompt = f"""
    Intent: {intent}

    Known Information:
    {memory}

    If some appointment information is missing,
    ask ONLY for the next missing detail.

    Keep the response short.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
    "role": "system",
    "content": "You are a helpful voice assistant. Never claim an action has been completed unless explicitly told. If the user requests an appointment, acknowledge the request and ask for the next step. Do not invent bookings."
},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

import json

def extract_patient_name(text):

    prompt = f"""
Extract the patient's name from the sentence.

Sentence:
{text}

Rules:
- Return ONLY valid JSON.
- If no patient's name exists, return:
{{"patient_name": null}}

Example:

Input:
The patient's name is Shiva.

Output:
{{"patient_name":"Shiva"}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You extract structured information. Return JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    try:
        data = json.loads(response.choices[0].message.content)
        return data.get("patient_name")
    except:
        return None