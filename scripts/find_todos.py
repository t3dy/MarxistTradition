#!/usr/bin/env python3
"""Find all scaffold files that still have TODO placeholders, grouped into batches."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT = Path(__file__).resolve().parent / "todo_batches.json"
BATCH_SIZE = 10


def main():
    todos = []
    for category in ["terms", "texts", "thinkers"]:
        cat_dir = CONTENT_DIR / category
        for filepath in sorted(cat_dir.glob("*.md")):
            content = filepath.read_text(encoding="utf-8")
            if "<!-- TODO:" in content:
                todos.append({
                    "category": category,
                    "slug": filepath.stem,
                    "path": str(filepath.relative_to(ROOT)),
                    "frontmatter": content.split("---")[1].strip() if "---" in content else ""
                })

    # Split into batches
    batches = []
    for i in range(0, len(todos), BATCH_SIZE):
        batches.append(todos[i:i + BATCH_SIZE])

    result = {
        "total_todos": len(todos),
        "batch_count": len(batches),
        "batch_size": BATCH_SIZE,
        "batches": batches
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Found {len(todos)} TODO files in {len(batches)} batches of {BATCH_SIZE}")
    # Breakdown by category
    by_cat = {}
    for t in todos:
        by_cat[t["category"]] = by_cat.get(t["category"], 0) + 1
    for cat, count in sorted(by_cat.items()):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
