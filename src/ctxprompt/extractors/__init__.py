from pathlib import Path

from ctxprompt.models import FileInfo
from ctxprompt.extractors.python_extractor import extract_python_file


DOC_SUFFIXES = {".md", ".txt", ".rst"}
CONFIG_SUFFIXES = {".toml", ".json", ".yaml", ".yml", ".ini", ".cfg", ".env"}


def extract_file(path: Path, root: Path, priority: int) -> FileInfo:
    suffix = path.suffix.lower()

    if suffix == ".py":
        return extract_python_file(path, root, priority)

    content = path.read_text(encoding="utf-8", errors="ignore")

    if suffix in DOC_SUFFIXES:
        file_type = "doc"
        language = "text"
    elif suffix in CONFIG_SUFFIXES or path.name in {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env.example",
    }:
        file_type = "config"
        language = suffix.lstrip(".") if suffix else "config"
    else:
        file_type = "text"
        language = "text"

    return FileInfo(
        path=path,
        rel_path=str(path.relative_to(root)),
        language=language,
        file_type=file_type,
        priority=priority,
        size_bytes=path.stat().st_size,
        content_preview=content[:3000],
    )