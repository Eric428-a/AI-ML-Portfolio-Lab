def build_rag_prompt(
    question: str,
    contexts: list[str],
) -> str:
    if contexts:
        context_text = "\n\n---\n\n".join(
            contexts
        )
    else:
        context_text = "No relevant document context was found."

    return f"""
Use the following document context to answer the question.

DOCUMENT CONTEXT:
{context_text}

QUESTION:
{question}

Instructions:
- Answer using the supplied document context.
- Do not invent information.
- If the answer cannot be found in the context, say so clearly.
- Keep the answer relevant to the question.
""".strip()