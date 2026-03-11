from pathlib import Path
import json
import tomllib


def detect_stack(root: Path) -> dict:
    stacks = []
    package_managers = []
    entrypoints = []
    run_commands = []
    test_commands = []
    notes = []

    package_json = root / "package.json"
    pyproject = root / "pyproject.toml"
    requirements = root / "requirements.txt"

    # Node detection
    if package_json.exists():
        stacks.append("node")

        try:
            data = json.loads(package_json.read_text())
        except Exception:
            data = {}

        scripts = data.get("scripts", {})
        deps = set(data.get("dependencies", {})) | set(data.get("devDependencies", {}))

        if (root / "pnpm-lock.yaml").exists():
            package_managers.append("pnpm")
        elif (root / "yarn.lock").exists():
            package_managers.append("yarn")
        elif (root / "package-lock.json").exists():
            package_managers.append("npm")

        if "typescript" in deps:
            stacks.append("typescript")
        else:
            stacks.append("javascript")

        pm = package_managers[0] if package_managers else "npm"

        for cmd in ("dev", "start", "build"):
            if cmd in scripts:
                run_commands.append(f"{pm} run {cmd}")

        for cmd in ("test", "lint"):
            if cmd in scripts:
                test_commands.append(f"{pm} run {cmd}")

    # Python detection
    if pyproject.exists():
        stacks.append("python")

        if (root / "uv.lock").exists():
            package_managers.append("uv")
        elif (root / "poetry.lock").exists():
            package_managers.append("poetry")
        else:
            package_managers.append("pip")

    elif requirements.exists():
        stacks.append("python")
        package_managers.append("pip")

    # entrypoints
    candidates = [
        "main.py",
        "app.py",
        "manage.py",
        "server.py",
        "index.js",
        "index.ts",
        "src/main.ts",
        "src/index.ts",
    ]

    for name in candidates:
        if (root / name).exists():
            entrypoints.append(name)

    return {
        "stacks": list(dict.fromkeys(stacks)),
        "package_managers": list(dict.fromkeys(package_managers)),
        "entrypoints": entrypoints,
        "run_commands": run_commands,
        "test_commands": test_commands,
        "notes": notes,
    }