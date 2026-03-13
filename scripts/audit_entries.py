#!/usr/bin/env python3
"""
Audit marxistdictionaryentries.txt against existing content files.
Produces gap_report.json with new entries needed, consolidated from granular variants.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
TXT_FILE = ROOT / "marxistdictionaryentries.txt"
CONTENT_DIR = ROOT / "content"
OUTPUT = Path(__file__).resolve().parent / "gap_report.json"

# --- Known aliases: txt file name → existing slug ---
THINKER_ALIASES = {
    "Karl Marx": "marx", "Frederick Engels": "engels", "V. I. Lenin": "lenin",
    "Antonio Gramsci": "gramsci", "Rosa Luxemburg": "luxemburg",
    "Karl Kautsky": "kautsky", "Georg Lukács": "lukacs", "Leon Trotsky": "trotsky",
    "Mao Zedong": "mao", "Louis Althusser": "althusser", "Herbert Marcuse": "marcuse",
    "Theodor Adorno": "adorno", "Max Horkheimer": "horkheimer",
    "Walter Benjamin": "benjamin", "Nicos Poulantzas": "poulantzas",
    "Samir Amin": "amin", "David Harvey": "harvey", "Michael Heinrich": "heinrich",
    "Paul Sweezy": "sweezy", "Fredric Jameson": "jameson", "Guy Debord": "debord",
    "C. L. R. James": "clr-james", "Frantz Fanon": "fanon", "Amílcar Cabral": "cabral",
    "Antonio Negri": "negri", "Paul Mattick": "mattick", "E. P. Thompson": "thompson",
    "David Ricardo": "ricardo", "Isaak Rubin": "rubin",
    "Angela Davis": "davis", "Étienne Balibar": "balibar", "Alain Badiou": "badiou",
    "Terry Eagleton": "eagleton", "Silvia Federici": "federici",
    "Ludwig Feuerbach": "feuerbach", "Rudolf Hilferding": "hilferding",
    "Jürgen Habermas": "habermas", "G. W. F. Hegel": "hegel",
    "Karl Korsch": "korsch", "Ernest Mandel": "mandel",
    "José Carlos Mariátegui": "mariategui", "Anton Pannekoek": "pannekoek",
    "John Roemer": "roemer", "Eduard Bernstein": "bernstein",
    "Amadeo Bordiga": "bordiga",
}

TEXT_ALIASES = {
    "Capital Volume I": "capital-vol1", "Capital Volume II": "capital-vol2",
    "Capital Volume III": "capital-vol3",
    "The Eighteenth Brumaire of Louis Bonaparte": "eighteenth-brumaire",
    "The German Ideology": "german-ideology", "Grundrisse": "grundrisse",
    "History and Class Consciousness": "history-class-consciousness",
    "Prison Notebooks": "prison-notebooks", "One-Dimensional Man": "one-dimensional-man",
    "Imperialism, the Highest Stage of Capitalism": "imperialism",
    "State and Revolution": "state-and-revolution",
}

TERM_ALIASES = {
    "historical materialism": "historical-materialism",
    "class struggle": "class-struggle", "mode of production": "mode-of-production",
    "relations of production": "relations-of-production",
    "forces of production": "forces-of-production",
    "base and superstructure": "base-superstructure",
    "alienation": "alienation", "surplus value": "surplus-value",
    "commodity": "commodity", "commodity fetishism": "commodity-fetishism",
    "exchange value": "exchange-value", "use value": "use-value",
    "value": "value-form", "reification": "reification",
    "lumpenproletariat": "lumpenproletariat",
    "labour power": "labor-power", "labor power": "labor-power",
    "surplus labour": "surplus-value",
    "dictatorship of the proletariat": "dictatorship-of-proletariat",
    "imperialism": "imperialism",
    "labour theory of value": "abstract-labor",
    "productive forces": "forces-of-production",
    "social relations of production": "relations-of-production",
    "materialist conception of history": "historical-materialism",
    "means of production": "forces-of-production",
    "absolute surplus labour": "absolute-surplus-value",
    "aristocracy of labour": "labor-aristocracy",
}

# --- Category mapping ---
CATEGORY_MAP = {
    "Core Marxist Concepts": "terms",
    "Political Economy Terms": "terms",
    "State and Political Theory": "terms",
    "Ideological Critiques / Polemical Categories": "terms",
    "Economic and Social Actors": "skip",
    "Political Movements and Organizations": "terms",
    "Nations / Political Contexts": "skip",
    "Events and Political Context": "terms",
    "Marx's Early Philosophical Themes": "skip",
    "Historical Figures (Referenced / Engaged)": "thinkers",
    "Philosophical Figures Referenced": "skip",
    "Political Leaders and Rulers": "skip",
    "Marxist Thinkers and Interpreters": "thinkers",
    "Pre-Marx Influences": "thinkers",
    "Key Revolutionary Events": "terms",
    "Workers' Movements": "terms",
    "Socialist and Communist Parties": "terms",
    "Internal Debates in Marxism": "terms",
    "Political Strategy Concepts": "terms",
    "Forms of Socialist Economy": "terms",
    "Labour Process Analysis Topics": "terms",
    "Global Capitalism Topics": "terms",
    "Imperialism Studies": "terms",
    "Culture and Ideology Studies": "terms",
    "Marxist Sociology Topics": "terms",
    "Ecological Marxism Topics": "terms",
    "Historical Materialist Studies": "terms",
    "Classic Marxist Texts (as dictionary entries)": "texts",
    "Analytical Research Topics": "terms",
}

# --- Consolidation rules for granular term entries ---
CONSOLIDATION_RULES = [
    # Capital dynamics
    (r"^capital (accumulation|centralisation|concentration|circulation|export|mobility|reproduction|turnover)", "capital-dynamics"),
    (r"^(centralisation of capital|concentration of wealth|compound accumulation|expanded reproduction|rate of accumulation|capital accumulation cycle)", "capital-dynamics"),
    # Capitalist development
    (r"^capitalist (agriculture|development|industrialisation|labour discipline|modernity|property relations|rationalisation|social relations|transition debates|urbanisation|world economy|world market)", "capitalist-development"),
    # Monopoly
    (r"^(cartel formation|corporate monopolies|corporate capitalism|monopoly capitalism|monopoly pricing|oligarchic capitalism)", "monopoly-capitalism"),
    # Colonial
    (r"^colonial (capitalism|exploitation|labour systems|plantations|trade regimes|administration|resource extraction|taxation|social hierarchies)", "colonial-capitalism"),
    # Commodity circulation
    (r"^commodity (chains|circulation|exchange systems|markets|production expansion|speculation|trade networks|valuation)", "commodity-circulation"),
    # Class analysis
    (r"^class (alliances|antagonism|composition|compromise|conflict|consciousness|domination|fractions|hegemony|interests|polarisation|reproduction|solidarity|stratification|struggle theory|subjectivity|transition)", "class-analysis"),
    (r"^(social classes formation|social conflict dynamics|balance of class forces|constitution of the working class)", "class-analysis"),
    # Crisis
    (r"^(crisis cycles|crisis of profitability|crisis of realisation|crisis of underconsumption|crisis tendencies|commercial crisis|economic crisis|overproduction crises?|overaccumulation crises?|consumption crises|compound crises|structural crises|general crisis|long depression|economic volatility|accumulation crisis)", "crisis-theory-general"),
    (r"^(credit crises|credit expansion|credit institutions|credit speculation|credit systems|banking crises)", "credit-system"),
    # Labour process
    (r"^labour (aristocracy debates|commodification|discipline regimes|fragmentation|intensity|markets formation|militancy|organisation|process|productivity growth|surplus populations|time measurement|turnover|unrest|value debates)", "labour-process"),
    (r"^(labour-capital relation|living labour|concrete labour|productive labour debates|human labour activity|alienated labour|appropriation of labour|emancipation of labour|human productive powers|regulation of labour|conservation of labour time)", "labour-capital-relation"),
    (r"^(dual labour markets|informal labour markets|temporary labour markets|free labour markets|cheap labour markets|global labour markets|labour markets? formation)", "labour-markets"),
    # Agrarian
    (r"^(land concentration|land dispossession|land reform|land rent|agrarian question|agrarian reform|agrarian capitalism|agrarian class)", "agrarian-question"),
    (r"^(enclosure movements|enclosures and dispossession|expropriation of peasants|expropriation of small|dispossession of peasants|conquest and dispossession|customary rights)", "primitive-accumulation-process"),
    (r"^(peasant communes|peasant economy|peasant insurgencies|peasant rebellions|peasant resistance|peasant subsistence)", "peasant-question"),
    # State
    (r"^(state capitalism|state centralisation|state intervention|state legitimacy|state monopoly|state repression|state socialism|state apparatus|state power|bourgeois state|post-revolutionary state)", "state-theory"),
    # Market
    (r"^market (anarchy|competition|dependence|exchange|expansion|mediation|regulation|society|transition)", "market-dynamics"),
    # Revolution
    (r"^(revolutionary crisis|revolutionary democracy|revolutionary ideology|revolutionary organisation|revolutionary praxis|revolutionary vanguard)", "revolutionary-theory"),
    (r"^(proletarian organisation|proletarian party|proletarian politics|proletarian radicalism|proletarian self-organisation|proletarian solidarity|proletarian subjectivity|proletarian uprising|proletarianisation)", "proletarian-organization"),
    # International
    (r"^(international capitalism|international competition|international division|international labour|international markets|international socialist|international trade)", "international-division-labour"),
    # Trade
    (r"^(trade cycles|trade liberalisation|trade protection|trade union organisation|trade policy|free trade|protective tariffs?|tariffs)", "trade-and-protection"),
    # Imperial
    (r"^(imperial expansion|imperial rivalry|imperial spheres|imperial trade)", "imperial-system"),
    (r"^(imperial rivalry theory|informal empire|colonial administration systems|settler colonialism|resource imperialism|economic imperialism|financial imperialism|military imperialism|neo-colonialism|core-periphery|semi-periphery|unequal exchange)", "imperialism-theory"),
    # Industrial
    (r"^(industrial capitalism|industrial concentration|industrial labour|industrial monopolies|industrial reserve|industrial wage|industrial working|industrialisation process|industry concentration|large-scale industry)", "industrial-capitalism"),
    # Wage
    (r"^(wage differentials|wage fund|wage labour system|wage suppression|wage struggles|wages|minimum wage)", "wage-system"),
    # Women/gender
    (r"^(women and labour|women in industry|women's labour|gender and labour|family wage|patriarchal labour)", "gender-and-labour"),
    # World economy
    (r"^(world economic|world economy|world market formation|world market fluctuations|world revolutionary|capitalist world)", "world-system"),
    # Historical development
    (r"^(historical development|historical materialism debates|historical necessity|historical periodisation|historical progress|historical transformation)", "historical-development"),
    # Global production
    (r"^(global commodity|global division|global labour markets|global production|global proletariat|global supply|global debt|global labour arbitrage)", "global-production-networks"),
    # Socialist planning
    (r"^(planned economy|central planning|workers' self-management|cooperative economies|participatory planning|cybernetic planning|decentralised planning|state planning|collectivised|communal agriculture|socialised industry|public banking|cooperative production|public ownership|associated producers)", "socialist-planning"),
    # Social transformation
    (r"^(socialisation of production|socialised labour|social ownership|social planning|social revolution|social transformation|social wealth)", "social-transformation"),
    (r"^(social reproduction theory|social reproduction debates|family and capitalism|household labour|reproduction of labour)", "social-reproduction-theory"),
    (r"^(social division of labour|division of social labour|technical division|division between manual|division of productive)", "division-of-labour"),
    # Reform vs revolution
    (r"^(reformism debates|reformist socialism|liberal reform|parliamentary reform|bourgeois social reform|philanthropic socialism|bourgeois socialism|sentimental socialism|religious socialism|sectarian socialism)", "reformism-critique"),
    # Profit
    (r"^(profit realisation|profit rate|profitability decline|declining rate of profit|crisis of profitability)", "profit-rate-dynamics"),
    # Finance
    (r"^(finance capital dominance|financial speculation|financialisation|financial globalisation|banking capital)", "financialisation"),
    # Monetary
    (r"^(monetary circulation|monetary crises|monetary policy|currency circulation|gold standard|money|savings banks|bank question)", "monetary-system"),
    # Ideology critique
    (r"^(bourgeois ideology|petty-bourgeois ideology|ideological apparatus|ideological domination|ideological mystification|ideology critique|ideological reproduction|false consciousness|moralising criticism|critical morality|philistine morality)", "ideology-and-consciousness"),
    # Culture studies
    (r"^(cultural industries|mass culture|culture and ideology|literature and class|art and class|popular culture|media ideology|education and ideology|national culture|working-class culture|counter-culture|cultural hegemony)", "culture-and-ideology"),
    # Ecology
    (r"^(capitalist environmental|industrial pollution|resource exhaustion|ecological crises|environmental justice|green socialism|social metabolism|energy transitions|climate crisis|fossil capitalism|metabolic interaction)", "ecological-crisis"),
    # Democracy debates
    (r"^(democratic centralism debates|democratic republicanism|democratic socialism|democratic uprisings|radical democracy|radical republicanism|bourgeois democracy|liberal democracy critique|parliamentary democracy|popular sovereignty|bourgeois constitutionalism|constitutional|bourgeois liberalism|liberal constitutional)", "democracy-and-state"),
    # Dialectics
    (r"^(dialectical contradiction|dialectical development|dialectical negation|dialectics of history|negation of the negation)", "dialectics-method"),
    # Pre-capitalist modes
    (r"^(ancient mode|ancient class|slave societies|tributary systems|feudal agrarian|feudal rent|medieval guild|merchant republics|early modern trade|estate society|non-capitalist social formations|natural economy)", "pre-capitalist-modes"),
    # Labour process control
    (r"^(scientific management|Taylorism|Fordism|post-Fordism|automation and labour|deskilling|labour control|managerial hierarchy|industrial discipline|labour surveillance|production quotas|factory regimes?|workplace resistance|factory discipline|factory legislation|factory system|despotism in production)", "labour-process-control"),
    # Global capitalism
    (r"^(transnational corporations|global supply chains|offshore production|outsourcing|export processing|financial globalisation|global labour arbitrage|global debt crises|international monetary|structural adjustment|trade liberalisation regimes|neoliberal globalisation)", "neoliberal-globalization"),
    # Communist parties
    (r"^(German Social Democratic|Bolshevik Party|Menshevik|Communist Party|Chinese Communist|Italian Communist|French Communist|Spanish Communist|British Communist|Cuban Communist|Vietnamese Communist|Workers' Party traditions|Trotskyist organ|Maoist parties|Eurocommunist|Left Communist groups)", "communist-parties-history"),
    # Workers' internationals
    (r"^(First International|Second International|Third International|Fourth International|Zimmerwald|syndicalist|industrial workers of the world|factory council|workers' soviets|workers' councils|autonomist workers|rank-and-file|wildcat strike|general strike movements|anti-austerity)", "workers-internationals"),
    # Political strategy
    (r"^(mass party|united front|popular front|dual power|insurrectionary|armed struggle|party discipline|democratic centralism theory|mass line|guerrilla warfare|protracted people|national liberation strategy|front organisations|cadre formation|revolutionary propaganda|political agitation|political education)", "political-strategy"),
    # Internal debates
    (r"^(revisionism|orthodox Marxism|Western Marxism|analytical Marxism|structural Marxism|humanist Marxism|Marxist feminism|eco-Marxism|autonomist Marxism|open Marxism|council communism|left communism|Leninism debates|Trotskyism debates|Maoism debates|Eurocommunism debates|market socialism debates|socialism in one country|permanent revolution theory|uneven development theory|combined development)", "marxist-currents"),
    # Bourgeois revolution
    (r"^(bourgeois revolution|bourgeois-democratic|bourgeois nationalism|bourgeois parliamentarism|bourgeois public sphere|bourgeois revolution theory|bourgeois state formation|anti-feudal revolution)", "bourgeois-revolution"),
    # Bureaucracy
    (r"^(bureaucratic centralisation|bureaucratic class|bureaucratic socialism|authoritarian socialism)", "bureaucracy-critique"),
    # Various standalone consolidations
    (r"^(domestic industry|domestic labour|household production|handicraft production|artisan production|artisan guild|guild production|manufacture system|manufacturing capitalism|petty commodity|petty producers)", "petty-production"),
    (r"^(rent|ground rent|rentier class)", "rent-theory"),
    (r"^(property|private property|communal property|communal village)", "property-relations"),
    (r"^(debt peonage|debt relations|contract labour|sharecropping|semi-proletarian)", "unfree-labour"),
    (r"^(urban proletariat|urban social|urbanisation under|rural proletariat|rural social|slum economies)", "urban-rural-proletariat"),
    (r"^(national bourgeoisie|national capitalist|national economic|national market|national liberation struggles|national question)", "national-question"),
    (r"^(human emancipation|human self-realisation|human species|human social relations|political emancipation)", "emancipation"),
    (r"^(innovation under|technological change|technological unemployment|digital capitalism|platform economies?)", "technology-capitalism"),
    (r"^(idealism critique|metaphysics of political economy|historical school of law)", "philosophical-critique"),
    (r"^(racial capitalism|migration and labour|precariat debates|informal economies)", "racial-capitalism"),
    (r"^(surplus appropriation|surplus extraction|surplus product|surplus population|productive surplus)", "surplus-extraction"),
    (r"^(fixed capital|variable capital debates|organic composition of capital debates)", "capital-composition"),
    (r"^(dependency relations|dependency theory)", "dependency-theory"),
    (r"^(socialist transition|post-capitalist transition|transitional society|transitional demands|epochal transition|economic transition)", "transitional-politics"),
    (r"^(economic determinism|economic base theory|economic laws of motion)", "economic-determinism-debate"),
    (r"^(political representation|political revolution|political subject|political struggle|political power|political organisation|class domination)", "political-power"),
    (r"^(economic liberalism critique|economic planning debates|economic restructuring)", "economic-policy-debates"),
    (r"^(opportunism|right opportunism|left opportunism)", "opportunism"),
    (r"^(long waves|long-term capitalist|cycles of accumulation|structural transformation|crisis and restructuring|revolutionary conjunctures)", "long-waves-capitalism"),
    (r"^(flexible accumulation|neo-mercantilism|merchant capitalism|merchant class|mercantile expansion|mercantilism critique)", "merchant-capital-history"),
    (r"^(political economy of welfare|welfare capitalism)", "welfare-state"),
    (r"^(financial crisis analysis|labour market segmentation|technological change and class)", "contemporary-political-economy"),
]

SECTION_TAGS = {
    "Core Marxist Concepts": ["political economy", "theory"],
    "Political Economy Terms": ["political economy"],
    "State and Political Theory": ["state theory", "politics"],
    "Ideological Critiques / Polemical Categories": ["ideology", "critique"],
    "Political Movements and Organizations": ["movements", "organizations"],
    "Events and Political Context": ["history", "revolution"],
    "Key Revolutionary Events": ["history", "revolution"],
    "Workers' Movements": ["labor movement", "organization"],
    "Socialist and Communist Parties": ["parties", "organization"],
    "Internal Debates in Marxism": ["debates", "theory"],
    "Political Strategy Concepts": ["strategy", "organization"],
    "Forms of Socialist Economy": ["socialist economy", "planning"],
    "Labour Process Analysis Topics": ["labor process", "production"],
    "Global Capitalism Topics": ["globalization", "capitalism"],
    "Imperialism Studies": ["imperialism", "colonialism"],
    "Culture and Ideology Studies": ["culture", "ideology"],
    "Marxist Sociology Topics": ["sociology", "reproduction"],
    "Ecological Marxism Topics": ["ecology", "environment"],
    "Historical Materialist Studies": ["history", "modes of production"],
    "Analytical Research Topics": ["analysis", "contemporary"],
    "Consolidated": ["theory", "political economy"],
}


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r"[''']s?\b", "", s)
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_txt(filepath):
    sections = {}
    current_section = None
    section_keywords = [
        "Concepts", "Terms", "Theory", "Critiques", "Actors", "Movements",
        "Organizations", "Figures", "Context", "Themes", "Thinkers",
        "Influences", "Events", "Leaders", "Nations", "Debates", "Strategy",
        "Economy", "Process", "Topics", "Studies", "Texts", "Workers",
        "Parties", "Research", "Rulers"
    ]
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            if line[0].isupper() and any(kw in line for kw in section_keywords):
                current_section = line.strip()
                sections.setdefault(current_section, [])
                continue
            if current_section:
                entry = line.strip()
                if entry:
                    sections[current_section].append(entry)
    return sections


def get_existing_slugs():
    existing = {}
    for category in ["terms", "texts", "thinkers"]:
        cat_dir = CONTENT_DIR / category
        existing[category] = {f.stem for f in cat_dir.glob("*.md")} if cat_dir.exists() else set()
    return existing


def consolidate(entry_name):
    name_lower = entry_name.lower()
    for pattern, umbrella_slug in CONSOLIDATION_RULES:
        if re.search(pattern, name_lower):
            return umbrella_slug, True
    return slugify(entry_name), False


def main():
    sections = parse_txt(TXT_FILE)
    existing = get_existing_slugs()

    all_aliases = {}
    all_aliases.update({slugify(k): v for k, v in THINKER_ALIASES.items()})
    all_aliases.update({slugify(k): v for k, v in TEXT_ALIASES.items()})
    all_aliases.update({slugify(k): v for k, v in TERM_ALIASES.items()})

    report = {
        "existing_matched": [],
        "new_terms": [],
        "new_texts": [],
        "new_thinkers": [],
        "consolidated": {},
        "skipped_sections": [],
    }

    umbrella_entries = defaultdict(list)
    seen_slugs = set()

    for section, entries in sections.items():
        category = CATEGORY_MAP.get(section, "skip")
        if category == "skip":
            report["skipped_sections"].append(section)
            continue

        for entry in entries:
            slug = slugify(entry)

            # Check aliases first
            if entry in THINKER_ALIASES or entry in TEXT_ALIASES or entry in TERM_ALIASES:
                report["existing_matched"].append(entry)
                continue
            if slug in all_aliases:
                report["existing_matched"].append(entry)
                continue

            # Check existing files
            if slug in existing.get(category, set()):
                report["existing_matched"].append(entry)
                continue

            # For terms, try consolidation
            if category == "terms":
                umbrella_slug, was_consolidated = consolidate(entry)
                if was_consolidated:
                    umbrella_entries[umbrella_slug].append(entry)
                    continue
                if slug in seen_slugs or slug in existing["terms"]:
                    continue
                seen_slugs.add(slug)
                report["new_terms"].append({
                    "slug": slug,
                    "name": entry,
                    "section": section,
                    "tags": SECTION_TAGS.get(section, ["theory"])
                })
            elif category == "texts":
                if slug in seen_slugs or slug in existing["texts"]:
                    continue
                seen_slugs.add(slug)
                report["new_texts"].append({
                    "slug": slug,
                    "name": entry,
                    "section": section
                })
            elif category == "thinkers":
                if slug in seen_slugs or slug in existing["thinkers"]:
                    continue
                seen_slugs.add(slug)
                report["new_thinkers"].append({
                    "slug": slug,
                    "name": entry,
                    "section": section
                })

    # Add consolidated umbrella terms
    for umbrella_slug, originals in umbrella_entries.items():
        if umbrella_slug in existing["terms"] or umbrella_slug in seen_slugs:
            report["existing_matched"].append(f"[consolidated] {umbrella_slug}")
            continue
        seen_slugs.add(umbrella_slug)
        display = umbrella_slug.replace("-", " ").title()
        report["new_terms"].append({
            "slug": umbrella_slug,
            "name": display,
            "section": "Consolidated",
            "tags": ["theory", "political economy"],
            "consolidates": originals
        })
        report["consolidated"][umbrella_slug] = originals

    report["stats"] = {
        "existing_matched": len(report["existing_matched"]),
        "new_terms": len(report["new_terms"]),
        "new_texts": len(report["new_texts"]),
        "new_thinkers": len(report["new_thinkers"]),
        "consolidated_groups": len(report["consolidated"]),
        "entries_consolidated": sum(len(v) for v in report["consolidated"].values()),
        "skipped_sections": report["skipped_sections"],
        "total_new": len(report["new_terms"]) + len(report["new_texts"]) + len(report["new_thinkers"]),
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Gap report: {OUTPUT}")
    print(f"\nStats:")
    for k, v in report["stats"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
