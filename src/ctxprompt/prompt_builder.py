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

    display_subprojects = subprojects
    if len(subprojects) == 1 and subprojects[0].rel_path == ".":
        display_subprojects = []

    if display_subprojects:
        lines.append("[SUBPROJECTS]")
        for subproject in display_subprojects:
            lines.append(f"- {subproject.rel_path}")
            lines.append(
                f"  stacks: {', '.join(subproject.stacks) if subproject.stacks else 'unknown'}"
            )
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
    for file_info in key_files:
        lines.append(f"- {file_info.rel_path} priority={file_info.priority}")

        routes = [s.name for s in file_info.symbols if s.kind == "route"]
        mounts = [s.name for s in file_info.symbols if s.kind == "router_mount"]
        others = [s.name for s in file_info.symbols if s.kind not in ("route", "router_mount")]

        if routes:
            lines.append(f"  routes: {', '.join(routes[:20])}")

        if mounts:
            lines.append(f"  routers: {', '.join(mounts[:20])}")

        if others:
            lines.append(f"  symbols: {', '.join(others[:10])}")

        if file_info.imports:
            import_names = ", ".join(file_info.imports[:8])
            lines.append(f"  imports: {import_names}")

    lines.append("")

    # lines.append("[IMPORTANT SNIPPETS]")
    # for file_info in key_files[:5]:
    #     preview = file_info.content_preview.strip()
    #     if not preview:
    #         continue
    # 
    #     lines.append(f"--- FILE: {file_info.rel_path} ---")
    #     lines.append(preview)
    #     lines.append("")

    lines.append("[INSTRUCTION]")
    
    has_api = any(
        s.kind in ("route", "router_mount") for f in key_files for s in f.symbols
    ) or any(
        api_kw in " ".join(stack_info.get("stacks", [])).lower()
        for api_kw in ("fastapi", "flask", "django", "express", "nest", "spring", "actix", "axum")
    )

    if has_api:
        api_msg = "This repository contains an API. Use the context to understand the API routes, routers, key symbols, and backend behavior."
    else:
        api_msg = "Use this context to understand the repository structure, key symbols, and execution setup."

    lines.append(
        f"{api_msg} IMPORTANT: This is PURE CONTEXT. Do not hallucinate file contents or implementations. "
        "If you have any doubts or need the code of a specific file or function to answer the user's prompt, "
        "STOP and ask the user to provide that file or function first."
    )

    return "\n".join(lines)