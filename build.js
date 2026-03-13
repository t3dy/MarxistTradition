const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');

const CONTENT_DIR = path.join(__dirname, 'content');
const DATA_DIR = path.join(__dirname, 'data');

function buildCategory(category) {
  const dir = path.join(CONTENT_DIR, category);
  if (!fs.existsSync(dir)) {
    console.warn(`  Skipping ${category}: directory not found`);
    return [];
  }

  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
  const entries = [];

  for (const file of files) {
    const raw = fs.readFileSync(path.join(dir, file), 'utf-8');
    const { data, content } = matter(raw);
    const body = marked.parse(content.trim());
    const slug = path.basename(file, '.md');
    entries.push({ slug, ...data, body });
  }

  // Sort: analyses by date descending, others alphabetically by display field
  if (category === 'analyses') {
    entries.sort((a, b) => (b.date || 0) - (a.date || 0));
  } else {
    const sortKey = (category === 'terms') ? 'term'
      : (category === 'texts' || category === 'wonks' || category === 'analyses' || category === 'comedians' || category === 'pundits') ? 'title'
      : 'name';
    entries.sort((a, b) => (a[sortKey] || '').localeCompare(b[sortKey] || ''));
  }

  return entries;
}

function main() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

  const categories = ['thinkers', 'texts', 'terms', 'analyses', 'wonks', 'comedians', 'pundits'];

  for (const cat of categories) {
    const entries = buildCategory(cat);
    const outPath = path.join(DATA_DIR, `${cat}.json`);
    fs.writeFileSync(outPath, JSON.stringify(entries, null, 2));
    console.log(`  ${cat}: ${entries.length} entries -> ${outPath}`);
  }

  console.log('Build complete.');
}

main();
