from .file_tools import (
    append_message_to_log,
    build_history,
    create_chat_log,
    extract_and_save_file,
    list_chat_logs,
    load_chat_log,
)
from .llm import stream_chat
from .ui import create_terminal_ui

def main():
    ui = create_terminal_ui()
    active_chat = create_chat_log()
    chats = list_chat_logs()
    status = f"Started a new chat ({_chat_index(chats, active_chat['id'])})."

    try:
        while True:
            chats = list_chat_logs()
            active_chat = _refresh_active_chat(active_chat["id"], chats)
            prompt = ui.ask_user(chats, active_chat, status=status)

            if prompt == "/exit":
                break

            command_result = _handle_command(prompt, chats, active_chat)
            if command_result is not None:
                active_chat, status = command_result
                continue

            active_chat = append_message_to_log(active_chat["id"], "user", prompt)
            chats = list_chat_logs()
            ui.render(chats, active_chat, status="CUE is thinking...", force=True)

            history = build_history(active_chat)[:-1]
            stream = stream_chat(history, prompt)
            full_response = ""
            for chunk in stream:
                delta = chunk.get("message", {}).get("content", "")
                full_response += delta
                ui.render(chats, active_chat, status="CUE is responding...", draft_assistant=full_response)

            saved_filename = extract_and_save_file(full_response) if full_response else None
            active_chat = append_message_to_log(active_chat["id"], "assistant", full_response)
            chats = list_chat_logs()
            status = f"Created file: {saved_filename}" if saved_filename else f"Updated chat {_chat_index(chats, active_chat['id'])}."
            ui.render(chats, active_chat, status=status, force=True)
    except KeyboardInterrupt:
        pass
    finally:
        ui.stop()


def _handle_command(prompt, chats, active_chat):
    if prompt == "/new":
        new_chat = create_chat_log()
        chats = list_chat_logs()
        return new_chat, f"Started chat {_chat_index(chats, new_chat['id'])}."

    if prompt.startswith("/switch"):
        parts = prompt.split(maxsplit=1)
        if len(parts) < 2:
            return active_chat, "Use /switch <number> to open a chat from the sidebar."

        target = parts[1].strip()
        selected_chat = _select_chat(target, chats)
        if selected_chat is None:
            return active_chat, f"Couldn't find chat '{target}'."
        return load_chat_log(selected_chat["id"]), f"Opened chat {_chat_index(chats, selected_chat['id'])}."

    return None

def _select_chat(target, chats):
    if target.isdigit():
        index = int(target) - 1
        if 0 <= index < len(chats):
            return chats[index]

    for chat in chats:
        if chat["id"] == target:
            return chat
    return None

def _refresh_active_chat(active_chat_id, chats):
    for chat in chats:
        if chat["id"] == active_chat_id:
            return load_chat_log(chat["id"])
    return create_chat_log()

def _chat_index(chats, chat_id):
    for index, chat in enumerate(chats, start=1):
        if chat["id"] == chat_id:
            return index
    return "?"

if __name__ == "__main__":
    main()
