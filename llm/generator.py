from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client= Groq(
    api_key= GROQ_API_KEY
)

def generate_answer(prompt):

    response= client.chat.completions.create(
        model= GROQ_MODEL,
        messages= [
            {
                "role": "user",
                "content": "You are a reliable document research assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature= 0.2
    )

    return response.choices[0].message.content