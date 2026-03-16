import ollama
from .config import MODEL, SYSTEM_PROMPT


def stream_chat(user_prompt):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    return ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True
    )