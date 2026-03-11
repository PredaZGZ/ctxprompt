from pathlib import Path

import typer

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

    print(f"Project root: {root}")
    print(f"Files detected: {len(files)}")
    print()

    for file_path in files[:30]:
        print(file_path.relative_to(root))


if __name__ == "__main__":
    app()