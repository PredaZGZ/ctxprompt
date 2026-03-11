from pathlib import Path

from ctxprompt.models import FileInfo


def build_prompt(root: Path, stack_info: dict, key_files: list[FileInfo]) -> str:
    lines: list[str] = []

    lines.append("[PROJECT CONTEXT]")
    lines.append(f"Root path: {root}")
    lines.append("")

    lines.append("[STACK]")
    lines.append(
        f"Detected stacks: {', '.join(stack_info['stacks']) if stack_info['stacks'] else 'unknown'}"
    )
    lines.append(
        f"Package managers: {', '.join(stack_info['package_managers']) if stack_info['package_managers'] else 'unknown'}"
    )

    if stack_info["entrypoints"]:
        lines.append(f"Entrypoints: {', '.join(stack_info['entrypoints'])}")

    if stack_info["run_commands"]:
        lines.append(f"Run commands: {', '.join(stack_info['run_commands'])}")

    if stack_info["test_commands"]:
        lines.append(f"Test commands: {', '.join(stack_info['test_commands'])}")

    if stack_info["notes"]:
        lines.append(f"Notes: {'; '.join(stack_info['notes'])}")

    lines.append("")

    lines.append("[KEY FILES]")
    for file_info in key_files[:12]:
        lines.append(f"- {file_info.rel_path} [{file_info.language}] priority={file_info.priority}")

        if file_info.symbols:
            symbol_names = ", ".join(symbol.name for symbol in file_info.symbols[:8])
            lines.append(f"  symbols: {symbol_names}")

        if file_info.imports:
            import_names = ", ".join(file_info.imports[:8])
            lines.append(f"  imports: {import_names}")

    lines.append("")

    lines.append("[IMPORTANT SNIPPETS]")
    for file_info in key_files[:5]:
        preview = file_info.content_preview.strip()
        if not preview:
            continue

        lines.append(f"--- FILE: {file_info.rel_path} ---")
        lines.append(preview)
        lines.append("")

    lines.append("[INSTRUCTION]")
    lines.append(
        "Use this context to understand the repository structure, important files, symbols, "
        "and execution setup. Reference file paths explicitly when explaining the project or proposing changes."
    )

    return "\n".join(lines)