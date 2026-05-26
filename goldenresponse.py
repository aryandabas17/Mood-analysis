"""
Golden Response code bundle for the Mood-analysis repository.

This script gathers all source/text code files from the project and exposes:
- PROJECT_CODE: dict[path, file_contents]
- COMBINED_CODE: one large combined string with file headers

Run:
    python goldenresponse.py
to regenerate and print/save the full combined code snapshot.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parent

# Include source/config/docs text files. Exclude generated/build/binary/secret folders.
INCLUDE_SUFFIXES = {
    ".js",
    ".ts",
    ".tsx",
    ".json",
    ".md",
    ".css",
    ".py",
    ".yml",
    ".yaml",
    ".txt",
    ".d.ts",
}

EXCLUDE_PARTS = {
    ".git",
    "node_modules",
    ".next",
    "out",
    "__pycache__",
    ".idea",
    ".vscode",
}

EXCLUDE_FILES = {
    "Golden Response/backend/.env",
    "Golden Response/frontend/.env.local",
    "Golden Response/backend/data/sessions.json",
}


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDE_FILES:
        return False
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if path.name == "goldenresponse.py":
        return False
    if path.suffix in INCLUDE_SUFFIXES:
        return True
    # Handle extension-less important files.
    if path.name in {".gitignore", ".env.example"}:
        return True
    return False


def collect_project_code() -> Dict[str, str]:
    collected: Dict[str, str] = {}
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        if not should_include(p):
            continue
        rel = p.relative_to(ROOT).as_posix()
        try:
            collected[rel] = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Skip non-text files safely.
            continue
    return collected


def build_combined_code(code_map: Dict[str, str]) -> str:
    sections = []
    for rel_path, content in code_map.items():
        sections.append(f"# ===== FILE: {rel_path} =====\n{content}\n")
    return "\n".join(sections).strip() + "\n"


PROJECT_CODE = collect_project_code()
COMBINED_CODE = build_combined_code(PROJECT_CODE)


def save_snapshot(output_file: str = "goldenresponse_snapshot.txt") -> Path:
    out_path = ROOT / output_file
    out_path.write_text(COMBINED_CODE, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    snapshot = save_snapshot()
    print(f"Collected {len(PROJECT_CODE)} files.")
    print(f"Snapshot written to: {snapshot}")
