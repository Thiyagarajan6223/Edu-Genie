from ai_client import generate_text


def recommend_learning_path(topic: str) -> str:

    prompt = f"""
You are EduGenie, a learning path assistant.

Create a learning path for:

{topic}

Give:

1. Beginner level
2. Intermediate level
3. Advanced level
4. Practice activities
5. Suggested learning order

Use simple English and clear bullet points.
"""

    return generate_text(prompt)