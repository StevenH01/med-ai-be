import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question_with_context(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a helpful medical tutor AI. Use the following study material to answer the question concisely and accurately.

Context:
{context}

Question:
{question}

Answer:
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a medical study assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]
