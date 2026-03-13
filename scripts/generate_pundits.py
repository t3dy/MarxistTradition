#!/usr/bin/env python3
"""Generate scaffold markdown files for the pundits & podcasters category."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "pundits"


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"['''\"]", "", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


PUNDITS = [
    # Right-wing / Conservative
    {"title": "Piers Morgan", "platform": "television", "tags": ["spectacle", "reaction", "culture war"], "note": "Professional provocateur as commodity; the culture war as ideological displacement of class conflict; media career as capital accumulation"},
    {"title": "Tucker Carlson", "platform": "television", "tags": ["fascism", "populism", "ideology"], "note": "Right-populism as ruling class strategy; the Fox News pipeline; faux class consciousness redirected toward nationalism and reaction"},
    {"title": "Ben Shapiro", "platform": "YouTube", "tags": ["ideology", "reaction", "debate culture"], "note": "Facts don't care about your feelings as positivist ideology; the debate bro as commodity form; Daily Wire as reactionary media capital"},
    {"title": "Jordan Peterson", "platform": "YouTube", "tags": ["ideology", "individualism", "reaction"], "note": "Jungian self-help as bourgeois ideology; clean your room as responsibilization; lobster hierarchies as naturalization of class"},
    {"title": "Dave Rubin", "platform": "YouTube", "tags": ["grift", "marketplace of ideas", "ideology"], "note": "The marketplace of ideas as commodity exchange; from progressive to reactionary as market optimization; the grifter as rational actor"},
    {"title": "Steven Crowder", "platform": "YouTube", "tags": ["reaction", "spectacle", "culture war"], "note": "Change My Mind as spectacle of false dialogue; conservative comedy as ideological reproduction; the media entrepreneur"},
    {"title": "Matt Walsh", "platform": "YouTube", "tags": ["reaction", "gender", "moral panic"], "note": "What Is a Woman as essentialist ideology; the theocratic right's culture industry; moral panic as class displacement"},
    {"title": "Dennis Prager", "platform": "YouTube", "tags": ["ideology", "education", "reaction"], "note": "PragerU as ideological state apparatus; the university form appropriated for bourgeois propaganda; oil money and educational content"},
    {"title": "Charlie Kirk", "platform": "social media", "tags": ["reaction", "youth", "astroturf"], "note": "Turning Point USA as astroturf bourgeois youth movement; the campus culture war as ideological battleground"},
    {"title": "Candace Owens", "platform": "social media", "tags": ["reaction", "race", "tokenism"], "note": "Black conservatism as ideological function for white supremacist capital; Blexit as manufactured consent"},
    {"title": "Alex Jones", "platform": "radio/web", "tags": ["conspiracy", "spectacle", "commodity"], "note": "Infowars as conspiracy commodity; supplements as surplus extraction from paranoia; the libidinal economy of reaction"},
    {"title": "Joe Rogan", "platform": "podcast", "tags": ["platform capitalism", "masculinity", "marketplace of ideas"], "note": "JRE as the quintessential platform commodity; $250M Spotify deal as labor aristocracy; the marketplace of ideas as ideological cover for reaction"},

    # Liberal / Centrist
    {"title": "Rachel Maddow", "platform": "television", "tags": ["liberal ideology", "Russiagate", "media"], "note": "MSNBC as liberal ideological apparatus; Russiagate as displacement of class analysis; the wonk as trusted authority"},
    {"title": "Anderson Cooper", "platform": "television", "tags": ["class", "objectivity", "Vanderbilt"], "note": "The Vanderbilt heir as objective journalist; objectivity as bourgeois ideology; CNN centrism as class interest"},
    {"title": "Chris Hayes", "platform": "television", "tags": ["liberal left", "media", "recuperation"], "note": "The most left-adjacent figure in corporate media; the structural limits of critique within capital's media apparatus"},
    {"title": "Ezra Klein", "platform": "podcast", "tags": ["wonk", "technocracy", "liberal ideology"], "note": "The technocratic liberal as ideological form; Vox and the explanatory journalism commodity; the podcast as elite discourse"},
    {"title": "Nate Silver", "platform": "web", "tags": ["quantification", "technocracy", "ideology"], "note": "The quantification of politics as ideology; FiveThirtyEight and the commodification of prediction; Silver Bulletin as independent media capital"},
    {"title": "Pod Save America", "platform": "podcast", "tags": ["Democratic Party", "liberal ideology", "commodity"], "note": "Obama staffers as podcast commodity; the revolving door between power and commentary; Crooked Media as liberal media capital"},
    {"title": "Malcolm Gladwell", "platform": "podcast", "tags": ["ideology", "pop social science", "commodity"], "note": "The 10,000 hours rule as meritocratic ideology; Revisionist History as liberal reformism; the airport book as commodity form"},

    # Left / Socialist
    {"title": "Chapo Trap House", "platform": "podcast", "tags": ["left", "irony", "Patreon"], "note": "Dirtbag left as aesthetic and political formation; Patreon and the means of podcast production; irony as left political affect"},
    {"title": "Hasan Piker", "platform": "Twitch", "tags": ["left", "streaming", "platform capitalism"], "note": "Socialist streamer as contradiction; the labor of political content creation; Twitch and the attention economy; house discourse as petty-bourgeois critique"},
    {"title": "Democracy Now!", "platform": "radio/web", "tags": ["left media", "independent", "solidarity"], "note": "Amy Goodman and independent left media; the political economy of listener-supported journalism; covering movements capital ignores"},
    {"title": "The Intercept", "platform": "web", "tags": ["investigative", "left liberal", "media capital"], "note": "Omidyar's billionaire-funded adversarial journalism; the contradiction of capital funding its own critique; Greenwald's rightward drift"},
    {"title": "Citations Needed", "platform": "podcast", "tags": ["media criticism", "left", "ideology"], "note": "Systematic critique of media ideology; the PR-to-news pipeline; how media manufactures consent for capital"},
    {"title": "Current Affairs", "platform": "web/podcast", "tags": ["left", "media", "aesthetics"], "note": "Nathan Robinson and left media aesthetics; the magazine as counter-hegemonic project; the labor disputes contradiction"},
    {"title": "Jacobin", "platform": "web", "tags": ["democratic socialism", "media", "left"], "note": "Bhaskar Sunkara and the socialist magazine as media commodity; the DSA-adjacent left; Catalyst as theoretical companion"},
    {"title": "The Majority Report", "platform": "podcast", "tags": ["left", "media", "labor"], "note": "Sam Seder and the daily left commentary form; the political economy of YouTube left media; training ground for left commentators"},
    {"title": "Novara Media", "platform": "web/podcast", "tags": ["British left", "Corbynism", "media"], "note": "Ash Sarkar's luxury communism; British left media after Corbyn; the political economy of independent left journalism"},
    {"title": "Red Scare", "platform": "podcast", "tags": ["post-left", "contrarian", "aesthetics"], "note": "Post-left aesthetics as political posture; the contrarian as commodity; Anna and Dasha between left and reaction"},

    # Influencers / New Media
    {"title": "Philip DeFranco", "platform": "YouTube", "tags": ["news commentary", "platform", "centrism"], "note": "The YouTube news personality as commodity; platform-native journalism; centrist both-sides-ism as ideological position"},
    {"title": "Tim Pool", "platform": "YouTube", "tags": ["grift", "reaction", "platform"], "note": "From Occupy to far-right pipeline; the grifter as rational market actor; beanie as brand commodity"},
    {"title": "Destiny (Steven Bonnell)", "platform": "Twitch", "tags": ["debate culture", "platform", "liberalism"], "note": "The debate streamer as commodity form; platform liberalism; the marketplace of ideas as content strategy"},
    {"title": "Vaush", "platform": "YouTube", "tags": ["left", "debate culture", "platform"], "note": "The socialist debate bro; platform leftism and its limits; the parasocial relationship as political formation"},
    {"title": "H3H3 (Ethan Klein)", "platform": "YouTube", "tags": ["platform", "content economy", "evolution"], "note": "From reaction videos to political commentary; the platform career as ideological journey; Frenemies and the commodity of interpersonal conflict"},
    {"title": "ContraPoints (Natalie Wynn)", "platform": "YouTube", "tags": ["left", "aesthetics", "philosophy"], "note": "The video essay as counter-hegemonic cultural production; aesthetic excess as political strategy; the trans experience under capitalism"},
    {"title": "Philosophy Tube (Abigail Thorn)", "platform": "YouTube", "tags": ["left", "philosophy", "performance"], "note": "Marxist philosophy as YouTube content; the theatricality of ideas; transition as political and personal liberation"},
    {"title": "BreadTube (as phenomenon)", "platform": "YouTube", "tags": ["left", "platform", "counter-hegemony"], "note": "The BreadTube phenomenon as left counter-hegemonic media; its limits within platform capitalism; the algorithm as ideological gatekeeper"},
    {"title": "Bari Weiss", "platform": "web/podcast", "tags": ["IDW", "reaction", "free speech"], "note": "The Free Press as centrist-coded reaction; cancel culture discourse as class displacement; the intellectual dark web commodity"},
    {"title": "Megyn Kelly", "platform": "podcast", "tags": ["reaction", "media", "gender"], "note": "From Fox to NBC to podcast; the media career as capital accumulation strategy; white feminism and its reactionary function"},

    # International / Global
    {"title": "Russell Brand", "platform": "YouTube", "tags": ["anti-establishment", "conspiracy", "grift"], "note": "From left-coded anti-establishment to conspiracy commodity; the pipeline from critique to reaction; allegations and the celebrity commodity"},
    {"title": "George Galloway", "platform": "web/radio", "tags": ["anti-imperialism", "British left", "populism"], "note": "Workers Party and left populism; anti-imperialist rhetoric; the contradictions of left-populist media"},
    {"title": "Owen Jones", "platform": "YouTube", "tags": ["British left", "Labour", "media"], "note": "From Guardian columnist to independent YouTube; the Corbyn era and its aftermath; the political economy of left commentary"},
    {"title": "Andrew Tate", "platform": "social media", "tags": ["masculinity", "reaction", "hustle culture"], "note": "Toxic masculinity as commodity; hustle culture as petty-bourgeois ideology; the manosphere and capitalist subjectivity; trafficking allegations"},
    {"title": "Logan Paul / Jake Paul", "platform": "YouTube", "tags": ["spectacle", "hustle culture", "exploitation"], "note": "The influencer as pure commodity form; crypto scams and financial exploitation of fans; the spectacle of entrepreneurial masculinity"},
    {"title": "Breaking Points", "platform": "YouTube", "tags": ["populism", "independent media", "both-sides"], "note": "Krystal and Saagar's left-right populist format; the political economy of independent political media; populism as ideological displacement"},
    {"title": "Matt Taibbi", "platform": "web", "tags": ["independent", "Twitter Files", "media"], "note": "From Rolling Stone muckraker to Substack libertarian; the Twitter Files and the free speech commodity; the journalist as brand"},
    {"title": "Glenn Greenwald", "platform": "web", "tags": ["independent", "civil liberties", "drift"], "note": "From Snowden revelations to Rumble; the rightward drift of civil libertarianism; Substack as means of media production"},
    {"title": "Jimmy Dore", "platform": "YouTube", "tags": ["populism", "anti-establishment", "pipeline"], "note": "Force the Vote and left media infighting; the anti-establishment comedian-to-pundit pipeline; left-right crossover audiences"},
    {"title": "The Young Turks", "platform": "YouTube", "tags": ["liberal left", "platform", "media"], "note": "Cenk Uygur and early YouTube political media; the political economy of progressive online media; naming contradiction with Armenian genocide"},
]


def generate_pundit_md(entry):
    slug = slugify(entry["title"])
    tags_str = ", ".join(entry["tags"])
    related_terms = []
    tag_to_term = {
        "ideology": "ideology",
        "spectacle": "reification",
        "class": "class-struggle",
        "imperialism": "imperialism",
        "alienation": "alienation",
        "commodity": "commodity",
        "platform capitalism": "commodity",
    }
    for tag in entry["tags"]:
        if tag in tag_to_term and tag_to_term[tag] not in related_terms:
            related_terms.append(tag_to_term[tag])

    lines = ["---"]
    lines.append(f'title: "{entry["title"]}"')
    lines.append(f'platform: "{entry["platform"]}"')
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
    for entry in PUNDITS:
        slug, content = generate_pundit_md(entry)
        filepath = CONTENT_DIR / f"{slug}.md"
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            created += 1
    print(f"Created {created} pundit scaffolds from {len(PUNDITS)} entries")


if __name__ == "__main__":
    main()
