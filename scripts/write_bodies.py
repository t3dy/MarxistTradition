#!/usr/bin/env python3
"""
Parse agent output and write body text back into scaffold markdown files.
Input: a text file with entries in this format:

===ENTRY: [slug]===
BODY: [paragraph]
CLASSICAL: [text]
VALUE-FORM: [text]
===END===
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"


def parse_entries(text):
    """Parse the agent output format into {slug: {body, classical, value_form}}."""
    entries = {}
    pattern = r'===ENTRY:\s*(.+?)\s*===\s*\nBODY:\s*(.*?)\nCLASSICAL:\s*(.*?)\nVALUE-FORM:\s*(.*?)\n===END==='
    for match in re.finditer(pattern, text, re.DOTALL):
        raw_slug = match.group(1).strip()
        # Handle "category/slug" or just "slug" format
        slug = raw_slug.split("/")[-1] if "/" in raw_slug else raw_slug
        category_hint = raw_slug.split("/")[0] if "/" in raw_slug else None
        entries[slug] = {
            "body": match.group(2).strip(),
            "classical": match.group(3).strip(),
            "value_form": match.group(4).strip(),
        }
    return entries


def write_to_file(slug, category, data):
    """Write body and tradition text into the scaffold file."""
    filepath = CONTENT_DIR / category / f"{slug}.md"
    if not filepath.exists():
        print(f"  SKIP (not found): {filepath}")
        return False

    content = filepath.read_text(encoding="utf-8")
    if "<!-- TODO:" not in content:
        print(f"  SKIP (already done): {slug}")
        return False

    # Replace tradition TODOs
    content = content.replace(
        '  classical: "TODO"',
        f'  classical: "{data["classical"]}"'
    )
    content = content.replace(
        '  value-form: "TODO"',
        f'  value-form: "{data["value_form"]}"'
    )

    # Replace body TODO
    content = content.replace("<!-- TODO: Write body -->", data["body"])

    # Also handle consolidation comments before body
    content = re.sub(r'<!-- Consolidates:.*?-->\n\n<!-- TODO: Write body -->', data["body"], content)

    filepath.write_text(content, encoding="utf-8")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python write_bodies.py <output_file>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    text = input_file.read_text(encoding="utf-8")
    entries = parse_entries(text)

    print(f"Parsed {len(entries)} entries")

    written = 0
    for slug, data in entries.items():
        # Try each category
        for category in ["terms", "texts", "thinkers"]:
            filepath = CONTENT_DIR / category / f"{slug}.md"
            if filepath.exists():
                if write_to_file(slug, category, data):
                    written += 1
                    print(f"  OK: {category}/{slug}")
                break
        else:
            print(f"  NOT FOUND: {slug}")

    print(f"\nWrote {written}/{len(entries)} entries")


if __name__ == "__main__":
    main()
