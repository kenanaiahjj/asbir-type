import test from 'node:test';
import assert from 'node:assert/strict';

async function loadHelpers() {
  try {
    const [catalog, router, render] = await Promise.all([
      import('../src/icons/catalog.js'),
      import('../src/icons/router.js'),
      import('../src/icons/render.js'),
    ]);
    return { ...catalog, ...router, ...render };
  } catch (error) {
    assert.fail(`icon helper modules are not implemented: ${error.message}`);
  }
}

async function loadPageRenderers() {
  try {
    const [browse, detail] = await Promise.all([
      import('../src/icons/browse.js'),
      import('../src/icons/detail.js'),
    ]);
    return { ...browse, ...detail };
  } catch (error) {
    assert.fail(`icon page renderers are not implemented: ${error.message}`);
  }
}

test('parses browse filters and default detail routes', async () => {
  const { parseRoute } = await loadHelpers();
  assert.deepEqual(parseRoute('/icons', '?pack=soft&category=Navigation&q=arrow'), {
    kind: 'browse', pack: 'soft', category: 'Navigation', query: 'arrow', variant: 'all',
  });
  assert.deepEqual(parseRoute('/icon/search', ''), { kind: 'detail', pack: 'soft', slug: 'search' });
});

test('builds shareable links', async () => {
  const { browseHref, iconHref } = await loadHelpers();
  assert.equal(browseHref({ pack: 'soft', category: 'Navigation', query: 'arrow', variant: 'outline' }), '/icons?pack=soft&category=Navigation&q=arrow&variant=outline');
  assert.equal(iconHref('soft', 'search'), '/icon/search');
  assert.equal(iconHref('technical', 'terminal'), '/icon/technical/terminal');
});

test('filters semantic records without duplicating outline and filled variants', async () => {
  const { filterIcons, getIcon } = await loadHelpers();
  const results = filterIcons({ pack: 'soft', query: 'search', category: 'all', variant: 'filled' });
  assert.ok(results.length >= 1);
  assert.ok(results.every(icon => icon.pack === 'soft'));
  assert.equal(getIcon('soft', results[0].slug).slug, results[0].slug);
});

test('normalizes SVG size and color without losing the Asbir viewBox', async () => {
  const { renderInlineSvg } = await loadHelpers();
  const svg = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M1 1H2Z"/></svg>';
  const result = renderInlineSvg(svg, { size: 64, color: '#ff6b2c' });
  assert.match(result, /width="64"/);
  assert.match(result, /height="64"/);
  assert.match(result, /viewBox="0 0 24 24"/);
  assert.match(result, /#ff6b2c/);
});

test('rejects unsafe SVG markup', async () => {
  const { renderInlineSvg } = await loadHelpers();
  assert.throws(() => renderInlineSvg('<svg><script>alert(1)</script></svg>', { size: 24, color: 'currentColor' }), /unsafe SVG/i);
});

test('browse markup includes accessible search, filters, grid links, and pack metadata', async () => {
  const { renderBrowsePage } = await loadPageRenderers();
  const html = renderBrowsePage({ kind: 'browse', pack: 'soft', category: 'all', query: '', variant: 'all' });
  assert.match(html, /aria-label="Search icons"/);
  assert.match(html, /data-icon-grid/);
  assert.match(html, /href="\/icon\//);
  assert.match(html, /Soft/);
});

test('detail markup includes exports, code tabs, props, context, and related links', async () => {
  const { renderDetailPage } = await loadPageRenderers();
  const html = renderDetailPage({ kind: 'detail', pack: 'soft', slug: 'search' });
  for (const label of ['Copy Name', 'Copy SVG', 'SVG', 'PNG', 'WebP', 'React', 'Props', 'In context', 'Related icons']) {
    assert.match(html, new RegExp(label));
  }
  assert.match(html, /aria-label="Outline or filled variant"/);
});
