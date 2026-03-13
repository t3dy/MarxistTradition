#!/usr/bin/env python3
"""Generate a prompt for a batch of entries to be processed by an agent."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"


def read_frontmatter(filepath):
    """Read frontmatter from a markdown file."""
    content = filepath.read_text(encoding="utf-8")
    if "---" not in content:
        return ""
    parts = content.split("---")
    if len(parts) >= 2:
        return parts[1].strip()
    return ""


def main():
    if len(sys.argv) < 3:
        print("Usage: python batch_prompt.py <start_batch> <end_batch>")
        sys.exit(1)

    start = int(sys.argv[1])  # 1-indexed
    end = int(sys.argv[2])    # 1-indexed, inclusive

    with open(Path(__file__).resolve().parent / "todo_batches.json") as f:
        data = json.load(f)

    entries = []
    for i in range(start - 1, min(end, len(data["batches"]))):
        entries.extend(data["batches"][i])

    # Filter to only entries that still have TODOs
    todo_entries = []
    for entry in entries:
        filepath = CONTENT_DIR / entry["category"] / f"{entry['slug']}.md"
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            if "<!-- TODO:" in content:
                fm = read_frontmatter(filepath)
                todo_entries.append({**entry, "frontmatter_text": fm})

    if not todo_entries:
        print("No TODO entries found in this range.")
        sys.exit(0)

    # Build prompt
    print(f"Processing {len(todo_entries)} entries (batches {start}-{end}):\n")
    for i, entry in enumerate(todo_entries, 1):
        cat = entry["category"]
        slug = entry["slug"]
        fm = entry["frontmatter_text"]
        # Extract key info from frontmatter
        print(f"{i}. {cat}/{slug}")
        # Show relevant frontmatter lines
        for line in fm.split("\n"):
            line = line.strip()
            if line and not line.startswith("traditions:") and not line.startswith("classical:") and not line.startswith("value-form:"):
                print(f"   {line}")
        print()


if __name__ == "__main__":
    main()
