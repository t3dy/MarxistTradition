#!/usr/bin/env python3
"""Generate scaffold markdown files for the wonks (policy critique) category."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TXT_FILE = ROOT / "wonk.txt"
CONTENT_DIR = ROOT / "content" / "wonks"

# Policy area tags derived from content
POLICY_AREAS = {
    "housing": ["YIMBY", "NIMBY", "Zoning", "Density", "Housing Vouchers", "Financialization of Housing", "Opportunity Zones", "Real Estate Tax", "Suburbanization"],
    "climate": ["Electric Cars", "Carbon Markets", "Green New Deal", "Electric Vehicle", "Climate Adaptation", "Data Centers and Energy"],
    "labor": ["Gig Economy", "Universal Basic Income", "Labor Market Flexibility", "Workforce Development", "Automation Policy"],
    "technology": ["Tech Sector", "Startup Culture", "Urban Tech", "AI Governance", "Logistics Infrastructure", "Municipal Tech"],
    "fiscal policy": ["Corporate Tax", "Capital Gains", "Tax Write-Offs", "Tax Credits", "Municipal Budget", "Pension Fund"],
    "trade": ["Supply Chain", "Globalization and Trade", "Industrial Policy"],
    "finance": ["Deregulation of Financial", "Central Bank", "Inflation Policy", "Venture Capital"],
    "infrastructure": ["Public Transit", "Infrastructure Investment", "High-Speed Rail"],
    "education": ["Education Policy"],
    "health": ["Pharmaceutical"],
    "IP": ["Intellectual Property"],
    "privatization": ["Privatization of Public"],
    "ideology": ["Abundance Agenda", "Ideology of", "Ezra Klein"],
}


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"['''\"]", "", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def classify_policy_area(title):
    for area, keywords in POLICY_AREAS.items():
        for kw in keywords:
            if kw.lower() in title.lower():
                return area
    return "political economy"


def derive_tags(title, outline):
    tags = set()
    tag_keywords = {
        "housing": ["housing", "zoning", "rent", "YIMBY", "NIMBY", "density", "landlord"],
        "climate": ["carbon", "green", "climate", "electric", "energy", "emissions"],
        "labor": ["labor", "work", "gig", "UBI", "wage", "precarity"],
        "technology": ["tech", "AI", "digital", "platform", "startup", "data"],
        "finance": ["financial", "bank", "credit", "speculation", "capital markets"],
        "infrastructure": ["transit", "rail", "infrastructure"],
        "privatization": ["privatization", "outsourcing"],
        "ideology": ["ideology", "technocratic", "pragmatism"],
        "monopoly": ["monopoly", "antitrust"],
        "state": ["state", "subsidies", "tax"],
        "class": ["class", "accumulation", "surplus"],
    }
    combined = f"{title} {outline}".lower()
    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw.lower() in combined:
                tags.add(tag)
                break
    return sorted(tags) or ["political economy"]


def infer_related_terms(title, outline):
    """Map to existing dictionary term slugs."""
    related = []
    mapping = {
        "housing": "rent-theory",
        "rent": "rent-theory",
        "commodity": "commodity",
        "surplus": "surplus-value",
        "accumulation": "primitive-accumulation",
        "monopoly": "monopoly",
        "finance": "financialisation",
        "class": "class-analysis",
        "labor": "exploitation",
        "wage": "wage-system",
        "ideology": "ideology",
        "state": "state-theory",
        "capital fix": "crisis-theory",
        "imperialism": "imperialism",
    }
    combined = f"{title} {outline}".lower()
    for keyword, slug in mapping.items():
        if keyword in combined and slug not in related:
            related.append(slug)
    return related[:5]


def parse_wonk_txt(filepath):
    """Parse wonk.txt into list of {title, outline}."""
    entries = []
    lines = filepath.read_text(encoding="utf-8").strip().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("Outline:"):
            # This shouldn't happen at start, but just in case
            i += 1
            continue
        # This is a title line
        title = line
        outline = ""
        if i + 1 < len(lines) and lines[i + 1].strip().startswith("Outline:"):
            outline = lines[i + 1].strip().replace("Outline: ", "").replace("Outline:", "")
            i += 2
        else:
            i += 1
        entries.append({"title": title, "outline": outline})
    return entries


def generate_wonk_md(entry):
    title = entry["title"]
    outline = entry["outline"]
    slug = slugify(title)
    policy_area = classify_policy_area(title)
    tags = derive_tags(title, outline)
    related_terms = infer_related_terms(title, outline)

    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'policy_area: "{policy_area}"')
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append("traditions:")
    lines.append('  classical: "TODO"')
    lines.append('  value-form: "TODO"')
    lines.append('  harvey: "TODO"')
    lines.append('  structuralist: "TODO"')
    if related_terms:
        lines.append(f"related_terms: [{', '.join(related_terms)}]")
    lines.append("---")
    lines.append("")
    if outline:
        lines.append(f"<!-- Outline: {outline} -->")
        lines.append("")
    lines.append("<!-- TODO: Write body -->")
    lines.append("")
    return slug, "\n".join(lines)


def main():
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    entries = parse_wonk_txt(TXT_FILE)
    created = 0
    for entry in entries:
        slug, content = generate_wonk_md(entry)
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            created += 1
    print(f"Created {created} wonk scaffolds from {len(entries)} entries")


if __name__ == "__main__":
    main()
