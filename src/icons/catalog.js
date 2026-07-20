import catalogData from './catalog.json' with { type: 'json' };

export const catalog = catalogData;
export const packs = catalogData.packs;
export const icons = catalogData.icons;

const packMap = new Map(packs.map(pack => [pack.id, pack]));
const iconMap = new Map(icons.map(icon => [`${icon.pack}/${icon.slug}`, icon]));

export function getPack(packId = 'soft') {
  return packMap.get(packId) || null;
}

export function getIcon(packId = 'soft', slug) {
  return iconMap.get(`${packId}/${slug}`) || null;
}

export function getCategories(packId = 'soft') {
  return [...new Set(icons.filter(icon => icon.pack === packId).map(icon => icon.category))];
}

export function iconAssetUrl(icon, variant = 'outline') {
  if (!icon) return '';
  return variant === 'filled' ? icon.filledAsset : icon.outlineAsset;
}

function searchableText(icon) {
  return [icon.name, icon.slug, icon.category, ...icon.aliases, ...icon.keywords]
    .join(' ')
    .toLowerCase();
}

export function filterIcons({ pack = 'soft', query = '', category = 'all', variant = 'all' } = {}) {
  const normalizedQuery = query.trim().toLowerCase();
  return icons.filter(icon => {
    if (icon.pack !== pack) return false;
    if (category !== 'all' && icon.category !== category) return false;
    if (variant !== 'all' && !['outline', 'filled'].includes(variant)) return false;
    return !normalizedQuery || searchableText(icon).includes(normalizedQuery);
  });
}
