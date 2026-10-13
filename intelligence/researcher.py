from llm.generator import generate_answer
from llm.prompt import RESEARCH_PROMPT

def research_documents(results, query):
    if not results:
        return "No document content available."

    context= "\n\n".join([
        doc["content"] 
        for doc in results]
    )

    prompt= RESEARCH_PROMPT.format(context= context, query= query)

    answer= generate_answer(prompt)
    return answer