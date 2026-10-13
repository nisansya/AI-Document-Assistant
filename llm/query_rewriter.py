from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from llm.generator import generate_answer
from llm.prompt import QUERY_REWRITE_PROMPT

client= Groq(
    api_key= GROQ_API_KEY
)

def rewrite_query(query, history):

    prompt= QUERY_REWRITE_PROMPT.format(
        conversation= history,
        query= query
    )

    rewritten_query= generate_answer(prompt)
    return rewritten_query.strip()

    