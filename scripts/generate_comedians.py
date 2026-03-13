#!/usr/bin/env python3
"""Generate scaffold markdown files for the comedians category."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "comedians"


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"['''\"]", "", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


COMEDIANS = [
    # Stand-up
    {"title": "Larry David", "genre": "stand-up", "tags": ["class", "alienation", "bourgeois anxiety"], "note": "Curb Your Enthusiasm as a study in bourgeois neurosis, property relations, and the social contract of the owning class"},
    {"title": "Jerry Seinfeld", "genre": "stand-up", "tags": ["commodity fetishism", "ideology", "complicity"], "note": "Comedy about nothing as the commodification of everyday life; his complicity in Israeli genocide through public support and troop visits"},
    {"title": "Bill Hicks", "genre": "stand-up", "tags": ["anti-capitalism", "ideology critique", "media"], "note": "Radical critique of consumer capitalism, the military-industrial complex, and media manipulation"},
    {"title": "George Carlin", "genre": "stand-up", "tags": ["class consciousness", "anti-capitalism", "language"], "note": "Explicitly class-conscious comedy exposing ruling class ideology, language as social control, and the American Dream as false consciousness"},
    {"title": "Daniel Tosh", "genre": "stand-up", "tags": ["transgression", "commodity", "edgelord"], "note": "Comedy as commodity spectacle; transgression recuperated by capital; the edgelord as depoliticized rebellion"},
    {"title": "Chris Hardwick", "genre": "stand-up", "tags": ["nerd culture", "platform capitalism", "branding"], "note": "Nerd as brand identity; Nerdist as platform capitalism; the comedian as content entrepreneur"},
    {"title": "Nikki Glaser", "genre": "stand-up", "tags": ["gender", "commodity", "spectacle"], "note": "Gender performance as commodity; the sexual confession as marketized authenticity"},
    {"title": "Nick Kroll", "genre": "stand-up", "tags": ["class", "privilege", "satire"], "note": "Son of billionaire satirizing class; the limits of bourgeois self-parody; Big Mouth and the commodification of adolescence"},
    {"title": "Amy Schumer", "genre": "stand-up", "tags": ["feminism", "commodity", "liberal ideology"], "note": "Liberal feminism as commodity form; the limits of representational politics in comedy"},
    {"title": "Dave Chappelle", "genre": "stand-up", "tags": ["race", "class", "alienation", "commodity"], "note": "Racial capitalism and comedy; walking away from $50 million as refusal of commodification; later Netflix specials as reactionary turn"},
    {"title": "Richard Pryor", "genre": "stand-up", "tags": ["race", "class", "lumpenproletariat"], "note": "Comedy from the lumpenproletariat; race and class in American capitalism; the body as site of struggle"},
    {"title": "Hannah Gadsby", "genre": "stand-up", "tags": ["form", "ideology", "deconstruction"], "note": "Nanette as deconstruction of comedy's ideological form; refusing the tension-release commodity structure"},
    {"title": "Bo Burnham", "genre": "stand-up", "tags": ["alienation", "spectacle", "digital capitalism"], "note": "Inside as alienation under digital capitalism; the performer trapped in the commodity form; meta-comedy as ideology critique"},
    {"title": "Maria Bamford", "genre": "stand-up", "tags": ["mental health", "precarity", "alienation"], "note": "Mental illness under capitalism; the precarity of creative labor; Lady Dynamite and the comedy of dispossession"},
    {"title": "Marc Maron", "genre": "stand-up", "tags": ["labor", "precarity", "podcast economy"], "note": "WTF as labor of self-exposure; the podcast as means of production; precarity in the comedy industry"},
    {"title": "Hasan Minhaj", "genre": "stand-up", "tags": ["race", "imperialism", "liberal ideology"], "note": "Patriot Act as liberal critique within capitalist media; the fabrication scandal and authenticity as commodity"},
    {"title": "John Mulaney", "genre": "stand-up", "tags": ["nostalgia", "class", "bourgeois comedy"], "note": "Nostalgia as ideological form; the well-crafted joke as commodity; bourgeois comedy's appeal to order"},
    {"title": "Tig Notaro", "genre": "stand-up", "tags": ["vulnerability", "commodity", "authenticity"], "note": "Trauma as comedic commodity; authenticity and its market value; the economics of confessional performance"},
    {"title": "Mitch Hedberg", "genre": "stand-up", "tags": ["surrealism", "commodity", "form"], "note": "The one-liner as minimum viable comedy commodity; surrealism as escape from realist ideology"},
    {"title": "Patton Oswalt", "genre": "stand-up", "tags": ["nerd culture", "gentrification", "cultural capital"], "note": "Nerd culture and cultural capital; comedy gentrification; the comedian as cultural gatekeeper"},

    # Sketch and Troupe
    {"title": "Saturday Night Live", "genre": "sketch troupe", "tags": ["ideology", "spectacle", "recuperation"], "note": "SNL as ideological state apparatus of American liberalism; recuperation of dissent; the revolving door between comedy and power"},
    {"title": "Upright Citizens Brigade", "genre": "sketch troupe", "tags": ["labor", "exploitation", "training pipeline"], "note": "UCB as exploitative labor pipeline; free/cheap labor rebranded as training; the comedy-industrial complex"},
    {"title": "Second City TV (SCTV)", "genre": "sketch troupe", "tags": ["media critique", "Canadian", "spectacle"], "note": "Canadian perspective on American media spectacle; television satirizing television's commodity form"},
    {"title": "Kids in the Hall", "genre": "sketch troupe", "tags": ["gender", "surrealism", "Canadian"], "note": "Gender performance and drag as ideological disruption; surrealism against bourgeois realism; Canadian cultural production"},
    {"title": "Monty Python", "genre": "sketch troupe", "tags": ["class", "absurdism", "British"], "note": "Life of Brian as critique of organized religion and revolutionary sectarianism; class consciousness in British absurdism"},
    {"title": "Key and Peele", "genre": "sketch troupe", "tags": ["race", "class", "code-switching"], "note": "Code-switching as survival under racial capitalism; Obama-era racial politics; sketch as ideological laboratory"},
    {"title": "Tim and Eric", "genre": "sketch troupe", "tags": ["anti-commodity", "surrealism", "media"], "note": "Anti-comedy as refusal of commodity form; the grotesque of commercial television; Awesome Show as Situationist détournement"},
    {"title": "Whitest Kids U Know", "genre": "sketch troupe", "tags": ["transgression", "class", "absurdism"], "note": "Working-class absurdism; transgression and the limits of taste as class marker"},

    # Late Night
    {"title": "The Daily Show (Jon Stewart era)", "genre": "late night", "tags": ["ideology", "liberal critique", "media"], "note": "Liberal ideology as the horizon of acceptable critique; the comedian as trusted news source under media crisis; irony as political impotence"},
    {"title": "The Colbert Report", "genre": "late night", "tags": ["satire", "ideology", "performance"], "note": "Conservative ideology performed to expose its absurdity; the problem of ironic distance; transition to CBS as ideological recuperation"},
    {"title": "Stephen Colbert (Late Show)", "genre": "late night", "tags": ["liberal ideology", "recuperation", "spectacle"], "note": "From satirist to establishment entertainer; the recuperation of critique by capital; late night as Democratic Party apparatus"},
    {"title": "Jimmy Fallon", "genre": "late night", "tags": ["spectacle", "celebrity", "depoliticization"], "note": "The total depoliticization of late night; celebrity worship as ideology; entertainment capital's demand for frictionless content"},
    {"title": "Jimmy Kimmel", "genre": "late night", "tags": ["liberal tears", "spectacle", "authenticity"], "note": "Emotional sincerity as brand strategy; The Man Show to liberal conscience as ideological flexibility of capital"},
    {"title": "Seth Meyers", "genre": "late night", "tags": ["liberal critique", "news comedy", "Democratic Party"], "note": "A Closer Look as liberal prosecutorial comedy; comedy as Democratic messaging; the limits of procedural critique"},
    {"title": "Conan O'Brien", "genre": "late night", "tags": ["absurdism", "labor", "platform"], "note": "The Tonight Show struggle as labor dispute; transition to podcasting and the platform economy; absurdism as escape from political comedy"},
    {"title": "John Oliver", "genre": "late night", "tags": ["liberal reformism", "investigative", "commodity"], "note": "Last Week Tonight as liberal reformism; the investigative comedy segment as commodity; systemic critique that never reaches capitalism itself"},
    {"title": "Craig Ferguson", "genre": "late night", "tags": ["authenticity", "immigrant", "anti-format"], "note": "Refusing the late night commodity format; immigrant perspective on American spectacle; the monologue as conversation"},
    {"title": "David Letterman", "genre": "late night", "tags": ["irony", "anti-celebrity", "form"], "note": "Ironic distance as generational posture; deconstructing the talk show form; late career turn to sincerity under platform capitalism"},
    {"title": "Jay Leno", "genre": "late night", "tags": ["lowest common denominator", "commodity", "labor"], "note": "Comedy as pure commodity form; the Tonight Show as factory of consent; Leno vs Conan as capitalist succession crisis"},
    {"title": "James Corden", "genre": "late night", "tags": ["spectacle", "virality", "platform"], "note": "Carpool Karaoke as viral commodity; late night reimagined for platform capitalism; content over comedy"},
    {"title": "Trevor Noah", "genre": "late night", "tags": ["global south", "liberal ideology", "race"], "note": "South African perspective constrained by American liberal framework; Daily Show as brand continuity; race and global capitalism"},

    # Other comedians
    {"title": "Sacha Baron Cohen", "genre": "satirist", "tags": ["spectacle", "ideology", "exposure"], "note": "Borat and the exposure of American ideological unconscious; Ali G and class performance; Who Is America and fascist tendencies"},
    {"title": "Nathan Fielder", "genre": "satirist", "tags": ["alienation", "entrepreneurship", "cringe"], "note": "Nathan For You as critique of small business ideology; The Rehearsal as alienation pushed to its limit; cringe as capitalist affect"},
    {"title": "Eric Andre", "genre": "satirist", "tags": ["spectacle", "destruction", "anti-commodity"], "note": "The Eric Andre Show as destruction of the talk show commodity form; chaos as refusal of ideological coherence"},
    {"title": "Sarah Silverman", "genre": "stand-up", "tags": ["transgression", "liberal feminism", "platform"], "note": "Transgressive comedy and its liberal recuperation; the platform pivot; comedy's ideological flexibility"},
    {"title": "Norm Macdonald", "genre": "stand-up", "tags": ["anti-comedy", "form", "resistance"], "note": "Anti-comedy as formal resistance to commodity structure; the moth joke as refusal of efficient content delivery"},
    {"title": "Stewart Lee", "genre": "stand-up", "tags": ["form", "anti-commodity", "British class"], "note": "Comedy as dialectical form; refusing mainstream success as refusal of commodification; class and cultural capital in British comedy"},
    {"title": "Frankie Boyle", "genre": "stand-up", "tags": ["class", "imperialism", "Scottish"], "note": "Scottish working-class perspective; anti-imperialist comedy; New World Order as explicit political economy of comedy"},
    {"title": "Joe Rogan (as comedian)", "genre": "stand-up", "tags": ["masculinity", "platform capitalism", "ideology"], "note": "The comedian as platform capitalist; JRE and the marketplace of ideas as commodity exchange; bro culture as petty-bourgeois ideology"},
]


def generate_comedian_md(entry):
    slug = slugify(entry["title"])
    tags_str = ", ".join(entry["tags"])
    related_terms = []
    tag_to_term = {
        "alienation": "alienation",
        "commodity": "commodity",
        "commodity fetishism": "commodity",
        "ideology": "ideology",
        "class": "class-struggle",
        "class consciousness": "class-struggle",
        "spectacle": "reification",
        "imperialism": "imperialism",
        "labor": "labor-power",
        "exploitation": "surplus-value",
    }
    for tag in entry["tags"]:
        if tag in tag_to_term and tag_to_term[tag] not in related_terms:
            related_terms.append(tag_to_term[tag])

    lines = ["---"]
    lines.append(f'title: "{entry["title"]}"')
    lines.append(f'genre: "{entry["genre"]}"')
    lines.append(f"tags: [{tags_str}]")
    lines.append("traditions:")
    lines.append('  classical: "TODO"')
    lines.append('  structuralist: "TODO"')
    if related_terms:
        lines.append(f"related_terms: [{', '.join(related_terms)}]")
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
    for entry in COMEDIANS:
        slug, content = generate_comedian_md(entry)
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            created += 1
    print(f"Created {created} comedian scaffolds from {len(COMEDIANS)} entries")


if __name__ == "__main__":
    main()
