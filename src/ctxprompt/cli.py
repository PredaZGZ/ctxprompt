from pathlib import Path

import typer

from ctxprompt.detectors import detect_stack
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

    files = scan_files(root)
    stack = detect_stack(root)

    ranked_files = sorted(
        files,
        key=lambda file_path: score_file(file_path, root),
        reverse=True,
    )

    print(f"Project root: {root}")
    print(f"Files detected: {len(files)}")
    print()

    print("Stack detected:")
    print(stack["stacks"])
    print()

    print("Package managers:")
    print(stack["package_managers"])
    print()

    if stack["entrypoints"]:
        print("Entrypoints:")
        print(stack["entrypoints"])
        print()

    if stack["run_commands"]:
        print("Run commands:")
        print(stack["run_commands"])
        print()

    if stack["test_commands"]:
        print("Test commands:")
        print(stack["test_commands"])
        print()

    print("Top ranked files:")
    for file_path in ranked_files[:10]:
        rel = file_path.relative_to(root)
        score = score_file(file_path, root)
        print(f"{score:>3}  {rel}")


if __name__ == "__main__":
    app()