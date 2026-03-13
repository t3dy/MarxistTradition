#!/usr/bin/env python3
"""Generate scaffold markdown files for Frankfurt School texts."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "texts"


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"['''\"]", "", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


TEXTS = [
    {"title": "Dialectic of Enlightenment", "author": "Max Horkheimer and Theodor Adorno", "year": 1944, "tradition": "Frankfurt School", "tags": ["critical theory", "culture industry", "enlightenment", "domination"], "note": "Foundational text arguing that Enlightenment rationality contains the seeds of its own regression into myth and domination; introduces the concept of the culture industry"},
    {"title": "Minima Moralia", "author": "Theodor Adorno", "year": 1951, "tradition": "Frankfurt School", "tags": ["critical theory", "damaged life", "aphorism", "alienation"], "note": "Reflections from damaged life; aphoristic critique of everyday existence under late capitalism from exile"},
    {"title": "Negative Dialectics", "author": "Theodor Adorno", "year": 1966, "tradition": "Frankfurt School", "tags": ["dialectics", "identity thinking", "non-identity", "philosophy"], "note": "Adorno's major philosophical work rejecting Hegelian synthesis in favor of non-identity thinking and the primacy of the object"},
    {"title": "Aesthetic Theory", "author": "Theodor Adorno", "year": 1970, "tradition": "Frankfurt School", "tags": ["aesthetics", "art", "autonomy", "commodity"], "note": "Posthumous work on art's truth content and its resistance to commodity form; art as the last refuge of non-instrumental reason"},
    {"title": "The Authoritarian Personality", "author": "Theodor Adorno et al.", "year": 1950, "tradition": "Frankfurt School", "tags": ["fascism", "psychology", "authoritarianism", "ideology"], "note": "Empirical study of the psychological dispositions underlying fascist susceptibility; the F-scale and authoritarian character structure"},
    {"title": "Eclipse of Reason", "author": "Max Horkheimer", "year": 1947, "tradition": "Frankfurt School", "tags": ["instrumental reason", "critical theory", "enlightenment"], "note": "Analysis of the reduction of reason to instrumental rationality under capitalism; subjective vs objective reason"},
    {"title": "Traditional and Critical Theory", "author": "Max Horkheimer", "year": 1937, "tradition": "Frankfurt School", "tags": ["methodology", "critical theory", "positivism"], "note": "Programmatic essay distinguishing critical theory from traditional theory; theory oriented toward emancipation vs theory as contemplation"},
    {"title": "Eros and Civilization", "author": "Herbert Marcuse", "year": 1955, "tradition": "Frankfurt School", "tags": ["psychoanalysis", "liberation", "Freud", "surplus repression"], "note": "Synthesis of Marx and Freud arguing that advanced civilization makes possible the liberation of Eros from surplus repression"},
    {"title": "One-Dimensional Man", "author": "Herbert Marcuse", "year": 1964, "tradition": "Frankfurt School", "tags": ["one-dimensionality", "advanced capitalism", "ideology", "technology"], "note": "Analysis of how advanced industrial society integrates opposition and produces one-dimensional thought and behavior"},
    {"title": "An Essay on Liberation", "author": "Herbert Marcuse", "year": 1969, "tradition": "Frankfurt School", "tags": ["liberation", "new left", "revolution", "aesthetics"], "note": "Written in the context of 1968; argues for a new sensibility and biological foundation for socialism"},
    {"title": "The Structural Transformation of the Public Sphere", "author": "Jurgen Habermas", "year": 1962, "tradition": "Frankfurt School", "tags": ["public sphere", "democracy", "bourgeois society", "media"], "note": "Historical analysis of the rise and decline of the bourgeois public sphere as a space for rational-critical debate"},
    {"title": "Knowledge and Human Interests", "author": "Jurgen Habermas", "year": 1968, "tradition": "Frankfurt School", "tags": ["epistemology", "critique", "positivism", "interests"], "note": "Three knowledge-constitutive interests: technical, practical, and emancipatory; critique of positivism and scientism"},
    {"title": "The Theory of Communicative Action", "author": "Jurgen Habermas", "year": 1981, "tradition": "Frankfurt School", "tags": ["communicative rationality", "lifeworld", "system", "modernity"], "note": "Two-volume magnum opus developing communicative rationality against instrumental reason; system vs lifeworld colonization"},
    {"title": "Legitimation Crisis", "author": "Jurgen Habermas", "year": 1973, "tradition": "Frankfurt School", "tags": ["crisis", "legitimation", "late capitalism", "state"], "note": "Analysis of how late capitalism generates crises of economic, rationality, legitimation, and motivation that threaten systemic stability"},
    {"title": "The Work of Art in the Age of Mechanical Reproduction", "author": "Walter Benjamin", "year": 1935, "tradition": "Frankfurt School", "tags": ["art", "aura", "reproduction", "fascism"], "note": "Seminal essay on how mechanical reproduction destroys the aura of the artwork and transforms its political function"},
    {"title": "Theses on the Philosophy of History", "author": "Walter Benjamin", "year": 1940, "tradition": "Frankfurt School", "tags": ["history", "messianism", "progress", "revolution"], "note": "Benjamin's final work: the angel of history, jetztzeit, revolutionary interruption of progress; against historicism"},
    {"title": "The Arcades Project", "author": "Walter Benjamin", "year": 1940, "tradition": "Frankfurt School", "tags": ["modernity", "commodity", "phantasmagoria", "Paris"], "note": "Massive unfinished work on 19th-century Paris as the capital of modernity; dialectical images, wish-images, and the phantasmagoria of commodities"},
    {"title": "The Origin of German Tragic Drama", "author": "Walter Benjamin", "year": 1928, "tradition": "Frankfurt School", "tags": ["allegory", "baroque", "melancholy", "criticism"], "note": "Benjamin's rejected Habilitation thesis; the theory of allegory vs symbol and the Baroque mourning play as critique of sovereign power"},
    {"title": "Escape from Freedom", "author": "Erich Fromm", "year": 1941, "tradition": "Frankfurt School", "tags": ["freedom", "authoritarianism", "psychology", "fascism"], "note": "Analysis of why modern individuals flee from the burden of freedom into authoritarian submission; the social character under capitalism"},
    {"title": "The Sane Society", "author": "Erich Fromm", "year": 1955, "tradition": "Frankfurt School", "tags": ["alienation", "mental health", "capitalism", "humanism"], "note": "Argues that capitalist society itself is pathological and produces widespread alienation; humanistic socialism as remedy"},
    {"title": "The Jargon of Authenticity", "author": "Theodor Adorno", "year": 1964, "tradition": "Frankfurt School", "tags": ["existentialism", "Heidegger", "ideology", "language"], "note": "Critique of Heideggerian existentialism as ideological mystification; authenticity as false concreteness"},
    {"title": "Prisms", "author": "Theodor Adorno", "year": 1955, "tradition": "Frankfurt School", "tags": ["cultural criticism", "essays", "Kafka", "sociology"], "note": "Essay collection including 'Cultural Criticism and Society' with the famous dictum about poetry after Auschwitz"},
    {"title": "Philosophy of New Music", "author": "Theodor Adorno", "year": 1949, "tradition": "Frankfurt School", "tags": ["music", "Schoenberg", "Stravinsky", "modernism"], "note": "Schoenberg's atonality as truth content of the historical situation vs Stravinsky's neoclassicism as regression; music and social totality"},
    {"title": "Reason and Revolution", "author": "Herbert Marcuse", "year": 1941, "tradition": "Frankfurt School", "tags": ["Hegel", "Marx", "social theory", "dialectics"], "note": "Marcuse's reading of Hegel as critical social theorist; the dialectical tradition from Hegel through Marx as inherently revolutionary"},
    {"title": "Studies on Authority and the Family", "author": "Max Horkheimer (ed.)", "year": 1936, "tradition": "Frankfurt School", "tags": ["authority", "family", "psychoanalysis", "ideology"], "note": "Major collaborative research project of the Institute; how the family reproduces authoritarian character structures under capitalism"},
]


def generate_text_md(entry):
    slug = slugify(entry["title"])
    tags_str = ", ".join(entry["tags"])

    lines = ["---"]
    lines.append(f'title: "{entry["title"]}"')
    lines.append(f'author: "{entry["author"]}"')
    lines.append(f'year: {entry["year"]}')
    lines.append(f'tradition: "{entry["tradition"]}"')
    lines.append(f"tags: [{tags_str}]")
    lines.append("traditions:")
    lines.append('  classical: "TODO"')
    lines.append('  value-form: "TODO"')
    lines.append('  harvey: "TODO"')
    lines.append('  structuralist: "TODO"')
    lines.append("---")
    lines.append("")
    if entry.get("note"):
        lines.append(f"<!-- Note: {entry['note']} -->")
        lines.append("")
    lines.append("<!-- TODO: Write body -->")
    lines.append("")
    return slug, "\n".join(lines)


def main():
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for entry in TEXTS:
        slug, content = generate_text_md(entry)
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            created += 1
            print(f"  Created: {slug}")
        else:
            print(f"  Exists: {slug}")
    print(f"\nCreated {created} Frankfurt School text scaffolds from {len(TEXTS)} entries")


if __name__ == "__main__":
    main()
