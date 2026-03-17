import ollama  # type: ignore
from duckduckgo_search import DDGS
from rich.console import Console

from .config import MODEL, SYSTEM_PROMPT

MAX_HISTORY = 6  # keep small for Pi

console = Console()


def build_messages(history, user_prompt):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for role, content in history[-MAX_HISTORY:]:
        messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_prompt})
    return messages


def search_web(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):
            results.append(r["body"])
    return "\n".join(results)


def stream_chat(history, user_prompt):
    messages = build_messages(history, user_prompt)
    try:
        return ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True,
        )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return []
