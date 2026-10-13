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
            'COMPARISON'
        ]
        
        if intent in valid_intents:
            return intent
        
        return "QUESTION"

    except json.JSONDecodeError:
        return "QUESTION"

    # allowed= {
    #     'QUESTION',
    #     'SUMMARY',
    #     'COMPARISON',
    #     'RESEARCH'
    # }

    # if category not in allowed:
    #     category= 'QUESTION'
    # return category
    