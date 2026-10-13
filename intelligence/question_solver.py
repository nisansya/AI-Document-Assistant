from llm.generator import generate_answer
from llm.prompt import QUESTION_PROMPT

def question_solver_document(results, query):
    if not results:
        return "No document content available.", []

    context= "\n\n".join(
        [doc["content"] 
        for doc in results]
    )

    sources= [
        {
            'sources': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
            'page': doc['metadata'].get('page', 'unknown'),
            'score': doc['similarity_score'],
            'preview': doc['content'][:300]+ '...'
        } for doc in results
    ]

    prompt= QUESTION_PROMPT.format(context= context, query= query)

    answer= generate_answer(prompt)
    return answer, sources