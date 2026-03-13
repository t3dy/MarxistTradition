#!/usr/bin/env python3
"""
Generate markdown scaffold files from gap_report.json.
Creates files with complete frontmatter but placeholder body text.
"""

import json
import re
from pathlib import Path
from lookups import THINKER_DATA, TEXT_DATA, GERMAN_TERMS, TERM_SOURCES

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
GAP_REPORT = Path(__file__).resolve().parent / "gap_report.json"


def yaml_str(val):
    """Format a value for YAML output."""
    if isinstance(val, str):
        if any(c in val for c in ":#{}[]&*?|>!%@`,"):
            return f'"{val}"'
        return val
    return str(val)


def yaml_list(items, indent=2):
    """Format a list for YAML."""
    prefix = " " * indent
    return "\n".join(f"{prefix}- {yaml_str(item)}" for item in items)


def title_case(name):
    """Smart title case that handles special patterns."""
    words = name.split()
    small_words = {"of", "the", "and", "in", "on", "to", "for", "a", "an", "by", "vs", "or"}
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)


def infer_related(slug, all_slugs, existing_slugs):
    """Infer related terms from keyword overlap."""
    related = []
    keywords = set(slug.split("-"))
    # Remove very common words
    keywords -= {"of", "the", "and", "in", "on", "to", "for", "a", "theory", "debates"}

    all_available = existing_slugs | {s for s in all_slugs}
    for other in all_available:
        if other == slug:
            continue
        other_keywords = set(other.split("-"))
        if keywords & other_keywords and len(keywords & other_keywords) > 0:
            related.append(other)
        if len(related) >= 5:
            break
    return related[:5]


def generate_term(entry, all_slugs, existing_slugs):
    """Generate markdown for a term entry."""
    slug = entry["slug"]
    name = entry.get("name", title_case(slug.replace("-", " ")))
    display_name = title_case(name)
    german = GERMAN_TERMS.get(name.lower(), "")
    source = TERM_SOURCES.get(name.lower(), "")
    tags = entry.get("tags", ["theory"])
    related = infer_related(slug, all_slugs, existing_slugs)
    consolidates = entry.get("consolidates", [])

    lines = ["---"]
    lines.append(f"term: {yaml_str(display_name)}")
    if german:
        lines.append(f"german: {yaml_str(german)}")
    if source:
        lines.append(f'source: "{source}"')
    if related:
        lines.append(f"related: [{', '.join(related)}]")
    lines.append(f"tags: [{', '.join(yaml_str(t) for t in tags)}]")

    # Add traditions block with placeholders
    lines.append("traditions:")
    lines.append('  classical: "TODO"')
    lines.append('  value-form: "TODO"')

    lines.append("---")
    lines.append("")

    if consolidates:
        lines.append(f"<!-- Consolidates: {'; '.join(consolidates[:10])} -->")
        lines.append("")

    lines.append("<!-- TODO: Write body -->")
    lines.append("")

    return "\n".join(lines)


def generate_text(entry):
    """Generate markdown for a text entry."""
    name = entry["name"]
    data = TEXT_DATA.get(name, {})

    author = data.get("author", "Unknown")
    year = data.get("year", 0)
    tradition = data.get("tradition", "Classical Marxism")
    translations = data.get("translations", [])
    tags = data.get("tags", ["political economy"])

    lines = ["---"]
    lines.append(f'title: "{name}"')
    lines.append(f"author: {yaml_str(author)}")
    lines.append(f"year: {year}")
    lines.append(f"tradition: {yaml_str(tradition)}")
    if translations:
        lines.append("translations:")
        for t in translations:
            lines.append(f'  - "{t}"')
    lines.append("tags:")
    for t in tags:
        lines.append(f"  - {t}")
    lines.append("---")
    lines.append("")
    lines.append("<!-- TODO: Write body -->")
    lines.append("")

    return "\n".join(lines)


def generate_thinker(entry):
    """Generate markdown for a thinker entry."""
    name = entry["name"]
    data = THINKER_DATA.get(name, {})

    born = data.get("born", 0)
    died = data.get("died")
    nationality = data.get("nationality", "Unknown")
    tradition = data.get("tradition", "Marxism")
    key_works = data.get("key_works", [])
    tags = data.get("tags", ["theory"])

    lines = ["---"]
    lines.append(f"name: {yaml_str(name)}")
    lines.append(f"born: {born}")
    if died is not None:
        lines.append(f"died: {died}")
    else:
        lines.append("died: null")
    lines.append(f"nationality: {yaml_str(nationality)}")
    lines.append(f"tradition: {yaml_str(tradition)}")
    if key_works:
        lines.append("key_works:")
        for w in key_works:
            lines.append(f'  - "{w}"')
    lines.append("tags:")
    for t in tags:
        lines.append(f"  - {t}")
    lines.append("---")
    lines.append("")
    lines.append("<!-- TODO: Write body -->")
    lines.append("")

    return "\n".join(lines)


def main():
    with open(GAP_REPORT, "r", encoding="utf-8") as f:
        report = json.load(f)

    # Collect all slugs for cross-referencing
    existing_term_slugs = {f.stem for f in (CONTENT_DIR / "terms").glob("*.md")}
    all_new_term_slugs = {t["slug"] for t in report["new_terms"]}

    created = {"terms": 0, "texts": 0, "thinkers": 0}

    # Generate term files
    for entry in report["new_terms"]:
        filepath = CONTENT_DIR / "terms" / f"{entry['slug']}.md"
        if filepath.exists():
            continue
        content = generate_term(entry, all_new_term_slugs, existing_term_slugs)
        filepath.write_text(content, encoding="utf-8")
        created["terms"] += 1

    # Generate text files
    for entry in report["new_texts"]:
        filepath = CONTENT_DIR / "texts" / f"{entry['slug']}.md"
        if filepath.exists():
            continue
        content = generate_text(entry)
        filepath.write_text(content, encoding="utf-8")
        created["texts"] += 1

    # Generate thinker files
    for entry in report["new_thinkers"]:
        filepath = CONTENT_DIR / "thinkers" / f"{entry['slug']}.md"
        if filepath.exists():
            continue
        content = generate_thinker(entry)
        filepath.write_text(content, encoding="utf-8")
        created["thinkers"] += 1

    print(f"Created scaffolds:")
    for cat, count in created.items():
        print(f"  {cat}: {count} files")
    print(f"  total: {sum(created.values())}")


if __name__ == "__main__":
    main()
