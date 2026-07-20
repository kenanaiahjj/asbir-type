import { filterIcons, getIcon, getPack, iconAssetUrl } from './catalog.js';
import { browseHref, iconHref } from './router.js';
import { escapeHtml } from './render.js';

const SIZES = [16, 24, 32, 48, 64, 128, 256, 512];
const CODE_TABS = ['js', 'cdn', 'react', 'reactNative', 'vue', 'svelte', 'flutter', 'direct'];
const CODE_LABELS = { js: 'JS', cdn: 'CDN', react: 'React', reactNative: 'React Native', vue: 'Vue', svelte: 'Svelte', flutter: 'Flutter', direct: 'Direct' };

function header() {
  return `<header class="icon-header"><a class="icon-brand" href="/" aria-label="Back to Asbir Type Studio"><span class="icon-brand-mark">A</span><span><strong>Asbir</strong><small>Icons</small></span></a><nav class="icon-header-nav" aria-label="Icon library navigation"><a href="/icons" data-icon-nav>Browse icons</a><a href="/">Type studio</a></nav><span class="icon-header-version">Soft / 1.0.0</span></header>`;
}

function preview(icon, variant = 'outline', className = '') {
  return `<img class="icon-preview-image ${className}" data-icon-preview src="${iconAssetUrl(icon, variant)}" alt="${escapeHtml(icon.name)} icon">`;
}

function contextCard(label, content, icon, variant = 'outline') {
  return `<article class="icon-context-card"><span class="icon-context-label">${label}</span>${content.replaceAll('__ICON__', preview(icon, variant, 'icon-context-image'))}</article>`;
}

function renderProps() {
  return `<table class="icon-props-table"><thead><tr><th scope="col">Prop</th><th scope="col">Type</th><th scope="col">Default</th><th scope="col">Description</th></tr></thead><tbody><tr><th scope="row"><code>size</code></th><td><code>number | string</code></td><td><code>24</code></td><td>Icon size in pixels.</td></tr><tr><th scope="row"><code>color</code></th><td><code>string</code></td><td><code>currentColor</code></td><td>Any valid CSS color.</td></tr><tr><th scope="row"><code>weight</code></th><td><code>"Outline" | "Filled"</code></td><td><code>Outline</code></td><td>Icon variant.</td></tr><tr><th scope="row"><code>className?</code></th><td><code>string</code></td><td><code>—</code></td><td>Extra CSS classes.</td></tr></tbody></table>`;
}

function renderContext(icon) {
  return `<section class="icon-context-section" aria-labelledby="icon-context-title"><span class="icon-eyebrow">In context</span><h2 id="icon-context-title">See the ${escapeHtml(icon.name)} icon in real UI.</h2><div class="icon-context-grid">
    ${contextCard('Sidebar nav', `<nav class="context-sidebar"><strong>__ICON__ ${escapeHtml(icon.name)}</strong><span>Overview</span><span>Activity</span></nav>`, icon)}
    ${contextCard('Buttons', `<div class="context-buttons"><button class="context-primary">__ICON__ <span>Continue</span></button><button class="context-secondary">__ICON__ <span>Secondary</span></button></div>`, icon)}
    ${contextCard('Metric card', `<div class="context-metric"><span class="context-metric-icon">__ICON__</span><strong>12,480</strong><small>Total this month</small><em>↗ 19.5% vs last month</em></div>`, icon, 'filled')}
    ${contextCard('Notification', `<div class="context-notification"><span class="context-notification-icon">__ICON__</span><div><strong>All changes saved</strong><small>Your workspace is up to date.</small></div><button aria-label="Dismiss notification">×</button></div>`, icon, 'filled')}
    ${contextCard('Input field', `<div class="context-input"><span>__ICON__</span><span>Type something...</span></div><div class="context-input is-disabled"><span>__ICON__</span><span>Disabled</span></div>`, icon)}
    ${contextCard('Bottom tab bar', `<nav class="context-tabbar"><span class="is-active">__ICON__<small>Home</small></span><span>__ICON__<small>Explore</small></span><span>__ICON__<small>Profile</small></span></nav>`, icon)}
  </div></section>`;
}

export function renderNotFoundPage(title = 'That icon is not here.', description = 'Return to the library and choose another icon.') {
  return `<div class="icon-surface">${header()}<main class="icon-not-found" aria-labelledby="icon-not-found-title"><span class="icon-eyebrow">404 / Icon library</span><h1 id="icon-not-found-title">${escapeHtml(title)}</h1><p>${escapeHtml(description)}</p><a class="icon-button icon-button-primary" href="/icons">Browse all icons</a></main></div>`;
}

export function renderDetailPage(route) {
  const icon = getIcon(route.pack, route.slug);
  const pack = getPack(route.pack);
  if (!pack) return renderNotFoundPage('That icon pack is not here.', 'The Soft pack is available while additional Asbir packs are being developed.');
  if (!icon) return renderNotFoundPage('That icon is not here.', 'Try searching the Soft pack for another name or keyword.');
  const related = filterIcons({ pack: icon.pack, query: '', category: icon.category, variant: 'all' }).filter(candidate => candidate.slug !== icon.slug && icon.related.includes(candidate.slug));
  return `<div class="icon-surface">
    ${header()}
    <main class="icon-main icon-detail" aria-labelledby="icon-detail-title">
      <div class="icon-detail-topbar"><div class="icon-breadcrumbs"><a href="/icons">Asbir / Icons</a><span>/</span><a href="${browseHref({ pack: icon.pack, category: icon.category })}">${escapeHtml(icon.category)}</a><span>/</span><strong>${escapeHtml(icon.name)}</strong></div><a class="icon-back-link" href="/icons">← Back</a></div>
      <section class="icon-detail-hero">
        <div class="icon-proof-column"><div class="icon-proof-canvas"><div class="icon-proof-grid" aria-hidden="true"></div>${preview(icon)}<span class="icon-proof-size" data-preview-size>64px</span><span class="icon-proof-variant" data-preview-variant>outline</span></div><div class="icon-detail-name"><h1 id="icon-detail-title">${escapeHtml(icon.name)}</h1><span>${escapeHtml(icon.category)}</span><code>${escapeHtml(icon.slug)}</code></div><div class="icon-customize"><span class="icon-panel-label">Customize</span><div class="icon-variant-control" role="group" aria-label="Outline or filled variant"><button class="is-active" type="button" data-icon-variant="outline" aria-pressed="true">Outline</button><button type="button" data-icon-variant="filled" aria-pressed="false">Filled</button></div><label class="icon-size-control" for="detail-size">Size <output data-size-output>64px</output></label><input id="detail-size" type="range" min="16" max="512" step="1" value="64" data-icon-size aria-label="Preview size"><label class="icon-color-control"><input type="checkbox" data-custom-color> Custom color <input type="color" value="#ff6b2c" data-icon-color aria-label="Custom icon color"></label></div></div>
        <div class="icon-detail-tools"><div class="icon-action-grid"><button type="button" data-icon-action="copy-jsx">Copy JSX</button><button type="button" data-icon-action="copy-name">Copy Name</button><button type="button" data-icon-action="copy-svg">Copy SVG</button></div><div class="icon-export-panel"><div class="icon-export-head"><span class="icon-panel-label">Export size</span><output data-export-size>64px</output></div><div class="icon-size-chips">${SIZES.map(size => `<button type="button" data-export-size-value="${size}" class="${size === 64 ? 'is-active' : ''}">${size}</button>`).join('')}</div><div class="icon-download-grid"><button type="button" data-export-format="svg">↓ SVG</button><button type="button" data-export-format="png">↓ PNG</button><button type="button" data-export-format="webp">↓ WebP</button></div></div><div class="icon-code-panel"><div class="icon-code-tabs" role="tablist" aria-label="Code examples">${CODE_TABS.map((tab, index) => `<button type="button" role="tab" aria-selected="${index === 0}" data-code-tab="${tab}">${CODE_LABELS[tab]}</button>`).join('')}</div><pre class="icon-code" data-code-panel tabindex="0"><code>Loading SVG example…</code></pre></div><div class="icon-props"><span class="icon-panel-label">Props</span>${renderProps()}</div></div>
      </section>
      ${renderContext(icon)}
      <section class="icon-related" aria-labelledby="related-icons-title"><h2 id="related-icons-title">Related icons</h2><div class="icon-related-grid">${related.map(candidate => `<a class="icon-related-card" data-icon-nav href="${iconHref(candidate.pack, candidate.slug)}"><img src="${iconAssetUrl(candidate)}" alt=""><span>${escapeHtml(candidate.name)}</span></a>`).join('')}</div></section>
    </main>
    <div class="icon-status" data-icon-status role="status" aria-live="polite"></div>
  </div>`;
}
