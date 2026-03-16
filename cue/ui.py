from rich.console import Console
from rich.panel import Panel

console = Console()


def show_header():

    console.print(
        Panel(
            "CUE — Cognitive User Engine",
            border_style="cyan"
        )
    )


def ask_user():

    return console.input("\n[bold green]You > [/bold green]")


def print_ai(text):

    console.print(text, style="cyan", end="")