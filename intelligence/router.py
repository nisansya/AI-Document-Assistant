from llm.generator import generate_answer
from llm.prompt import ROUTER_PROMPT
import json

# client= Groq(
#     api_key= GROQ_API_KEY
# )

def route_query(query):
    prompt= ROUTER_PROMPT.format(
        query= query
    )

    response= generate_answer(prompt)

    response= response.strip()

    try:
        data= json.loads(response)

        intent= data.get(
            "intent",
            "QUESTION"
        )

        valid_intents= [
            'QUESTION',
            'SUMMARY',
            'COMPARISON',
            'RESEARCH'
        ]
        
        if intent in valid_intents:
            return intent
        
        return "QUESTION"

    except json.JSONDecodeError:
        return "QUESTION"
        
    # prompt= f"""
    #     Classify the user's request into exactly ONE category
        
    #     Categories:

    #     QUESTION
    #     SUMMARY
    #     COMPARISON
    #     RESEARCH

    #     Definitions:

    #     QUESTION:
    #     User wants an answer to a specific question.

    #     SUMMARY:
    #     User wants a summary of a document.

    #     COMPARISON:
    #     User wants two or more documents or concepts compared.

    #     RESEARCH:
    #     User wants a detailed explaination involving multiple piece of information.

    #     User query:

    #     {query}

    #     Return only the category.
    # """

    # response= client.chat.completions.create(
    #     model= GROQ_MODEL,
    #     message= [
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     temperature= 0

    # )

    # category= response.choice[0].message.content.strip()/


    allowed= {
        'QUESTION',
        'SUMMARY',
        'COMPARISON',
        'RESEARCH'
    }

    if category not in allowed:
        category= 'QUESTION'
    return category
    