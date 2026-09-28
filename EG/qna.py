from ai_client import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the following student question clearly.

Question:
{question}

Instructions:

1. Use simple English.
2. Give an accurate answer.
3. Explain difficult terms.
4. Keep the answer concise.
5. Use examples when useful.
"""

    return generate_text(prompt)