from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "target",
    "out",
    ".turbo",
}

EXCLUDED_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".pyc",
    ".pyo",
    ".class",
    ".so",
    ".dll",
    ".dylib",
    ".map",
}


def should_ignore_dir(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    return any(part in EXCLUDED_DIRS for part in rel_parts)


def should_ignore_file(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts

    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return True

    if path.suffix.lower() in EXCLUDED_EXTS:
        return True

    return False