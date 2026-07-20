import { filterIcons, getCategories, getPack, iconAssetUrl } from './catalog.js';
import { browseHref, iconHref } from './router.js';
import { escapeHtml } from './render.js';

const VARIANTS = [
  ['all', 'All'],
  ['outline', 'Outline'],
  ['filled', 'Filled'],
];

function filterLink(route, overrides = {}, label = '', active = false) {
  const href = browseHref({
    pack: overrides.pack ?? route.pack,
    category: overrides.category ?? route.category,
    query: overrides.query ?? route.query,
    variant: overrides.variant ?? route.variant,
  });
  return `<a class="icon-filter-chip ${active ? 'is-active' : ''}" data-icon-nav href="${href}" aria-current="${active ? 'page' : 'false'}">${escapeHtml(label)}</a>`;
}

function renderHeader() {
  return `<header class="icon-header">
    <a class="icon-brand" href="/" aria-label="Back to Asbir Type Studio"><span class="icon-brand-mark">A</span><span><strong>Asbir</strong><small>Icons</small></span></a>
    <nav class="icon-header-nav" aria-label="Icon library navigation"><a href="/icons" data-icon-nav>Browse icons</a><a href="/">Type studio</a></nav>
    <span class="icon-header-version">Soft / 1.0.0</span>
  </header>`;
}

export function renderBrowsePage(route) {
  const pack = getPack(route.pack);
  if (!pack) {
    return `<div class="icon-surface"><main class="icon-not-found" aria-labelledby="icon-not-found-title"><span class="icon-eyebrow">Pack unavailable</span><h1 id="icon-not-found-title">That icon pack is not here.</h1><p>Choose the available Soft pack to continue browsing.</p><a class="icon-button icon-button-primary" href="/icons">Browse Soft icons</a></main></div>`;
  }
  const results = filterIcons(route);
  const categories = getCategories(route.pack);
  const previewVariant = route.variant === 'filled' ? 'filled' : 'outline';
  return `<div class="icon-surface">
    ${renderHeader()}
    <main class="icon-main icon-browse" aria-labelledby="icon-browse-title">
      <div class="icon-breadcrumbs"><a href="/">Asbir</a><span>/</span><strong>Icons</strong><span>/</span><span>${escapeHtml(pack.name)}</span></div>
      <section class="icon-browse-hero">
        <div><span class="icon-eyebrow">${escapeHtml(pack.name)} pack / ${pack.version}</span><h1 id="icon-browse-title">Icons for the interface layer.</h1><p>${escapeHtml(pack.description)} Find a symbol, inspect its construction, and take the exact asset into your product.</p></div>
        <div class="icon-browse-count"><strong>${pack.iconCount}</strong><span>semantic icons<br>${pack.iconCount * 2} SVG variants</span></div>
      </section>
      <section class="icon-browser-panel" aria-label="Browse icon collection">
        <form class="icon-search-form" data-icon-search-form>
          <label class="icon-search-label" for="icon-search">Search icons</label>
          <span class="icon-search-mark" aria-hidden="true">⌕</span>
          <input id="icon-search" name="q" value="${escapeHtml(route.query)}" type="search" placeholder="Search by name or keyword" aria-label="Search icons" autocomplete="off">
          <kbd>⌘ K</kbd>
        </form>
        <div class="icon-filter-toolbar">
          <div class="icon-filter-group" aria-label="Icon variants"><span class="icon-filter-label">Weight</span>${VARIANTS.map(([value, label]) => filterLink(route, { variant: value }, label, route.variant === value || (value === 'all' && route.variant === 'all'))).join('')}</div>
          <div class="icon-filter-group icon-category-group" aria-label="Icon categories"><span class="icon-filter-label">Category</span>${filterLink(route, { category: 'all' }, 'All', route.category === 'all')}${categories.map(category => filterLink(route, { category }, category, route.category === category)).join('')}</div>
        </div>
      </section>
      <div class="icon-result-bar"><span>${results.length} ${results.length === 1 ? 'icon' : 'icons'}${route.query ? ` for “${escapeHtml(route.query)}”` : ''}</span><span>24 × 24 / currentColor</span></div>
      ${results.length ? `<section class="icon-grid" data-icon-grid aria-label="${escapeHtml(pack.name)} icons">${results.map(icon => `<a class="icon-tile" data-icon-nav href="${iconHref(icon.pack, icon.slug)}" aria-label="${escapeHtml(icon.name)}, ${escapeHtml(icon.pack)} icon"><span class="icon-tile-art"><img src="${iconAssetUrl(icon, previewVariant)}" alt="" loading="lazy"></span><strong>${escapeHtml(icon.name)}</strong><small>${escapeHtml(icon.category)}</small></a>`).join('')}</section>` : `<section class="icon-empty-state" aria-live="polite"><span class="icon-eyebrow">No matches</span><h2>Nothing in this collection yet.</h2><p>Try a broader keyword or reset the filters to see the full Soft pack.</p><a class="icon-button" href="/icons">Reset search</a></section>`}
    </main>
    <div class="icon-status" data-icon-status role="status" aria-live="polite"></div>
  </div>`;
}
