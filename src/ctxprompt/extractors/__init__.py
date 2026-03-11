from pathlib import Path

from ctxprompt.models import FileInfo
from ctxprompt.extractors.python_extractor import extract_python_file


def extract_file(path: Path, root: Path, priority: int) -> FileInfo:
    suffix = path.suffix.lower()

    if suffix == ".py":
        return extract_python_file(path, root, priority)

    content = path.read_text(encoding="utf-8", errors="ignore")
    return FileInfo(
        path=path,
        rel_path=str(path.relative_to(root)),
        language="text",
        file_type="doc" if suffix in {".md", ".txt", ".rst"} else "config",
        priority=priority,
        size_bytes=path.stat().st_size,
        content_preview=content[:3000],
    )