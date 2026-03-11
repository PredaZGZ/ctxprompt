import ast
from pathlib import Path

from ctxprompt.models import FileInfo, SymbolInfo


def extract_python_file(path: Path, root: Path, priority: int) -> FileInfo:
    content = path.read_text(encoding="utf-8", errors="ignore")
    imports: list[str] = []
    symbols: list[SymbolInfo] = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return FileInfo(
            path=path,
            rel_path=str(path.relative_to(root)),
            language="python",
            file_type="source",
            priority=priority,
            size_bytes=path.stat().st_size,
            content_preview=content[:3000],
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

        elif isinstance(node, ast.ClassDef):
            symbols.append(
                SymbolInfo(
                    name=node.name,
                    kind="class",
                    line_start=getattr(node, "lineno", None),
                    line_end=getattr(node, "end_lineno", None),
                )
            )

        elif isinstance(node, ast.FunctionDef):
            symbols.append(
                SymbolInfo(
                    name=node.name,
                    kind="function",
                    line_start=getattr(node, "lineno", None),
                    line_end=getattr(node, "end_lineno", None),
                )
            )

        elif isinstance(node, ast.AsyncFunctionDef):
            symbols.append(
                SymbolInfo(
                    name=node.name,
                    kind="async_function",
                    line_start=getattr(node, "lineno", None),
                    line_end=getattr(node, "end_lineno", None),
                )
            )

    return FileInfo(
        path=path,
        rel_path=str(path.relative_to(root)),
        language="python",
        file_type="source",
        priority=priority,
        size_bytes=path.stat().st_size,
        imports=imports[:50],
        symbols=symbols[:50],
        content_preview=content[:3000],
    )