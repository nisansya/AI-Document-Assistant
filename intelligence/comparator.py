from llm.generator import generate_answer
from llm.prompt import COMPARISON_PROMPT

def compare_documents(document_a_chunks, document_b_chunks):
    
    if not document_a_chunks:
        return "Document A does not contain readable content."

    if not document_b_chunks:
        return "Document B does not contain readable content."

    def get__short_text(chunks, max_chars= 3000):
        full_text= "\n\n".join(
        chunk.page_content if hasattr(chunk, "page_content") else chunk.get("text", "")
        for chunk in chunks
        )
        return full_text[:max_chars]

    document_a= get__short_text(document_a_chunks)
    document_b= get__short_text(document_b_chunks)

    prompt= COMPARISON_PROMPT.format(
        document_a= document_a,
        document_b= document_b
    )
 
    answer= generate_answer(prompt)


    return answer
    
    