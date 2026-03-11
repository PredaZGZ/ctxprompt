from pathlib import Path

from ctxprompt.models import FileInfo, SubprojectInfo


def build_prompt(
    root: Path,
    stack_info: dict,
    subprojects: list[SubprojectInfo],
    key_files: list[FileInfo],
) -> str:
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
    if stack_info["notes"]:
        lines.append(f"Notes: {'; '.join(stack_info['notes'])}")
    lines.append("")

    if subprojects:
        lines.append("[SUBPROJECTS]")
        for subproject in subprojects:
            lines.append(f"- {subproject.rel_path}")
            lines.append(f"  stacks: {', '.join(subproject.stacks) if subproject.stacks else 'unknown'}")
            lines.append(
                f"  package managers: {', '.join(subproject.package_managers) if subproject.package_managers else 'unknown'}"
            )
            if subproject.entrypoints:
                lines.append(f"  entrypoints: {', '.join(subproject.entrypoints)}")
            if subproject.run_commands:
                lines.append(f"  run commands: {', '.join(subproject.run_commands)}")
            if subproject.test_commands:
                lines.append(f"  test commands: {', '.join(subproject.test_commands)}")
            if subproject.notes:
                lines.append(f"  notes: {'; '.join(subproject.notes)}")
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
        "Use this context to understand the repository structure, subprojects, important files, "
        "symbols, and execution setup. Reference file paths explicitly when explaining the project "
        "or proposing changes."
    )

    return "\n".join(lines)