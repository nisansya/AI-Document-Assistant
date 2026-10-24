from llm.generator import generate_answer
from llm.prompt import SUMMARY_PROMPT

def summarize_document(chunks):
    if not chunks:
        return "No text found in this document."

    def get__short_text(chunks, max_chars= 8000):
        full_text= "\n\n".join(
        chunk.page_content if hasattr(chunk, "page_content") else chunk.get("text", "")
        for chunk in chunks
        )
        return full_text[:max_chars]
    context= get__short_text(chunks)

    prompt= SUMMARY_PROMPT.format(context= context)

    answer= generate_answer(prompt)
    return answer


    