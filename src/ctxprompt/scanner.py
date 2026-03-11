from pathlib import Path

from ctxprompt.ignore import should_ignore


def scan_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if should_ignore(path, root):
            continue

        files.append(path)

    return sorted(files)