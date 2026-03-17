import json
import os
import re
import time

CHAT_DIR = "chats"


def ensure_chat_dir(chat_dir=CHAT_DIR):
    os.makedirs(chat_dir, exist_ok=True)
    return chat_dir


def _chat_path(chat_id, chat_dir=CHAT_DIR):
    return os.path.join(ensure_chat_dir(chat_dir), f"{chat_id}.json")


def _save_chat(chat, chat_dir=CHAT_DIR):
    path = _chat_path(chat["id"], chat_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=2)
    return path


def create_chat_log(chat_dir=CHAT_DIR):
    now = int(time.time())
    chat_id = str(int(time.time() * 1000))
    chat_log = {
        "id": chat_id,
        "created_at": now,
        "updated_at": now,
        "messages": [],
        "pinned": False,
    }
    _save_chat(chat_log, chat_dir)
    return chat_log


def load_chat_log(chat_id, chat_dir=CHAT_DIR):
    path = _chat_path(chat_id, chat_dir)
    with open(path, "r", encoding="utf-8") as f:
        chat_log = json.load(f)

    chat_log.setdefault("messages", [])
    chat_log.setdefault("created_at", int(time.time()))
    chat_log.setdefault("updated_at", chat_log["created_at"])
    chat_log.setdefault("pinned", False)
    return chat_log


def append_message_to_log(chat_id, role, message, chat_dir=CHAT_DIR):
    chat_log = load_chat_log(chat_id, chat_dir)
    chat_log["messages"].append({"role": role, "content": message})
    chat_log["updated_at"] = int(time.time())
    _save_chat(chat_log, chat_dir)
    return chat_log


def list_chat_logs(chat_dir=CHAT_DIR):
    ensure_chat_dir(chat_dir)
    chats = []
    for name in os.listdir(chat_dir):
        if not name.endswith(".json"):
            continue
        path = os.path.join(chat_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            chat = json.load(f)
        chat.setdefault("id", os.path.splitext(name)[0])
        chat.setdefault("messages", [])
        chat.setdefault("created_at", int(os.path.getctime(path)))
        chat.setdefault("updated_at", chat.get("created_at", int(time.time())))
        chat.setdefault("pinned", False)
        chats.append(chat)

    return sorted(
        chats,
        key=lambda chat: (
            not chat.get("pinned", False),
            -chat.get("updated_at", chat.get("created_at", 0)),
        ),
    )


def build_history(chat_log):
    return [
        (message["role"], message["content"])
        for message in chat_log.get("messages", [])
        if message.get("role") in {"user", "assistant"}
    ]


def chat_title(chat_log, max_length=28):
    for message in chat_log.get("messages", []):
        if message.get("role") == "user" and message.get("content", "").strip():
            title = " ".join(message["content"].split())
            return _truncate(title, max_length)
    return "New chat"


def _truncate(value, max_length):
    if len(value) <= max_length:
        return value
    return value[: max_length - 3].rstrip() + "..."


def extract_and_save_file(text):
    pattern = r"FILE:\s*(.+?)\n```.*?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        filename = match.group(1).strip()
        content = match.group(2)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename
    return None
