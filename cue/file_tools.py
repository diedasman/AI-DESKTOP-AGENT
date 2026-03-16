import re
from rich.console import Console

console = Console()


def extract_and_save_file(text):

    pattern = r"FILE:\s*(.+?)\n```.*?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        filename = match.group(1).strip()
        content = match.group(2)

        with open(filename, "w") as f:
            f.write(content)

        console.print(f"[green]Created file:[/green] {filename}")