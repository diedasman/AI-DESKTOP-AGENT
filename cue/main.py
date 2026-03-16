from .ui import show_header, ask_user, print_ai
from .llm import stream_chat
from .file_tools import extract_and_save_file


def main():

    show_header()

    while True:

        prompt = ask_user()

        if prompt == "/exit":
            break

        full_response = ""

        stream = stream_chat(prompt)

        for chunk in stream:

            delta = chunk["message"]["content"]
            full_response += delta
            print_ai(delta)

        print()

        extract_and_save_file(full_response)


if __name__ == "__main__":
    main()