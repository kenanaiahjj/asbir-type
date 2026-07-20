const VALID_VARIANTS = new Set(['all', 'outline', 'filled']);

function cleanPath(pathname) {
  const path = pathname.replace(/\/+/g, '/').replace(/\/$/, '');
  return path || '/';
}

export function parseRoute(pathname, search = '') {
  const path = cleanPath(pathname);
  if (path === '/') return { kind: 'studio' };

  const parts = path.split('/').filter(Boolean);
  if (parts[0] === 'icons' && parts.length === 1) {
    const params = new URLSearchParams(search);
    const variant = VALID_VARIANTS.has(params.get('variant')) ? params.get('variant') : 'all';
    return {
      kind: 'browse',
      pack: params.get('pack') || 'soft',
      category: params.get('category') || 'all',
      query: params.get('q') || '',
      variant,
    };
  }

  if (parts[0] === 'icon' && parts.length === 2) {
    return { kind: 'detail', pack: 'soft', slug: decodeURIComponent(parts[1]) };
  }

  if (parts[0] === 'icon' && parts.length === 3) {
    return { kind: 'detail', pack: decodeURIComponent(parts[1]), slug: decodeURIComponent(parts[2]) };
  }

  return { kind: 'not-found', path };
}

export function browseHref({ pack = 'soft', category = 'all', query = '', variant = 'all' } = {}) {
  const params = new URLSearchParams();
  if (pack) params.set('pack', pack);
  if (category && category !== 'all') params.set('category', category);
  if (query.trim()) params.set('q', query.trim());
  if (variant && variant !== 'all') params.set('variant', variant);
  const queryString = params.toString();
  return `/icons${queryString ? `?${queryString}` : ''}`;
}

export function iconHref(pack = 'soft', slug) {
  return pack === 'soft'
    ? `/icon/${encodeURIComponent(slug)}`
    : `/icon/${encodeURIComponent(pack)}/${encodeURIComponent(slug)}`;
}
