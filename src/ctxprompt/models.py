from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SymbolInfo:
    name: str
    kind: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    signature: Optional[str] = None


@dataclass
class FileInfo:
    path: Path
    rel_path: str
    language: str
    file_type: str
    priority: int
    size_bytes: int
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    symbols: list[SymbolInfo] = field(default_factory=list)
    content_preview: str = ""
    summary: Optional[str] = None