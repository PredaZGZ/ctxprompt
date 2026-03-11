from pathlib import Path

import typer

from ctxprompt.detectors import detect_stack
from ctxprompt.extractors import extract_file
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

    extracted = []
    for file_path in files:
        priority = score_file(file_path, root)
        info = extract_file(file_path, root, priority)
        extracted.append(info)

    extracted.sort(key=lambda item: item.priority, reverse=True)

    print(f"Project root: {root}")
    print(f"Files detected: {len(files)}")
    print()

    print("Stack detected:")
    print(stack["stacks"])
    print()

    print("Package managers:")
    print(stack["package_managers"])
    print()

    print("Top ranked files:")
    for file_info in extracted[:10]:
        print(f"{file_info.priority:>3}  {file_info.rel_path}")
        if file_info.symbols:
            names = ", ".join(symbol.name for symbol in file_info.symbols[:8])
            print(f"     symbols: {names}")
        if file_info.imports:
            names = ", ".join(file_info.imports[:8])
            print(f"     imports: {names}")


if __name__ == "__main__":
    app()