from pathlib import Path


KEY_FILENAMES = {
    "readme.md": 100,
    "package.json": 100,
    "pyproject.toml": 100,
    "requirements.txt": 95,
    "dockerfile": 90,
    ".env.example": 85,
    "docker-compose.yml": 90,
    "docker-compose.yaml": 90,
    "schema.prisma": 90,
    "main.py": 85,
    "app.py": 85,
    "manage.py": 85,
    "server.py": 85,
    "index.ts": 80,
    "index.js": 80,
    "main.ts": 85,
}


def score_file(path: Path, root: Path) -> int:
    name = path.name.lower()
    rel_path = path.relative_to(root)
    rel = str(rel_path).lower()
    depth = len(rel_path.parts)

    score = KEY_FILENAMES.get(name, 10)

    if depth == 1:
        score += 20
    elif depth == 2:
        score += 10
    else:
        score -= min(depth * 2, 12)

    if rel.startswith("src/"):
        score += 10

    if rel.startswith("tests/") or "/tests/" in rel:
        score -= 15

    if rel.startswith("docs/") or "/docs/" in rel:
        score += 5

    if rel.endswith(".py"):
        score += 8
    elif rel.endswith(".ts"):
        score += 8
    elif rel.endswith(".js"):
        score += 6
    elif rel.endswith(".md"):
        score += 4
    elif rel.endswith(".toml"):
        score += 4
    elif rel.endswith(".json"):
        score += 4
    elif rel.endswith(".prisma"):
        score += 6

    if name == "readme.md" and depth > 1:
        score -= 20

    return score