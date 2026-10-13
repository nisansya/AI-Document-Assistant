from llm.generator import generate_answer
from llm.prompt import COMPARISON_PROMPT

def compare_documents(document_a_chunks, document_b_chunks):
    # if not results:
    #     return "No document content available."
    
    # context= "\n\n".join(
    #     [
    #         doc["content"] 
    #         for doc in results
    #         ]
    #     )

    # prompt= COMPARISON_PROMPT.format(context= context)
    # answer= generate_answer(prompt)
    # return answer
    
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
    
    # document_a= "\n\n".join(
    #     chunk.page_content if hasattr(chunk, "page_content") else chunk.get("text", "")
    #     for chunk in document_a_chunks
    # )

    # document_b= "\n\n".join(
    #     chunk.page_content if hasattr(chunk, "page_content") else chunk.get("text", "")
    #     for chunk in document_b_chunks
    # )

    prompt= COMPARISON_PROMPT.format(
        document_a= document_a,
        document_b= document_b
    )
 
    answer= generate_answer(prompt)


    return answer
    
    
    # prompt= f"""
    #     Compare the following two documents.

    #     DOCUMENT A:
    #     {document_a}

    #     DOCUMENT B:
    #     {document_b}
            
    #     Compare them based on:

    #     1. Main objective
    #     2. Methodology
    #     3. Advantages
    #     4. Limitations
    #     5. Results
    #     6. Key differences

    #     Do not invent information.
    #     If a particular point is unavailable,
    #     write "Not available in the provided documents.
    #     Use only the provided documents.
    # """

    # return generate_answer(prompt)

