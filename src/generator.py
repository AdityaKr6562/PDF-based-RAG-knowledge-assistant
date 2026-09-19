import ollama


MODEL_NAME = "qwen3:8b"


def generate_answer(question, retrieved_documents):

    # Build context from retrieved chunks
    context_parts = []

    for doc in retrieved_documents:

        context_parts.append(
            f"""
Source: {doc['source']}
Page: {doc['page']}

{doc['text']}
"""
        )

    context = "\n\n".join(context_parts)


    # Prompt the LLM
    prompt = f"""
You are an AI Knowledge Assistant.

Your job is to answer questions using ONLY the
information provided in the CONTEXT.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer cannot be found in the context,
   say:
   "I could not find this information in the provided documents."
4. Give a clear and concise answer.
5. Use the source information when appropriate.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    # Send request to Ollama
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]