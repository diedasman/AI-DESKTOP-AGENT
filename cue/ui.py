import os
import sys
from datetime import datetime

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from .file_tools import chat_title

console = Console()

# TODO: This is a very basic terminal UI implementation. It can be improved in many ways, such as:
# - Better input handling (e.g. support for arrow keys, history, etc.)
# - Better rendering performance (e.g. only update the parts of the screen that changed)
# - More features (e.g. chat deletion, renaming, etc.)

class TerminalUI:
    def __init__(self):
        self.console = console
        self.live = Live(
            console=self.console,
            auto_refresh=True,
            screen=True,
            refresh_per_second=60,
        )
        self._started = False
        self._last_frame = None

    def start(self):
        if not self._started:
            self.live.start()
            self._started = True

    def stop(self):
        if self._started:
            self.live.stop()
            self._started = False

    def render(self, chats, active_chat, status=None, draft_assistant="", input_buffer="", force=False):
        self.start()
        frame = _build_layout(chats, active_chat, status, draft_assistant, input_buffer)
        frame_key = (
            active_chat.get("id"),
            len(active_chat.get("messages", [])),
            status or "",
            draft_assistant,
            input_buffer,
            tuple((chat.get("id"), chat.get("updated_at"), len(chat.get("messages", []))) for chat in chats),
        )
        if force or frame_key != self._last_frame:
            self.live.update(frame, refresh=True)
            self._last_frame = frame_key

    def ask_user(self, chats, active_chat, status=None):
        buffer = ""
        self.start()
        self.render(chats, active_chat, status=status, input_buffer=buffer, force=True)

        while True:
            key = _read_key()
            if key in {"\r", "\n"}:
                return buffer
            if key == "\x03":
                return "/exit"
            if key in {"\x08", "\x7f"}:
                buffer = buffer[:-1]
            elif key and key >= " ":
                buffer += key

            self.render(chats, active_chat, status=status, input_buffer=buffer)


def create_terminal_ui():
    return TerminalUI()


def _build_layout(chats, active_chat, status, draft_assistant, input_buffer):
    layout = Layout()
    layout.split_column(
        Layout(_build_header(), size=3),
        Layout(name="body", ratio=1),
        Layout(_build_footer(status), size=5),
    )
    layout["body"].split_row(
        Layout(_build_sidebar(chats, active_chat), size=32),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_column(
        Layout(_build_chat_panel(active_chat, draft_assistant), ratio=1),
        Layout(_build_input_panel(input_buffer), size=5),
    )
    return layout


def _build_header():
    return Panel("CUE - Cognitive User Engine", border_style="cyan")


def _build_footer(status):
    help_text = Text()
    help_text.append("/new", style="bold cyan")
    help_text.append(" start a fresh chat    ")
    help_text.append("/switch <number>", style="bold cyan")
    help_text.append(" open a chat from the sidebar    ")
    help_text.append("/exit", style="bold cyan")
    help_text.append(" quit")

    body = [help_text]
    if status:
        body.append(Text(status, style="yellow"))
    return Panel(Group(*body), title="Controls", border_style="blue")


def _build_sidebar(chats, active_chat):
    lines = [Text("[+] New chat", style="bold green"), Text("")]

    for index, chat in enumerate(chats, start=1):
        prefix = ">" if chat["id"] == active_chat["id"] else " "
        style = "bold cyan" if chat["id"] == active_chat["id"] else "white"
        lines.append(Text(f"{prefix} {index}. {chat_title(chat)}", style=style))
        lines.append(Text(f"   {_format_chat_meta(chat)}", style="dim"))

    if len(lines) == 2:
        lines.append(Text("No saved chats yet.", style="dim"))

    return Panel(Group(*lines), title="Chats", border_style="magenta")


def _build_chat_panel(active_chat, draft_assistant):
    messages = list(active_chat.get("messages", []))
    if draft_assistant:
        messages.append({"role": "assistant", "content": draft_assistant})

    return Panel(
        _render_messages(messages),
        title=chat_title(active_chat, max_length=40),
        border_style="cyan",
    )


def _build_input_panel(input_buffer):
    prompt = Text()
    prompt.append("You > ", style="bold green")
    prompt.append(input_buffer or "", style="white")
    prompt.append("|", style="bold green")
    return Panel(prompt, title="Input", border_style="green")


def _render_messages(messages):
    if not messages:
        return Text("New chat ready. Type a message below or use /switch to open an older chat.", style="dim")

    max_lines = max(console.size.height - 20, 12)
    collected = []
    total_lines = 0

    for message in reversed(messages):
        block = _message_block(message)
        line_count = block.plain.count("\n") + 1
        if collected and total_lines + line_count > max_lines:
            break
        collected.append(block)
        total_lines += line_count

    collected.reverse()
    return Group(*collected)


def _message_block(message):
    role = message.get("role", "assistant")
    content = message.get("content", "")
    label = "You" if role == "user" else "CUE"
    style = "bold green" if role == "user" else "bold cyan"
    return Text.assemble((f"{label}: ", style), content, "\n")


def _format_chat_meta(chat):
    stamp = chat.get("updated_at", chat.get("created_at"))
    if not stamp:
        return "empty"
    message_count = len(chat.get("messages", []))
    when = datetime.fromtimestamp(stamp).strftime("%Y-%m-%d %H:%M")
    return f"{message_count} msgs - {when}"


def _read_key():
    if os.name == "nt":
        return _read_key_windows()
    return _read_key_posix()


def _read_key_windows():
    import msvcrt

    while True:
        key = msvcrt.getwch()
        if key in {"\x00", "\xe0"}:
            msvcrt.getwch()
            continue
        return key


def _read_key_posix():
    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == "\x1b":
            next_char = sys.stdin.read(1)
            if next_char == "[":
                sys.stdin.read(1)
            return ""
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
