from llm.generator import generate_answer
from llm.prompt import SUMMARY_PROMPT

def summarize_document(chunks):
    if not chunks:
        return "No text found in this document."

    # context= "\n\n".join([
    #     chunk["text"] 
    #     for chunk in chunks
    # ])

    def get__short_text(chunks, max_chars= 3000):
        full_text= "\n\n".join(
        chunk.page_content if hasattr(chunk, "page_content") else chunk.get("text", "")
        for chunk in chunks
        )
        return full_text[:max_chars]
    context= get__short_text(chunks)

    prompt= SUMMARY_PROMPT.format(context= context)

    answer= generate_answer(prompt)
    return answer


    # summaries= []

    # for chunk in chunks:
    #     prompt= f"""
    #         Summarize the following document section.

    #         Focus on:
    #         -Main idea
    #         -Important findings
    #         -Key concepts

    #         Document section:
    #         {chunk}
    #     """

    #     summary= generate_answer(prompt)

    #     summaries.append(summary)

    # final_context= "\n\n".join(summaries)

    # final_prompt= f"""
    #             Create a concise overall summary from these section summaries.

    #             Section summaries:

    #             {final_context}
    #         """

    # return generate_answer(final_prompt)