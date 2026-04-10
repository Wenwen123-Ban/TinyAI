"""TinyAI v1.7 CLI entrypoint."""

from __future__ import annotations

from .auth import login
from .data_loader import DataBlockLoader
from .logic_engine import LogicEngine, fmt_number


def _print_welcome() -> None:
    print("TinyAI v1.7 - Offline NLP Math Engine")
    print("Type math-like natural language questions, or 'quit' to exit.")


def _admin_menu(loader: DataBlockLoader) -> None:
    print("\nDeveloper Admin Menu")
    print("1) Update Data Blocks")
    print("2) Back")
    choice = input("Select option: ").strip()

    if choice != "1":
        return

    print("Choose block to update: constants | number_map | math_rules")
    block = input("Block: ").strip()
    print("Paste content. End with a line containing only 'EOF'.")

    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)

    saved_to = loader.update_block(block, "\n".join(lines))
    print(f"Updated {saved_to}")


def _maybe_login_admin(loader: DataBlockLoader) -> None:
    ans = input("Admin login? (y/N): ").strip().lower()
    if ans != "y":
        return

    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if login(username, password):
        print("Login successful.")
        _admin_menu(loader)
    else:
        print("Invalid credentials.")


def run() -> None:
    loader = DataBlockLoader()
    _maybe_login_admin(loader)
    blocks = loader.load()
    engine = LogicEngine(blocks)

    _print_welcome()

    while True:
        text = input("\n> ").strip()
        if text.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break

        result = engine.solve(text)
        print(f"Operation: {result.operation}")
        print(f"Result: {fmt_number(result.value)}")
        print(f"Details: {result.explanation}")


if __name__ == "__main__":
    run()
