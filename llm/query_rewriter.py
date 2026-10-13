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

    # if not history:
    #     return query
    
    # history_text= "\n".join(
    #     [
    #         f"{message['role']}: {message['content']}"
    #         for message in history[-6:]
    #     ]
    # )

    # prompt= f"""
    # You are a query rewriting system.
    # Rewrite the user's latest question so that it is self-contained and suitable for document retrieval.

    # Do not answer the question.

    # Conversation:

    # {history_text}

    # Latest question:
    # {query}
    
    # Rewritten query:

    # """

    # response= client.chat.completions.create(
    #     model= GROQ_MODEL,
    #     messages= [
    #         {
    #             'role': "user",
    #             'content': prompt
    #         }
    #     ],
    #     temperature= 0
    # )

    # return response.choices[0].message.content.strip()