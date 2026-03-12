import re
from pathlib import Path

from ctxprompt.models import FileInfo, SymbolInfo


IMPORT_PATTERNS = [
    re.compile(r'^\s*import\s+.*?from\s+[\'"](.+?)[\'"]', re.MULTILINE),
    re.compile(r'^\s*const\s+.*?=\s*require\([\'"](.+?)[\'"]\)', re.MULTILINE),
]

SYMBOL_PATTERNS = [
    ("class", re.compile(r'^\s*export\s+class\s+([A-Za-z_][A-Za-z0-9_]*)', re.MULTILINE)),
    ("class", re.compile(r'^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)', re.MULTILINE)),
    ("function", re.compile(r'^\s*export\s+function\s+([A-Za-z_][A-Za-z0-9_]*)', re.MULTILINE)),
    ("function", re.compile(r'^\s*export\s+default\s+function\s+([A-Za-z_][A-Za-z0-9_]*)', re.MULTILINE)),
    ("function", re.compile(r'^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', re.MULTILINE)),
    ("const", re.compile(r'^\s*export\s+const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=', re.MULTILINE)),
    ("const", re.compile(r'^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=', re.MULTILINE)),
]

ROUTE_PATTERN = re.compile(
    r'\b(app|router)\.(get|post|put|patch|delete)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
)

MOUNT_PATTERN = re.compile(
    r'\bapp\.use\s*\(\s*[\'"`]([^\'"`]+)[\'"`]\s*,\s*([A-Za-z0-9_]+)'
)

def detect_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".ts":
        return "typescript"
    if suffix == ".tsx":
        return "tsx"
    if suffix == ".js":
        return "javascript"
    if suffix == ".jsx":
        return "jsx"
    return "text"


def extract_node_file(path: Path, root: Path, priority: int) -> FileInfo:
    content = path.read_text(encoding="utf-8", errors="ignore")

    imports: list[str] = []
    for pattern in IMPORT_PATTERNS:
        imports.extend(pattern.findall(content))

    symbols: list[SymbolInfo] = []
    seen: set[tuple[str, str]] = set()

    for kind, pattern in SYMBOL_PATTERNS:
        for match in pattern.findall(content):
            key = (kind, match)
            if key in seen:
                continue
            seen.add(key)
            symbols.append(SymbolInfo(name=match, kind=kind))

    for match in ROUTE_PATTERN.finditer(content):
        method = match.group(2).upper()
        route = match.group(3)

        symbols.append(
            SymbolInfo(
                name=f"{method} {route}",
                kind="route",
            )
        )

    for prefix, router in MOUNT_PATTERN.findall(content):
        symbols.append(
            SymbolInfo(
                name=f"{prefix} -> {router}",
                kind="router_mount",
            )
        )
    

    return FileInfo(
        path=path,
        rel_path=str(path.relative_to(root)),
        language=detect_language(path),
        file_type="source",
        priority=priority,
        size_bytes=path.stat().st_size,
        imports=imports[:50],
        symbols=symbols[:50],
        content_preview=content[:3000],
    )