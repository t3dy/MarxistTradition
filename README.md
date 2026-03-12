# The Marxist Tradition

A companion website to [Capital RAG](https://github.com/EricRuud/capital_interpreter) providing a curated tour of the Marxist intellectual tradition.

**Live site: [https://t3dy.github.io/MarxistTradition/](https://t3dy.github.io/MarxistTradition/)**

## Pages

| Page | Description |
|------|-------------|
| **Tour** | Guided walk through the Marxist tradition from classical foundations to contemporary debates |
| **Dictionary** | Terms of art with German originals, definitions, and multi-tradition interpretive differences |
| **Who's Who** | Biographical profiles of major thinkers arranged as a timeline |
| **21st Century** | Marxist analysis of 22 contemporary issues through four theoretical traditions |

## Content Architecture

All content lives as Markdown files with YAML frontmatter in `content/`:

```
content/
  thinkers/    10 entries (Marx, Engels, Luxemburg, Lenin, Gramsci, Althusser, Harvey, Heinrich, Rubin, Roemer)
  texts/       10 entries (Capital, Grundrisse, Communist Manifesto, Prison Notebooks, etc.)
  terms/       15 entries (commodity, surplus-value, alienation, dialectics, etc.)
  analyses/    22 entries (Iran war, housing crisis, AI & labor, Thiel & tech oligarchy, etc.)
```

A Node.js build step (`npm run build`) compiles the Markdown into JSON in `data/`, which the static HTML/JS pages consume at runtime.

### Adding Content

Create a new `.md` file in the appropriate `content/` subdirectory following the existing YAML schema, then run `npm run build`.

**Thinker schema:**
```yaml
name, born, died, nationality, tradition, key_works[], tags[]
```

**Text schema:**
```yaml
title, author, year, tradition, translations[], tags[]
```

**Term schema:**
```yaml
term, german, source, related[], tags[], traditions{} (optional)
```

**Analysis schema:**
```yaml
title, date, region, tags[], traditions{classical, value-form, harvey, structuralist}, related_terms[], related_thinkers[]
```

## Multi-Tradition Perspectives

The analyses page presents each contemporary issue through four Marxist theoretical lenses:

- **Classical Marxism** (Marx, Engels, Lenin, Luxemburg) - class struggle, imperialism, surplus extraction
- **Value-Form Theory** (Heinrich, Rubin) - social forms of value, abstract labor, commodity fetishism
- **Harvey / Geographical Materialism** - spatial fixes, accumulation by dispossession, uneven development
- **Structuralist Marxism** (Althusser) - ideological state apparatuses, overdetermination, structural causality

## Development

```bash
npm install
npm run build    # compiles content/ -> data/
npx serve .      # local preview at http://localhost:3000
```

## Tech Stack

- Static HTML/CSS/JS (no framework)
- Tailwind CSS (CDN)
- gray-matter + marked (build-time Markdown processing)
- GitHub Pages (hosting)
