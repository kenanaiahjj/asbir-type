import '@fontsource-variable/inter';
import '@fontsource-variable/geist';
import '@fontsource/instrument-serif/400.css';
import '@fontsource-variable/fraunces';
import '@fontsource-variable/geist-mono';
import '@fontsource/ibm-plex-mono/400.css';
import '@fontsource/ibm-plex-mono/700.css';
import './styles.css';
import { glyphCodepoints } from './glyphs.js';

const app = document.querySelector('#app');

const families = {
  sans: {
    name: 'Asbir Sans', tag: 'Sans', label: 'High x-height geometric grotesk', xHeight: 77,
    title: 'Raise the lowercase.\nKeep the voice precise.',
    description: 'Asbir Sans is a bold, editorial neo-grotesk built for Asbir Tech products and the identity around them. Its high x-height, open apertures, and measured spacing keep dense interface text clear while giving headlines and brand moments a distinct voice.',
    attributes: ['x-height 77%', 'wght 100–900', 'open apertures'],
    comparisons: [
      ['asbir-sans', 'Asbir Sans', 'Authored derivative source', 'High lowercase / geometric character system.'],
      ['inter', 'Inter', 'Reference', 'Tall x-height / UI-first clarity.'],
      ['geist', 'Geist', 'Reference', 'Crisp geometry / calmer lowercase.'],
    ],
  },
  serif: {
    name: 'Asbir Serif', tag: 'Serif', label: 'High-x display serif companion', xHeight: 76,
    title: 'Editorial contrast.\nThe same compact rhythm.',
    description: 'A serif companion built for commanding display copy: condensed enough for tension, but with the high lowercase, open counters, and measured spacing that make it unmistakably Asbir.',
    attributes: ['x-height 76%', 'display contrast', 'firm bracketed serifs'],
    comparisons: [
      ['asbir-serif', 'Asbir Serif', 'Editable review source', 'High lowercase / controlled old-style contrast.'],
      ['instrument', 'Instrument Serif', 'Reference', 'Condensed editorial old-style reference.'],
      ['fraunces', 'Fraunces', 'Reference', 'Open-source serif with expressive optical character.'],
    ],
  },
  mono: {
    name: 'Asbir Mono', tag: 'Mono', label: 'UI and code companion', xHeight: 75,
    title: 'Make the code exact.\nKeep it recognizably Asbir.',
    description: 'A coding and data companion with a generous lowercase, stable 600-unit rhythm, and precise differentiation where source code needs it most.',
    attributes: ['x-height 75%', 'wght 100–900', 'slashed zero / 600-unit grid'],
    comparisons: [
      ['asbir-mono', 'Asbir Mono', 'Approved production family', 'Two-storey a / slashed zero / fixed 600-unit grid.'],
      ['plex-mono', 'IBM Plex Mono', 'Reference', 'Reliable humanist coding forms.'],
      ['geist-mono', 'Geist Mono', 'Reference', 'Contemporary developer mono foundation.'],
    ],
  },
};

const sets = {
  Sentence: 'The quick brown fox jumps over the lazy dog.',
  Pangram: 'Sphinx of black quartz, judge my vow.',
  Interface: 'Make every detail feel intentional.',
  Code: 'const form = await submit({ id: "asbir-01" });',
  Numbers: '0123456789  —  48.50 / 100%',
  French: "À l'été, le garçon déjà là.",
  Polish: 'Zażółć gęślą jaźń.',
  Czech: 'Příliš žluťoučký kůň úpěl ďábelské ódy.',
  Turkish: 'İstanbul, ıslak yağmur, Şeker.',
  Romanian: 'Știință și țară.',
  Hungarian: 'Árvíztűrő tükörfúrógép.',
  Icelandic: 'Þórður á Ðórshöfn.',
  Vietnamese: 'Tiếng Việt: Trăm năm trong cõi người ta.',
  Greek: 'Καλημέρα κόσμε. Τα γράμματα έχουν ρυθμό.',
  Cyrillic: 'Съешь же ещё этих мягких французских булок, да выпей чаю.',
};

const weightStyles = [
  [100, 'Thin'], [200, 'ExtraLight'], [300, 'Light'], [400, 'Regular'], [500, 'Medium'],
  [600, 'SemiBold'], [700, 'Bold'], [800, 'ExtraBold'], [900, 'Black'],
];

const glyphGroups = {
  latin: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
  figures: '0123456789₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹¼½¾⅓⅔⅛⅜⅝⅞',
  punctuation: `.,:;!?¿¡…-–—_()[]{}<>/\\|@#$%&*+−=×÷~^\"'‘’“”«»©®™°·←→↑↓↔⇐⇒⇔≤≥≠±`,
  accents: 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØŒÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøœùúûüýþÿĀĂĄĆČĎĐĒĘĚĞĮİŁŃŇŐŔŘŚŠŞȚŤŪŮŸŹŻŽăąćčďđēěğįıłńňőřšťşțťūůźżž',
  greek: 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωΆΈΉΊΌΎΏάέήίόύώ',
  cyrillic: 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяЂЃЄЅІЇЈЉЊЋЌЎЏђѓєѕіїјљњћќўџ',
};

const featureCards = [
  ['zero', 'Slashed zero', '0 O 0 0 0123456789'],
  ['tnum', 'Tabular figures', '12 48 96 100 2024'],
  ['pnum', 'Proportional figures', '12 48 96 100 2024'],
  ['dlig', 'Discretionary ligatures', 'fi ffi ffl fj'],
  ['frac', 'Fractions', '1/2 3/4 5/8'],
  ['sups', 'Superscript', 'H2O x2 n2'],
  ['subs', 'Subscript', 'H2O x2 n2'],
  ['ss01', 'Alternate forms', 'A G a g 1 4'],
];

const monoFeatureCards = [
  ['ss09', 'Plain-zero fallback', '0 O 0 0 0123456789'],
  ['ss01', 'Single-storey a alternate', 'a á ă â ä ã å'],
  ['ss03', 'Alternate l', 'I l 1  |  Il1'],
  ['liga', 'Default coding ligatures', '->  =>  !=  ==  ===  <=  >='],
  ['ss11', 'Extended coding ligatures', '<=>  -->  ::  |>  ...'],
  ['ss07', 'Arrow alternatives', '←  →  ↑  ↓  ↔'],
  ['frac', 'Fractions', '1/2 3/4 5/8'],
  ['sups', 'Superscript', 'H2O x2 n2'],
  ['subs', 'Subscript', 'H2O x2 n2'],
];

const featureCardsFor = family => family === families.mono ? monoFeatureCards : featureCards;

const state = { family: 'sans', text: sets.Sentence, size: 64, weight: 400, tracking: 0, figures: 'tnum', guides: true, mode: 'Sentence', glyphSet: 'latin' };
let monoCountdownTimer = null;
const active = () => families[state.family];

function render() {
  if (monoCountdownTimer) {
    clearInterval(monoCountdownTimer);
    monoCountdownTimer = null;
  }
  const family = active();
  const trackingLabel = state.tracking > 0 ? `+${state.tracking}` : state.tracking;
  const isMono = state.family === 'mono';
  const isSans = state.family === 'sans';
  const hasItalic = isSans || isMono;
  const heroDownload = isSans
    ? '<a class="hero-download" href="/downloads/AsbirSans-1.1.0.zip" download>Download Asbir Sans 1.1.0 ZIP <b>↓</b></a>'
    : '<a class="hero-download" href="/downloads/AsbirMono-1.1.0.zip" download>Download Asbir Mono 1.1.0 ZIP <b>↓</b></a>';
  app.className = `app-${state.family}`;
  app.innerHTML = `
    <header class="site-header">
      <a class="wordmark" href="#top" aria-label="Asbir Tech type studio"><img class="brand-logo" src="https://asbir.tech/assets/asbirtechlogo-BptLBLy6.png" alt="Asbir Tech"><span class="brand-context">/ Type</span></a>
      <div class="header-family">
        <strong>${family.name}</strong>
        <span>Typeface specimen / ${isSans || isMono ? '1.1.0' : 'review'}</span>
      </div>
      <div class="header-actions"><button class="text-button" id="guide-toggle" aria-pressed="${state.guides}">${state.guides ? 'Hide guides' : 'Show guides'} <span class="button-key">G</span></button></div>
    </header>
    <main id="top">
      <nav class="family-nav" aria-label="Typeface family"><div class="nav-label"><span>Family</span><b>03</b></div><div class="family-switcher">${Object.entries(families).map(([key, value]) => { const isComingSoon = key === 'serif'; return `<button class="family-button ${key === state.family ? 'is-active' : ''} ${isComingSoon ? 'is-disabled' : ''}" data-family="${key}" aria-pressed="${key === state.family}" ${isComingSoon ? 'disabled aria-disabled="true"' : ''}><span>${value.tag}</span><small>${key === state.family ? 'Selected' : isComingSoon ? 'Coming soon' : 'Available'}</small></button>`; }).join('')}</div><div class="nav-meta">Variable family<br><span>100—900</span></div></nav>
      <section class="intro intro-${state.family} intro-hero">
        <div class="intro-meta"><span class="intro-family-label">${family.name}</span><span class="intro-style-count">${weightStyles.length} styles</span><span class="intro-variable">Variable</span></div>
        <div class="intro-grid"><div><h1>${family.name}</h1></div><div class="intro-side"><p>${family.description}</p><div class="attribute-list">${family.attributes.map(item => `<span>${item}</span>`).join("")}</div><div class="hero-hero-actions">${heroDownload}</div></div></div></div>
        <div class="intro-hero-foot"><span class="hero-credit">Designed By Asbir Tech Product Design Department</span><a class="hero-license" href="https://scripts.sil.org/OFL" target="_blank" rel="noreferrer">SIL Open Font License 1.1 <b>↗</b></a></div>
      </section>
      <section class="hero-specimen ${state.family}" aria-label="Primary ${family.name} specimen"><div class="hero-specimen-head"><div><span class="eyebrow">Primary specimen</span><strong>${family.name}</strong></div><span class="hero-range">${state.weight} / ${state.size}px / ${trackingLabel} <i></i> Edit directly</span></div><div class="hero-copy" contenteditable="true" role="textbox" aria-label="Editable primary ${family.name} proof" spellcheck="false" style="--hero-size:${Math.max(state.size * 1.55, 88)}px; --hero-weight:${state.weight}; --hero-tracking:${state.tracking / 1000}em">${state.text}</div><div class="hero-specimen-foot"><span>Type anything here to test the family in context.</span><span>↘ Drag the controls below</span></div></section>
      <section class="proof-controls" aria-label="Proof controls">
        <div class="control-intro"><span class="eyebrow">Specimen controls</span><strong>Set the proof</strong><p>Change one family-level variable at a time.</p></div>
        <div class="control-body"><div class="set-picker" role="group" aria-label="Specimen sets">${Object.keys(sets).map(name => `<button class="set-button ${state.mode === name ? 'is-active' : ''}" data-set="${name}" aria-pressed="${state.mode === name}">${name}</button>`).join('')}</div><div class="control-grid"><div class="control-stack"><label for="size">Size <output>${state.size} px</output></label><input id="size" aria-label="Specimen size" type="range" min="32" max="112" value="${state.size}" /></div><div class="control-stack weight-control"><label for="weight">Weight <output>${state.weight}</output></label><input id="weight" aria-label="Specimen weight" type="range" min="100" max="900" step="10" value="${state.weight}" /><div class="weight-stops"><span>100</span><span>400</span><span>700</span><span>900</span></div></div><div class="control-stack tracking-control"><label for="tracking">Letter spacing <output>${trackingLabel}</output></label><input id="tracking" aria-label="Letter spacing" type="range" min="-100" max="100" step="5" value="${state.tracking}" /><div class="tracking-stops"><span>−100</span><span>0</span><span>+100</span></div></div><div class="control-stack figure-control"><label for="figures">Figures</label><select id="figures"><option value="tnum" ${state.figures === 'tnum' ? 'selected' : ''}>${isMono ? 'Fixed-width lining' : 'Tabular lining'}</option>${isMono ? '' : `<option value="pnum" ${state.figures === 'pnum' ? 'selected' : ''}>Proportional lining</option><option value="onum" ${state.figures === 'onum' ? 'selected' : ''}>Proportional oldstyle</option>`}</select></div></div></div>
      </section>
      <section class="comparison" aria-label="${family.name} comparison">${family.comparisons.map(([css, name, type, detail]) => proof(css, name, type, detail)).join('')}</section>
      <section class="notes"><div><span class="note-number">01</span><p><b>Family connection</b><br>Asbir Sans, Serif, and Mono share a high lowercase footprint, measured spacing, and a quiet, firm baseline.</p></div><div><span class="note-number">02</span><p><b>${family.name} focus</b><br>${family === families.serif ? 'Contrast and serif tension without losing the practical Asbir rhythm.' : family === families.mono ? 'Character differentiation, stable texture, and compact code density.' : 'Open counters, clear ambiguity control, and calm UI texture.'}</p></div><div class="proof-status"><span class="status-dot"></span><p><b>Proof mode is live</b><br>Click into any specimen and type your own text.</p></div></section>
      ${renderFamilyContent(family)}
    </main>
    <div class="toast" role="status" aria-live="polite"></div>`;
  bind();
  if (isMono) {
    bindMonoCountdown();
    bindMonoExamples();
  }
}

function proof(css, name, type, detail) {
  const isAsbir = css.startsWith('asbir');
  const fontSize = isAsbir ? Math.round(state.size * (active().xHeight / 74)) : state.size;
  return `<article class="type-proof ${css} ${state.guides ? 'has-guides' : ''}"><header class="proof-head"><div><h2>${name}</h2><span>${type}</span></div><span class="font-metrics">${isAsbir ? `x/h ${active().xHeight}/100` : 'reference'} · ${state.weight}</span></header><div class="guide-label cap">CAP</div><div class="guide-label xheight">x-height</div><div class="guide-label baseline">baseline</div><div class="proof-copy" contenteditable="true" role="textbox" aria-label="Editable ${name} proof" spellcheck="false" style="--proof-size:${fontSize}px; --proof-weight:${state.weight}; --proof-tracking:${state.tracking / 1000}em; --proof-features:${state.figures === 'tnum' ? 'normal' : `'${state.figures}' 1`}">${state.text}</div><p class="proof-detail">${detail}</p></article>`;
}

function renderFamilyContent(family) {
  const familyClass = state.family;
  const isMono = familyClass === 'mono';
  const mappedTotal = (glyphCodepoints[state.family]?.length || 0).toLocaleString();
  const glyphDescription = state.family === 'sans'
    ? `2,987 glyph repertoire / ${mappedTotal} mapped characters across Latin, Greek, Cyrillic, Vietnamese, figures, symbols, and OpenType construction parts.`
    : isMono
      ? `1,170-glyph core repertoire / ${mappedTotal} mapped characters across Latin, Cyrillic, Vietnamese, coding punctuation, Unicode technical arrows, currency, and OpenType construction parts. The separate Nerd Font terminal build adds Powerline and icon symbols.`
      : `${mappedTotal} mapped characters across the current review repertoire.`;
  const prefix = { sans: 'AsbirSans', serif: 'AsbirSerif', mono: 'AsbirMono' }[state.family];
  const glyphs = getGlyphs(state.glyphSet);
  const layoutShowcase = isMono
    ? `<div class="layout-showcase mono-layout-showcase"><article class="layout-display-block mono-layout-code-block"><div class="layout-meta"><span>Code / 01</span><b>TypeScript / 12px</b></div><div class="mono-layout-code-window"><div class="mono-editor-bar"><span class="mono-dots"><i></i><i></i><i></i></span><span>reconcile.ts</span><span>UTF-8</span></div><pre class="mono-layout-code" aria-label="Dense TypeScript specimen"><span class="mono-line">01</span> <span class="mono-keyword">type</span> <span class="mono-name">Session</span> <span class="mono-punc">=</span> {<br><span class="mono-line">02</span>   <span class="mono-key">id</span><span class="mono-punc">:</span> <span class="mono-name">string</span><span class="mono-punc">;</span><br><span class="mono-line">03</span>   <span class="mono-key">status</span><span class="mono-punc">:</span> <span class="mono-string">&quot;active&quot;</span> <span class="mono-punc">|</span> <span class="mono-string">&quot;queued&quot;</span> <span class="mono-punc">|</span> <span class="mono-string">&quot;archived&quot;</span><span class="mono-punc">;</span><br><span class="mono-line">04</span>   <span class="mono-key">latency</span><span class="mono-punc">:</span> <span class="mono-name">number</span><span class="mono-punc">;</span><br><span class="mono-line">05</span> }<span class="mono-punc">;</span><br><span class="mono-line">06</span><br><span class="mono-line">07</span> <span class="mono-keyword">const</span> <span class="mono-function">reconcile</span> <span class="mono-punc">=</span> <span class="mono-punc">(</span><span class="mono-key">rows</span><span class="mono-punc">:</span> <span class="mono-name">Session</span><span class="mono-punc">[])</span> <span class="mono-punc">=&gt;</span> <span class="mono-key">rows</span><br><span class="mono-line">08</span>   <span class="mono-punc">.</span><span class="mono-function">filter</span><span class="mono-punc">(</span><span class="mono-punc">({</span><span class="mono-key">status</span><span class="mono-punc">})</span> <span class="mono-punc">=&gt;</span> <span class="mono-key">status</span> <span class="mono-punc">!==</span> <span class="mono-string">&quot;archived&quot;</span><span class="mono-punc">)</span><br><span class="mono-line">09</span>   <span class="mono-punc">.</span><span class="mono-function">sort</span><span class="mono-punc">((</span><span class="mono-key">a</span><span class="mono-punc">,</span> <span class="mono-key">b</span><span class="mono-punc">)</span> <span class="mono-punc">=&gt;</span> <span class="mono-key">b</span><span class="mono-punc">.</span><span class="mono-key">latency</span> <span class="mono-punc">-</span> <span class="mono-key">a</span><span class="mono-punc">.</span><span class="mono-key">latency</span><span class="mono-punc">)</span><br><span class="mono-line">10</span>   <span class="mono-punc">.</span><span class="mono-function">map</span><span class="mono-punc">(({</span><span class="mono-key">id</span><span class="mono-punc">,</span> <span class="mono-key">latency</span><span class="mono-punc">})</span> <span class="mono-punc">=&gt;</span> <span class="mono-punc">({</span><br><span class="mono-line">11</span>     <span class="mono-key">id</span><span class="mono-punc">,</span><br><span class="mono-line">12</span>     <span class="mono-key">label</span><span class="mono-punc">:</span> <span class="mono-string">&#96;$</span><span class="mono-key">{latency.toFixed(2)}</span><span class="mono-string"> ms&#96;</span><span class="mono-punc">,</span><br><span class="mono-line">13</span>   <span class="mono-punc">}));</span></pre></div></article><article class="layout-reading-block"><div class="layout-meta"><span>Data / 02</span><b>Tabular figures</b></div><p class="layout-lead mono-data-sample">uptime   99.982%<br>latency   48.50 ms<br>build     #0184 / passing</p></article><article class="layout-column-block"><div class="layout-meta"><span>Ambiguity / 03</span><b>Clear by default</b></div><div class="layout-columns mono-ambiguity"><p>O 0 &nbsp; I l 1<br>{ } &nbsp; [ ] &nbsp; ( )<br>!= &nbsp; == &nbsp; =&nbsp; &lt;=</p><p>Asbir Mono defaults to a slashed zero and two-storey a, keeping its coding voice distinct from Asbir Sans.</p><p>Every encoded visible character occupies a fixed 600-unit cell, keeping code and columns aligned at every weight.</p></div></article></div>`
    : `<div class="layout-showcase"><article class="layout-display-block"><div class="layout-meta"><span>Display / 01</span><b>Asbir Sans</b></div><div class="layout-display">Connect with nature</div></article><article class="layout-reading-block"><div class="layout-meta"><span>Reading / 02</span><b>Regular 400</b></div><p class="layout-lead">Shall I compare thee to a summer's day? Thou art more lovely and more temperate: Rough winds do shake the darling buds of May, And summer's lease hath all too short a date</p></article><article class="layout-column-block"><div class="layout-meta"><span>Long form / 03</span><b>Three columns</b></div><div class="layout-columns"><p>The sun had set, leaving the sky painted in shades of orange and pink as the stars twinkled above. The air was filled with the sound of crickets and the rustle of leaves in the gentle breeze. It was a warm summer night, perfect for a walk in the countryside.</p><p>A young man named John ambled down the road, taking in the beauty of the night. He had always been fascinated by the stars and would often spend hours gazing at the sky, lost in thought. He was a simple man, content with his life, but always searching for something more.</p><p>As he walked, he came across a small cottage nestled among the trees. It was a charming place, with a thatched roof and a garden filled with flowers. A light burned in the window, casting a warm glow onto the yard. John drew closer to the cottage, feeling as if he had found something special.</p></div></article></div>`;
  const languageSection = `<section class="family-section language-section" aria-labelledby="language-heading">
      <div class="section-heading"><div><span class="section-index">04 / Language coverage</span><h2 id="language-heading">Designed to travel.</h2></div><p>From everyday interface copy to multilingual product surfaces, the family keeps its rhythm across scripts.</p></div>
      <div class="language-grid ${familyClass}">${[['Latin', sets.Sentence], ['Vietnamese', sets.Vietnamese], ['Greek', sets.Greek], ['Cyrillic', sets.Cyrillic]].map(([language, sample]) => `<article class="language-card"><span>${language}</span><div>${sample}</div></article>`).join('')}</div>
    </section>`;
  const monoDataSection = `<section class="family-section mono-data-section" aria-labelledby="mono-data-heading">
      <div class="section-heading"><div><span class="section-index">04 / Data surfaces</span><h2 id="mono-data-heading">High density. Zero drift.</h2></div><p>Asbir Mono is for the information that has to line up: IDs, routes, statuses, measurements, and the long tail of values a product needs to show at once. The decisive check is at 12–16px with real tables, logs, JSON/TypeScript, and dense terminal output—not the large specimen alone.</p></div>
      <div class="mono-data-grid">
        <article class="mono-data-panel mono-data-wide">
          <div class="mono-example-head"><span>Operations / 01</span><b>48 rows / sorted by latency</b></div>
          <div class="mono-table-wrap"><table class="mono-data-table"><thead><tr><th>ID</th><th>ROUTE</th><th>STATUS</th><th>LATENCY</th><th>REQUESTS</th></tr></thead><tbody><tr><td>as-0184</td><td>/api/session</td><td><span class="mono-status is-good">200 OK</span></td><td>48.50 ms</td><td>1,284,904</td></tr><tr><td>as-0185</td><td>/api/profile</td><td><span class="mono-status is-good">200 OK</span></td><td>52.14 ms</td><td>982,410</td></tr><tr><td>as-0186</td><td>/api/checkout</td><td><span class="mono-status is-warn">202 QUEUED</span></td><td>118.02 ms</td><td>764,082</td></tr><tr><td>as-0187</td><td>/api/assets</td><td><span class="mono-status is-good">200 OK</span></td><td>31.08 ms</td><td>2,048,221</td></tr><tr><td>as-0188</td><td>/api/notify</td><td><span class="mono-status is-error">500 RETRY</span></td><td>804.62 ms</td><td>64,018</td></tr></tbody></table></div>
        </article>
        <article class="mono-data-panel mono-diff-panel">
          <div class="mono-example-head"><span>Patch / 02</span><b>queue.ts</b></div>
          <pre class="mono-diff"><span class="mono-comment">// keep the queue observable</span><br><span class="mono-diff-minus">- const timeout = 5000;</span><br><span class="mono-diff-plus">+ const timeout = 4800;</span><br><span class="mono-keyword">const</span> <span class="mono-function">retry</span> <span class="mono-punc">=</span> <span class="mono-keyword">async</span> <span class="mono-name">job</span> <span class="mono-punc">=&gt;</span> {<br>  <span class="mono-key">metrics</span><span class="mono-punc">.</span><span class="mono-function">record</span><span class="mono-punc">(</span><span class="mono-string">&quot;queue.wait&quot;</span><span class="mono-punc">,</span> timeout<span class="mono-punc">);</span><br>  <span class="mono-keyword">return</span> <span class="mono-function">dispatch</span><span class="mono-punc">(</span>job<span class="mono-punc">);</span><br>};</pre>
        </article>
      </div>
    </section>`;
  const story = isMono ? {
    heading: 'Built for exact work. Drawn to stay readable.',
    intro: 'Asbir Mono brings the Asbir voice into code, logs, tables, and technical UI without turning utility into costume.',
    label: 'Asbir Mono',
    lede: 'A stable code grid with enough character to belong to Asbir.',
    paragraphs: ['The Geist Mono foundation supplies a dependable variable structure and a complete nine-weight range. Asbir keeps the coding system deliberately distinct from Sans: a two-storey a and a slashed zero.', 'The result stays quiet in a terminal and structured in a table. I, l, and 1 are purposefully distinct; punctuation has enough presence to scan quickly; every encoded visible character keeps the same 600-unit advance.', 'Asbir Mono is now approved for production, with Roman and true italic families, clean release binaries, and a separately packaged terminal companion.'],
    foot: ['600-unit advance / slashed zero', 'Code + data + technical UI', 'Asbir Mono / 1.1.0'],
  } : {
    heading: 'Built for products. Drawn for presence.', intro: 'Asbir Sans brings the clarity of a product UI into the wider Asbir Tech identity, without flattening the character out of it.', label: 'Asbir Sans', lede: 'One type system for the interface and the identity around it.',
    paragraphs: ['Asbir Sans began with a straightforward need: a clearer, more expressive voice for Asbir products. Instead of separating the functional from the recognizable, the family was developed as one system, quietly precise in the UI and more present in brand moments.', 'Its high x-height and open apertures give dense interface text room to breathe. Measured spacing keeps the texture steady across navigation, tables, and product copy; at display scale, the proportions open into something bolder and more editorial.', 'The result is a family that can carry a button label and a launch headline with the same underlying logic: clear enough to use every day, distinctive enough to belong to Asbir Tech.'],
    foot: ['High lowercase / open apertures', 'Product UI + brand identity', 'Asbir Sans / 1.1.0'],
  };
  const release = isMono ? {
    heading: 'Asbir Mono 1.1.0 is ready to ship.', description: 'The approved Asbir Mono release: Roman and true italic families, default coding ligatures, technical Unicode arrows, clean production binaries, and a separately named Nerd Font / Powerline terminal TTF.',
    action: '<a class="release-download" href="/downloads/AsbirMono-1.1.0.zip" download>Download all Asbir Mono files <b>↓</b></a>',
    status: '1.1.0 · approved', axes: 'wght 100—900', coverage: 'Latin / Cyrillic<br>Vietnamese / symbols', license: 'Asbir Mono is an OFL-compliant derivative of Geist Mono. It may be used, studied, modified, embedded, and redistributed under the terms of the license.',
  } : {
    heading: 'Asbir Sans 1.1.0 is ready to ship.', description: 'The approved Asbir Sans release for product, brand, and engineering. Download the complete family or choose a format below.',
    action: '<a class="release-download" href="/downloads/AsbirSans-1.1.0.zip" download>Download all Asbir Sans files <b>↓</b></a>',
    status: '1.1.0', axes: 'wght 100—900<br>opsz 14—32', coverage: 'Latin / Greek<br>Cyrillic / Vietnamese', license: 'Asbir Sans is an OFL-compliant derivative of Inter. It may be used, studied, modified, embedded, and redistributed under the terms of the license.',
  };
  return `
    <section class="family-section style-showcase" aria-labelledby="styles-heading">
      <div class="section-heading"><div><span class="section-index">01 / Family styles</span><h2 id="styles-heading">One family. Nine weights.</h2></div><p>${family.description}</p></div>
      <div class="style-list">${weightStyles.map(([weight, name]) => `<article class="style-row"><div class="style-meta"><span>${String(weight).padStart(3, '0')}</span></div><div class="style-word ${familyClass}" style="font-weight:${weight}; --family-tracking:${state.tracking / 1000}em">${name}</div></article>`).join('')}</div>
    </section>
    <section class="family-section glyph-section" aria-labelledby="glyphs-heading">
      <div class="section-heading"><div><span class="section-index">02 / Character set</span><h2 id="glyphs-heading">Every character has a job.</h2></div><p>${glyphDescription}</p></div>
      <div class="glyph-tabs" role="group" aria-label="Glyph groups">${(isMono ? [['latin','Latin'],['figures','Figures'],['punctuation','Punctuation'],['accents','Accents'],['cyrillic','Cyrillic'],['all','All glyphs']] : [['latin','Latin'],['figures','Figures'],['punctuation','Punctuation'],['accents','Accents'],['greek','Greek'],['cyrillic','Cyrillic'],['all','All glyphs']]).map(([key, label]) => `<button class="glyph-tab ${state.glyphSet === key ? 'is-active' : ''}" data-glyph-set="${key}" aria-pressed="${state.glyphSet === key}">${label}</button>`).join('')}</div>
      <div class="glyph-grid ${familyClass}">${glyphs.map(glyph => `<span class="glyph-cell ${glyph === ' ' ? 'is-space' : ''}"><strong>${escapeHtml(glyph)}</strong><small>U+${glyph.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}</small></span>`).join('')}</div>
    </section>
    <section class="family-section feature-section" aria-labelledby="features-heading">
      <div class="section-heading"><div><span class="section-index">03 / OpenType</span><h2 id="features-heading">Details for the details.</h2></div><p>Asbir keeps the practical features close at hand: figures, fractions, alternates, ligatures, and the forms that make UI text easier to read.</p></div>
      <div class="feature-grid ${familyClass}">${featureCardsFor(family).map(([tag, name, sample]) => `<article class="feature-card"><div class="feature-card-head"><code>${tag}</code><span>${name}</span></div><div class="feature-sample" style="font-feature-settings:'${tag}' 1">${sample}</div></article>`).join('')}</div>
    </section>
    ${isMono ? monoDataSection : languageSection}
    <section class="family-section layout-section" aria-labelledby="layouts-heading">
      <div class="section-heading"><div><span class="section-index">05 / Layouts</span><h2 id="layouts-heading">Let the type set the pace.</h2></div><p>${isMono ? 'Code, numbers, and technical UI all use the same stable cell. The proof below focuses on the moments where a mono either earns trust or gets in the way.' : 'Display, reading, and interface text in the same family. Asbir Sans is built to move from a single expressive line to a complete product surface without changing its voice.'}</p></div>
      ${layoutShowcase}
    </section>
    ${isMono ? `
    <section class="family-section mono-showcase-section" aria-labelledby="mono-examples-heading">
      <div class="section-heading"><div><span class="section-index">Mono / In use</span><h2 id="mono-examples-heading">Make information feel exact.</h2></div><p>Code, timed states, system output, and compact metrics all benefit from a rhythm that stays aligned. Click any code block, terminal output, or table cell to edit it in place.</p></div>
      <div class="mono-showcase-grid">
        <article class="mono-example mono-countdown">
          <div class="mono-example-head"><span>Countdown / 01</span><b>Live state</b></div>
          <div class="mono-countdown-time" data-countdown>07:32:10</div>
          <div class="mono-countdown-foot"><span>Session begins in</span><span>UTC+08:00</span></div>
        </article>
        <article class="mono-example mono-editor">
          <div class="mono-example-head"><span>IDE / 02</span><b>asbir.ts</b></div>
          <div class="mono-editor-window">
            <div class="mono-editor-bar"><span class="mono-dots"><i></i><i></i><i></i></span><span>asbir.ts</span><span>⌘ S</span></div>
            <pre class="mono-code" aria-label="Asbir Mono code sample"><span class="mono-line">01</span> <span class="mono-keyword">const</span> <span class="mono-name">session</span> <span class="mono-punc">=</span> {<br><span class="mono-line">02</span>   <span class="mono-key">status</span><span class="mono-punc">:</span> <span class="mono-string">&quot;active&quot;</span><span class="mono-punc">,</span><br><span class="mono-line">03</span>   <span class="mono-key">startsAt</span><span class="mono-punc">:</span> <span class="mono-string">&quot;16:00&quot;</span><span class="mono-punc">,</span><br><span class="mono-line">04</span>   <span class="mono-key">seats</span><span class="mono-punc">:</span> <span class="mono-number">048</span><br><span class="mono-line">05</span> }<br><span class="mono-line">06</span> <span class="mono-name">queue</span><span class="mono-punc">.</span><span class="mono-name">start</span><span class="mono-punc">(</span><span class="mono-name">session</span><span class="mono-punc">);</span></pre>
          </div>
        </article>
        <article class="mono-example mono-json">
          <div class="mono-example-head"><span>Payload / 03</span><b>session.json</b></div>
          <pre class="mono-json-code" aria-label="JSON data sample">{<br>  <span class="mono-key">&quot;id&quot;</span><span class="mono-punc">:</span> <span class="mono-string">&quot;as-0184&quot;</span><span class="mono-punc">,</span><br>  <span class="mono-key">&quot;status&quot;</span><span class="mono-punc">:</span> <span class="mono-string">&quot;active&quot;</span><span class="mono-punc">,</span><br>  <span class="mono-key">&quot;latency&quot;</span><span class="mono-punc">:</span> <span class="mono-number">48.50</span><span class="mono-punc">,</span><br>  <span class="mono-key">&quot;regions&quot;</span><span class="mono-punc">:</span> [<span class="mono-string">&quot;apac&quot;</span><span class="mono-punc">,</span> <span class="mono-string">&quot;eu&quot;</span>]<br>}</pre>
        </article>
        <article class="mono-example mono-log">
          <div class="mono-example-head"><span>Terminal / 04</span><b>Build output</b></div>
          <pre class="mono-terminal" aria-label="Dense terminal output"><span class="mono-prompt">asbir@studio:~$</span> pnpm font:check<br><span class="mono-comment">[fontbakery]</span> 164 checks passed<br><span class="mono-comment">[glyphs]</span>   2,987 mapped / 0 missing<br><span class="mono-comment">[build]</span>    AsbirMono-Review-VF.ttf <span class="mono-good">done</span><br><span class="mono-prompt">asbir@studio:~$</span> <span class="mono-cursor">_</span></pre>
        </article>
        <article class="mono-example mono-readout">
          <div class="mono-example-head"><span>Readout / 05</span><b>Product utility</b></div>
          <div class="mono-readout-grid"><div><strong>128</strong><span>requests</span></div><div><strong>42ms</strong><span>response</span></div><div><strong>99.9%</strong><span>uptime</span></div></div>
        </article>
        <article class="mono-example mono-trace">
          <div class="mono-example-head"><span>Trace / 06</span><b>Failure state</b></div>
          <div class="mono-trace-list"><div><span>12:04:08.422</span><strong>POST /v1/sessions</strong><em class="mono-trace-good">201</em></div><div><span>12:04:08.470</span><strong>GET /v1/sessions/as-0184/events</strong><em class="mono-trace-good">200</em></div><div><span>12:04:09.275</span><strong>PATCH /v1/sessions/as-0184/notify</strong><em class="mono-trace-warn">429</em></div><div><span>12:04:14.076</span><strong>retry-after: 4.8s</strong><em class="mono-trace-error">retry</em></div></div>
        </article>
      </div>
    </section>` : ''}
    ${isMono ? '' : `<section class="family-section story-section" aria-labelledby="story-heading">
      <div class="section-heading"><div><span class="section-index">06 / The story</span><h2 id="story-heading">${story.heading}</h2></div><p>${story.intro}</p></div>
      <div class="story-layout"><div class="story-primary"><div class="story-caption"><span>Origin / 01</span><b>${story.label}</b></div><p class="story-lede">${story.lede}</p></div><div class="story-copy">${story.paragraphs.map(paragraph => `<p>${paragraph}</p>`).join('')}</div></div>
      <div class="story-foot">${story.foot.map(item => `<span>${item}</span>`).join('')}</div>
    </section>`}
    <section class="family-section release-section" aria-labelledby="release-heading">
      <div class="section-heading"><div><span class="section-index">${isMono ? '06' : '07'} / Release files</span><h2 id="release-heading">${release.heading}</h2></div><div class="release-heading-side"><p>${release.description}</p>${release.action}</div></div>
      <div class="release-grid ${isMono ? 'is-mono' : ''}"><a class="release-card is-primary" href="/downloads/${prefix}-Review-VF.ttf" download><span class="release-type">Variable TTF</span><strong>${family.name} Variable</strong><small>${release.axes.replace('<br>', ' · ')} · Roman <b>↓</b></small></a>${hasItalic ? `<a class="release-card" href="/downloads/${prefix}-Review-Italic-VF.ttf" download><span class="release-type">Italic variable</span><strong>${family.name} Italic</strong><small>${release.axes.replace('<br>', ' · ')} · True italic <b>↓</b></small></a>` : ''}<a class="release-card" href="/downloads/${prefix}-Review-Regular.ttf" download><span class="release-type">Static TTF</span><strong>${family.name} Regular</strong><small>TrueType · Regular 400 <b>↓</b></small></a><a class="release-card" href="/downloads/${prefix}-Review-Regular.otf" download><span class="release-type">CFF OTF</span><strong>${family.name} Regular</strong><small>OpenType · CFF outlines <b>↓</b></small></a>${hasItalic ? `<a class="release-card" href="/downloads/web/${prefix}/${prefix}.css" download><span class="release-type">Web loading kit</span><strong>${family.name} CSS</strong><small>WOFF2 · normal + italic <b>↓</b></small></a>` : ''}${isMono ? '<a class="release-card" href="/downloads/AsbirMono-NerdFont-Review-Regular.ttf" download><span class="release-type">Terminal TTF</span><strong>Asbir Mono Nerd Font</strong><small>Powerline / icons · Regular 400 <b>↓</b></small></a>' : ''}</div>
    </section>
    <section class="family-section details-section" aria-labelledby="details-heading">
      <div class="section-heading"><div><span class="section-index">${isMono ? '07' : '08'} / Details &amp; license</span><h2 id="details-heading">${isMono ? 'Everything you need to ship it.' : 'Everything you need to ship it.'}</h2></div><p>${isMono ? 'Roman and true italic families, fixed-cell metrics, terminal companion, and web loading files are included in the approved production package.' : 'One approved release, documented clearly for design, engineering, and anyone responsible for putting the family into the world.'}</p></div>
      <div class="details-layout"><div class="details-grid"><div class="detail-item"><span>Family</span><strong>${family.name}</strong></div><div class="detail-item"><span>Version</span><strong>${release.status}</strong></div><div class="detail-item"><span>Axes</span><strong>${release.axes}</strong></div><div class="detail-item"><span>Coverage</span><strong>${release.coverage}</strong></div><div class="detail-item"><span>Formats</span><strong>Variable TTF<br>Static TTF / CFF OTF</strong></div><div class="detail-item"><span>Designed by</span><strong>Asbir Tech<br>Product Design Department</strong></div></div><aside class="license-panel"><span>License</span><h3>SIL Open Font License 1.1</h3><p>${release.license}</p><a href="https://scripts.sil.org/OFL" target="_blank" rel="noreferrer">Read third-party notices <b>↗</b></a></aside></div>
    </section>`;
}

function getGlyphs(group) {
  if (group === 'all') return (glyphCodepoints[state.family] || []).map(codepoint => String.fromCodePoint(codepoint));
  const groups = group === 'all' ? Object.values(glyphGroups) : [glyphGroups[group] || glyphGroups.latin];
  return Array.from(new Set(groups.join('').split('')));
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

function bind() {
  ['size', 'weight', 'tracking'].forEach(key => document.querySelector(`#${key}`).addEventListener('input', event => { state[key] = Number(event.target.value); render(); }));
  document.querySelector('#figures').addEventListener('change', event => { state.figures = event.target.value; render(); });
  document.querySelectorAll('[data-set]').forEach(button => button.addEventListener('click', () => { state.mode = button.dataset.set; state.text = sets[state.mode]; render(); }));
  document.querySelectorAll('[data-family]:not(:disabled)').forEach(button => button.addEventListener('click', () => { state.family = button.dataset.family; if (state.family === 'mono' && state.glyphSet === 'greek') state.glyphSet = 'latin'; if (state.family === 'mono' && state.figures !== 'tnum') state.figures = 'tnum'; render(); }));
  document.querySelectorAll('[data-glyph-set]').forEach(button => button.addEventListener('click', () => { state.glyphSet = button.dataset.glyphSet; render(); }));
  document.querySelector('#guide-toggle').addEventListener('click', () => { state.guides = !state.guides; render(); });
  document.querySelectorAll('.proof-copy, .hero-copy').forEach(proof => proof.addEventListener('input', event => { state.text = event.currentTarget.textContent.replace(/\n/g, ' '); document.querySelectorAll('.proof-copy, .hero-copy').forEach(other => { if (other !== event.currentTarget) other.textContent = state.text; }); }));
  document.onkeydown = event => { const target = document.activeElement; const isTyping = target?.isContentEditable || ['INPUT', 'SELECT', 'TEXTAREA'].includes(target?.tagName); if (event.key.toLowerCase() === 'g' && !isTyping) { state.guides = !state.guides; render(); } };
}

function bindMonoCountdown() {
  const element = document.querySelector('[data-countdown]');
  if (!element) return;
  let remaining = 7 * 3600 + 32 * 60 + 10;
  const update = () => {
    const hours = String(Math.floor(remaining / 3600)).padStart(2, '0');
    const minutes = String(Math.floor((remaining % 3600) / 60)).padStart(2, '0');
    const seconds = String(remaining % 60).padStart(2, '0');
    element.textContent = `${hours}:${minutes}:${seconds}`;
  };
  update();
  monoCountdownTimer = setInterval(() => {
    remaining = Math.max(remaining - 1, 0);
    update();
  }, 1000);
}

function bindMonoExamples() {
  const editableSamples = document.querySelectorAll('.mono-layout-code, .mono-code, .mono-json-code, .mono-terminal');
  editableSamples.forEach((sample, index) => {
    sample.contentEditable = 'true';
    sample.spellcheck = false;
    sample.classList.add('is-editable');
    sample.setAttribute('role', 'textbox');
    sample.setAttribute('aria-multiline', 'true');
    sample.setAttribute('aria-label', `Editable Mono code sample ${index + 1}`);
    sample.title = 'Click to edit this code sample';
  });

  document.querySelectorAll('.mono-data-table tbody td').forEach(cell => {
    cell.contentEditable = 'true';
    cell.spellcheck = false;
    cell.classList.add('is-editable');
    cell.setAttribute('role', 'textbox');
    cell.setAttribute('aria-label', 'Editable data table cell');
    cell.title = 'Click to edit this value';
    cell.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        event.preventDefault();
        cell.blur();
      }
    });
  });
}

function toast(message) { const element = document.querySelector('.toast'); element.textContent = message; element.classList.add('show'); setTimeout(() => element.classList.remove('show'), 2500); }
render();
