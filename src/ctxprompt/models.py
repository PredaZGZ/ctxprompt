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


@dataclass
class SubprojectInfo:
    root: Path
    rel_path: str
    stacks: list[str] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    entrypoints: list[str] = field(default_factory=list)
    run_commands: list[str] = field(default_factory=list)
    test_commands: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    manifests: list[str] = field(default_factory=list)