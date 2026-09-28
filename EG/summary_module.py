from ai_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie.

Summarize the following educational text.

Text:
{text}

Requirements:

- Keep the main meaning.
- Remove unnecessary details.
- Use simple English.
- Make it easy for students to revise.
- Give important points as bullet points.
"""

    return generate_text(prompt)