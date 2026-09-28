from ai_client import generate_text


def explain_topic(topic: str) -> str:

    prompt = f"""
You are EduGenie.

Explain the following topic to a beginner.

Topic:
{topic}

Give the answer in this format:

Definition:
Explain the topic in simple words.

Key Points:
- Point 1
- Point 2
- Point 3

Example:
Give one simple real-world example.

Use simple English.
Do not make the answer unnecessarily long.
"""

    return generate_text(prompt)