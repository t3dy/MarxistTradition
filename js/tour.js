(async function () {
  const [thinkers, texts, terms] = await Promise.all([
    fetch('data/thinkers.json').then(r => r.json()),
    fetch('data/texts.json').then(r => r.json()),
    fetch('data/terms.json').then(r => r.json()),
  ]);

  const container = document.getElementById('tour-content');

  function linkThinker(slug) {
    return `<a class="cross-link" href="dictionary.html#thinker-${slug}">${slug}</a>`;
  }

  function linkText(slug) {
    return `<a class="cross-link" href="dictionary.html#text-${slug}">${slug}</a>`;
  }

  function linkTerm(slug) {
    return `<a class="cross-link" href="dictionary.html#term-${slug}">${slug}</a>`;
  }

  const sections = [
    {
      title: 'Classical Marxism',
      period: '1840s\u20131920s',
      body: `<p>The tradition begins with Karl Marx and Friedrich Engels, who together developed a materialist critique of capitalism grounded in the analysis of commodity production, class struggle, and historical change. Marx's <em>Capital</em> (1867) remains the foundational text: a systematic investigation of how value is created through labor, extracted as surplus, and accumulated in the capitalist mode of production.</p>
      <p>This period also includes Rosa Luxemburg's analysis of imperialism and expanded reproduction, and Vladimir Lenin's theorization of the state and monopoly capitalism. These thinkers shared a commitment to understanding capitalism as a historically specific and internally contradictory system.</p>`,
      thinkers: ['marx', 'engels', 'luxemburg', 'lenin'],
      texts: ['capital-vol1', 'communist-manifesto', 'accumulation-of-capital'],
      terms: ['commodity', 'surplus-value', 'primitive-accumulation', 'historical-materialism'],
    },
    {
      title: 'Western Marxism',
      period: '1920s\u20131960s',
      body: `<p>In the aftermath of failed revolutions in Western Europe, a new generation of Marxist intellectuals turned from political economy toward philosophy, culture, and ideology. Antonio Gramsci, writing from a Fascist prison, developed the concept of hegemony to explain how ruling classes maintain power not just through coercion but through cultural and intellectual leadership.</p>
      <p>Western Marxism broadened the tradition's scope well beyond the factory floor, opening questions about consciousness, ideology, and the relationship between base and superstructure that remain central to contemporary debates.</p>`,
      thinkers: ['gramsci'],
      texts: ['prison-notebooks'],
      terms: ['alienation', 'base-superstructure', 'dialectics'],
    },
    {
      title: 'Structuralist Marxism',
      period: '1960s\u20131980s',
      body: `<p>Louis Althusser and his collaborators (Balibar, Ranciere, Macherey, Establet) proposed a radically anti-humanist reading of Marx. In <em>Reading Capital</em> (1965), they argued that Marx himself had not fully understood his own theoretical breakthrough &mdash; the move from ideology to science &mdash; and that a "symptomatic reading" was required to extract the latent scientific structure from Marx's texts.</p>
      <p>Structuralist Marxism rejected the Hegelian dialectic, the humanist subject, and simple base-superstructure causality in favor of structural causality, overdetermination, and the relative autonomy of different levels of the social formation. This approach remains influential in its insistence that social structures cannot be reduced to the intentions of individual actors.</p>`,
      thinkers: ['althusser'],
      texts: ['reading-capital'],
      terms: ['mode-of-production', 'relations-of-production', 'forces-of-production'],
    },
    {
      title: 'Value-Form Theory',
      period: '1970s\u2013present',
      body: `<p>Drawing on the work of Isaak Rubin (whose <em>Essays on Marx's Theory of Value</em> was rediscovered in the 1970s), value-form theorists argue that value is not a substance embedded in commodities by labor, but a social form constituted through the process of exchange. Abstract labor, on this reading, is not mere expenditure of human energy but a historically specific social abstraction produced by commodity exchange.</p>
      <p>Michael Heinrich's "new reading of Marx" (<em>neue Marx-Lekture</em>) and Soren Mau's analysis of capital as a form of structural domination represent the cutting edge of this tradition. These theorists emphasize that Marx's categories are forms of social mediation, not transhistorical descriptions of economic life.</p>`,
      thinkers: ['rubin', 'heinrich'],
      texts: ['essays-value', 'introduction-three-volumes', 'mute-compulsion'],
      terms: ['value-form', 'abstract-labor', 'commodity-fetishism', 'exchange-value'],
    },
    {
      title: 'Contemporary Readings',
      period: '1980s\u2013present',
      body: `<p>David Harvey's widely-read <em>Companion to Marx's Capital</em> offers a close, chapter-by-chapter reading of <em>Capital</em> that emphasizes the empirical and political dimensions of Marx's analysis. Harvey's approach is historicist: he reads Marx's categories as tools for understanding the concrete dynamics of class struggle and capital accumulation in specific times and places.</p>
      <p>John Roemer and the analytical Marxists, meanwhile, attempted to reconstruct Marxian economics using the formal tools of game theory and rational choice. While controversial within the tradition, analytical Marxism sharpened debates about exploitation, class, and distributive justice.</p>
      <p>These contemporary approaches demonstrate that Marx's work continues to generate productive disagreement. The tension between value-form readings (which emphasize the formal structures of commodity society) and historicist readings (which emphasize class struggle and empirical political economy) remains one of the most generative fault lines in Marxist scholarship today.</p>`,
      thinkers: ['harvey', 'roemer'],
      texts: ['companion-to-capital'],
      terms: ['use-value', 'commodity'],
    },
  ];

  let html = '';
  for (const s of sections) {
    const thinkerLinks = (s.thinkers || []).map(slug => {
      const t = thinkers.find(x => x.slug === slug);
      return t ? `<a class="cross-link" href="whos-who.html">${t.name}</a>` : '';
    }).filter(Boolean).join(' ');

    const textLinks = (s.texts || []).map(slug => {
      const t = texts.find(x => x.slug === slug);
      return t ? `<a class="cross-link" href="dictionary.html">${t.title}</a>` : '';
    }).filter(Boolean).join(' ');

    const termLinks = (s.terms || []).map(slug => {
      const t = terms.find(x => x.slug === slug);
      return t ? `<a class="cross-link" href="dictionary.html">${t.term}</a>` : '';
    }).filter(Boolean).join(' ');

    html += `
      <div class="tour-section">
        <h2>${s.title}</h2>
        <div class="period">${s.period}</div>
        ${s.body}
        <div class="cross-links" style="margin-top:1rem;">
          ${thinkerLinks ? `<div style="margin-bottom:0.5rem;"><strong style="font-size:0.82rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-muted);">Thinkers:</strong> ${thinkerLinks}</div>` : ''}
          ${textLinks ? `<div style="margin-bottom:0.5rem;"><strong style="font-size:0.82rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-muted);">Texts:</strong> ${textLinks}</div>` : ''}
          ${termLinks ? `<div><strong style="font-size:0.82rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--color-text-muted);">Key concepts:</strong> ${termLinks}</div>` : ''}
        </div>
      </div>
    `;
  }

  container.innerHTML = html;
})();
