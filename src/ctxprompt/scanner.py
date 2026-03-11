import os
from pathlib import Path

from ctxprompt.ignore import EXCLUDED_DIRS, should_ignore_file


def scan_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)

        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname not in EXCLUDED_DIRS
        ]

        for filename in filenames:
            path = current_path / filename

            if should_ignore_file(path, root):
                continue

            files.append(path)

    return sorted(files)