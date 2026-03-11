from pathlib import Path
import json
import tomllib

from ctxprompt.models import SubprojectInfo


def _detect_node_project(project_root: Path, rel_path: str) -> SubprojectInfo | None:
    package_json = project_root / "package.json"
    if not package_json.exists():
        return None

    info = SubprojectInfo(
        root=project_root,
        rel_path=rel_path,
        manifests=["package.json"],
    )

    info.stacks.append("node")

    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except Exception:
        data = {}

    scripts = data.get("scripts", {})
    deps = set(data.get("dependencies", {})) | set(data.get("devDependencies", {}))

    if (project_root / "pnpm-lock.yaml").exists():
        info.package_managers.append("pnpm")
    elif (project_root / "yarn.lock").exists():
        info.package_managers.append("yarn")
    elif (project_root / "package-lock.json").exists():
        info.package_managers.append("npm")
    else:
        info.package_managers.append("npm")

    if "typescript" in deps:
        info.stacks.append("typescript")
    else:
        info.stacks.append("javascript")

    if "react" in deps:
        info.notes.append("React detected")
    if "vite" in deps:
        info.notes.append("Vite detected")
    if "next" in deps:
        info.notes.append("Next.js detected")
    if "@nestjs/core" in deps:
        info.notes.append("NestJS detected")
    if "express" in deps:
        info.notes.append("Express detected")
    if "@prisma/client" in deps or "prisma" in deps:
        info.notes.append("Prisma detected")

    pm = info.package_managers[0]

    for cmd in ("dev", "start", "build", "preview"):
        if cmd in scripts:
            info.run_commands.append(f"{rel_path}: {pm} run {cmd}" if rel_path != "." else f"{pm} run {cmd}")

    for cmd in ("test", "lint"):
        if cmd in scripts:
            info.test_commands.append(f"{rel_path}: {pm} run {cmd}" if rel_path != "." else f"{pm} run {cmd}")

    candidates = [
        "src/main.ts",
        "src/index.ts",
        "src/server.ts",
        "src/app.ts",
        "main.ts",
        "index.ts",
        "server.ts",
        "app.ts",
        "src/main.js",
        "src/index.js",
        "src/server.js",
        "src/app.js",
        "main.js",
        "index.js",
        "server.js",
        "app.js",
    ]

    for candidate in candidates:
        if (project_root / candidate).exists():
            info.entrypoints.append(candidate)

    return info


def _detect_python_project(project_root: Path, rel_path: str) -> SubprojectInfo | None:
    pyproject = project_root / "pyproject.toml"
    requirements = project_root / "requirements.txt"

    if not pyproject.exists() and not requirements.exists():
        return None

    info = SubprojectInfo(root=project_root, rel_path=rel_path)

    if pyproject.exists():
        info.manifests.append("pyproject.toml")
    if requirements.exists():
        info.manifests.append("requirements.txt")

    info.stacks.append("python")

    if (project_root / "uv.lock").exists():
        info.package_managers.append("uv")
    elif (project_root / "poetry.lock").exists():
        info.package_managers.append("poetry")
    else:
        info.package_managers.append("pip")

    if pyproject.exists():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            project = data.get("project", {})
            deps = project.get("dependencies", [])
            dep_text = " ".join(deps).lower() if isinstance(deps, list) else ""
            if "fastapi" in dep_text:
                info.notes.append("FastAPI detected")
            if "django" in dep_text:
                info.notes.append("Django detected")
            if "flask" in dep_text:
                info.notes.append("Flask detected")
        except Exception:
            pass

    candidates = [
        "main.py",
        "app.py",
        "manage.py",
        "server.py",
        "src/main.py",
        "src/app.py",
    ]

    for candidate in candidates:
        if (project_root / candidate).exists():
            info.entrypoints.append(candidate)

    return info


def detect_subprojects(root: Path, files: list[Path]) -> list[SubprojectInfo]:
    candidate_roots: set[Path] = set()

    for file_path in files:
        name = file_path.name
        if name in {"package.json", "pyproject.toml", "requirements.txt"}:
            candidate_roots.add(file_path.parent)

    if root in candidate_roots:
        ordered_roots = [root] + sorted(p for p in candidate_roots if p != root)
    else:
        ordered_roots = sorted(candidate_roots)

    subprojects: list[SubprojectInfo] = []

    for project_root in ordered_roots:
        rel_path = "." if project_root == root else str(project_root.relative_to(root))

        detected = _detect_node_project(project_root, rel_path)
        if detected is None:
            detected = _detect_python_project(project_root, rel_path)

        if detected is not None:
            subprojects.append(detected)

    return subprojects


def summarize_repo_stack(subprojects: list[SubprojectInfo]) -> dict:
    stacks: list[str] = []
    package_managers: list[str] = []
    notes: list[str] = []

    for subproject in subprojects:
        stacks.extend(subproject.stacks)
        package_managers.extend(subproject.package_managers)
        notes.extend(subproject.notes)

    return {
        "stacks": list(dict.fromkeys(stacks)),
        "package_managers": list(dict.fromkeys(package_managers)),
        "notes": list(dict.fromkeys(notes)),
    }