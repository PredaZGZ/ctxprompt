from pathlib import Path

import typer

from ctxprompt.detectors import detect_stack
from ctxprompt.extractors import extract_file
from ctxprompt.prompt_builder import build_prompt
from ctxprompt.ranking import score_file
from ctxprompt.scanner import scan_files

app = typer.Typer()


@app.command()
def main(
    path: str = typer.Argument(".", help="Path to project root"),
) -> None:
    root = Path(path).resolve()

    if not root.exists():
        raise typer.BadParameter(f"Path does not exist: {root}")

    if not root.is_dir():
        raise typer.BadParameter(f"Path is not a directory: {root}")

    files = scan_files(root)
    stack = detect_stack(root)

    extracted = []
    for file_path in files:
        priority = score_file(file_path, root)
        info = extract_file(file_path, root, priority)
        extracted.append(info)

    extracted.sort(key=lambda item: item.priority, reverse=True)

    prompt = build_prompt(root, stack, extracted[:20])
    print(prompt)


if __name__ == "__main__":
    app()