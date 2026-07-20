import './icons.css';
import { getIcon, iconAssetUrl } from './catalog.js';
import { parseRoute, browseHref } from './router.js';
import { codeExamples, renderInlineSvg } from './render.js';
import { renderBrowsePage } from './browse.js';
import { renderDetailPage, renderNotFoundPage } from './detail.js';

const PREVIEW_COLOR = '#f5f1e9';

function setStatus(root, message) {
  const status = root.querySelector('[data-icon-status]');
  if (!status) return;
  status.textContent = message;
  status.classList.add('is-visible');
  window.clearTimeout(status._timer);
  status._timer = window.setTimeout(() => status.classList.remove('is-visible'), 2400);
}

export async function copyText(text) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch {}
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.setAttribute('readonly', '');
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.append(textarea);
  textarea.select();
  const copied = document.execCommand('copy');
  textarea.remove();
  return copied;
}

function downloadFile(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function loadSvg(icon, variant) {
  const response = await fetch(iconAssetUrl(icon, variant));
  if (!response.ok) throw new Error(`Unable to load ${variant} SVG`);
  return response.text();
}

async function exportRaster(svg, size, color, format) {
  const normalized = renderInlineSvg(svg, { size, color });
  const image = new Image();
  const imageUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(normalized)}`;
  await new Promise((resolve, reject) => {
    image.onload = resolve;
    image.onerror = () => reject(new Error('Unable to rasterize SVG'));
    image.src = imageUrl;
  });
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext('2d');
  if (!context) throw new Error('Canvas is unavailable');
  context.drawImage(image, 0, 0, size, size);
  const mime = format === 'webp' ? 'image/webp' : 'image/png';
  const blob = await new Promise(resolve => canvas.toBlob(resolve, mime));
  if (!blob) throw new Error(`${format.toUpperCase()} export is unavailable`);
  return blob;
}

function bindInternalLinks(root) {
  root.querySelectorAll('a[data-icon-nav]').forEach(link => link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank') return;
    const url = new URL(link.href, window.location.origin);
    if (url.origin !== window.location.origin) return;
    event.preventDefault();
    window.history.pushState({}, '', `${url.pathname}${url.search}`);
    window.dispatchEvent(new PopStateEvent('popstate'));
  }));
}

function bindBrowse(root, route) {
  bindInternalLinks(root);
  const form = root.querySelector('[data-icon-search-form]');
  form?.addEventListener('submit', event => {
    event.preventDefault();
    const query = new FormData(form).get('q')?.toString() || '';
    const params = new URLSearchParams(window.location.search);
    window.history.pushState({}, '', browseHref({
      pack: route.pack,
      category: params.get('category') || 'all',
      query,
      variant: params.get('variant') || 'all',
    }));
    window.dispatchEvent(new PopStateEvent('popstate'));
  });
  root.querySelector('#icon-search')?.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.currentTarget.value = '';
      event.currentTarget.form.requestSubmit();
    }
  });
}

async function bindDetail(root, route) {
  bindInternalLinks(root);
  const icon = getIcon(route.pack, route.slug);
  if (!icon) return;
  const state = { variant: 'outline', previewSize: 64, exportSize: 64, color: 'currentColor', customColor: false, tab: 'js', svg: null, examples: null };
  const cache = new Map();
  const loadSelectedSvg = async () => {
    if (!cache.has(state.variant)) cache.set(state.variant, await loadSvg(icon, state.variant));
    state.svg = cache.get(state.variant);
    state.examples = codeExamples(icon, state.variant, state.svg);
  };

  const updateVisuals = async () => {
    try {
      await loadSelectedSvg();
      const preview = root.querySelector('.icon-proof-canvas [data-icon-preview]');
      if (preview) {
        const color = state.customColor ? state.color : PREVIEW_COLOR;
        const inline = renderInlineSvg(state.svg, { size: state.previewSize, color })
          .replace('<svg ', `<svg class="icon-preview-inline" data-icon-preview role="img" aria-label="${icon.name} icon" `);
        preview.outerHTML = inline;
      }
      root.querySelectorAll('.icon-context-card [data-icon-preview]').forEach(image => {
        image.src = iconAssetUrl(icon, state.variant);
      });
      root.querySelector('[data-preview-size]').textContent = `${state.previewSize}px`;
      root.querySelector('[data-export-size]').textContent = `${state.exportSize}px`;
      root.querySelector('[data-preview-variant]').textContent = state.variant;
      root.querySelector('[data-size-output]').textContent = `${state.previewSize}px`;
      root.querySelector('[data-code-panel] code').textContent = state.examples[state.tab];
    } catch (error) {
      setStatus(root, error.message);
    }
  };

  root.querySelectorAll('[data-icon-variant]').forEach(button => button.addEventListener('click', () => {
    state.variant = button.dataset.iconVariant;
    root.querySelectorAll('[data-icon-variant]').forEach(candidate => {
      const active = candidate === button;
      candidate.classList.toggle('is-active', active);
      candidate.setAttribute('aria-pressed', String(active));
    });
    updateVisuals();
  }));
  root.querySelector('[data-icon-size]')?.addEventListener('input', event => {
    state.previewSize = Number(event.target.value);
    updateVisuals();
  });
  root.querySelectorAll('[data-export-size-value]').forEach(button => button.addEventListener('click', () => {
    state.exportSize = Number(button.dataset.exportSizeValue);
    root.querySelectorAll('[data-export-size-value]').forEach(candidate => candidate.classList.toggle('is-active', candidate === button));
    updateVisuals();
  }));
  root.querySelector('[data-custom-color]')?.addEventListener('change', event => {
    state.customColor = event.target.checked;
    updateVisuals();
  });
  root.querySelector('[data-icon-color]')?.addEventListener('input', event => {
    state.color = event.target.value;
    if (!state.customColor) {
      root.querySelector('[data-custom-color]').checked = true;
      state.customColor = true;
    }
    updateVisuals();
  });
  root.querySelectorAll('[data-code-tab]').forEach(button => button.addEventListener('click', () => {
    state.tab = button.dataset.codeTab;
    root.querySelectorAll('[data-code-tab]').forEach(candidate => candidate.setAttribute('aria-selected', String(candidate === button)));
    updateVisuals();
  }));
  root.querySelector('[data-icon-action="copy-name"]')?.addEventListener('click', async () => setStatus(root, await copyText(icon.slug) ? 'Icon name copied.' : 'Copy unavailable.'));
  root.querySelector('[data-icon-action="copy-svg"]')?.addEventListener('click', async () => {
    await loadSelectedSvg();
    setStatus(root, await copyText(renderInlineSvg(state.svg, { size: state.previewSize, color: state.customColor ? state.color : 'currentColor' })) ? 'SVG copied.' : 'Copy unavailable.');
  });
  root.querySelector('[data-icon-action="copy-jsx"]')?.addEventListener('click', async () => {
    await loadSelectedSvg();
    setStatus(root, await copyText(state.examples.react) ? 'JSX copied.' : 'Copy unavailable.');
  });
  root.querySelectorAll('[data-export-format]').forEach(button => button.addEventListener('click', async () => {
    try {
      await loadSelectedSvg();
      const format = button.dataset.exportFormat;
      const color = state.customColor ? state.color : 'currentColor';
      if (format === 'svg') downloadFile(new Blob([renderInlineSvg(state.svg, { size: state.exportSize, color })], { type: 'image/svg+xml' }), `${icon.slug}-${state.variant}-${state.exportSize}.svg`);
      else downloadFile(await exportRaster(state.svg, state.exportSize, color, format), `${icon.slug}-${state.variant}-${state.exportSize}.${format}`);
      setStatus(root, `${format.toUpperCase()} downloaded.`);
    } catch (error) {
      setStatus(root, error.message);
    }
  }));
  await updateVisuals();
}

export function mountIconRoute(root) {
  const route = parseRoute(window.location.pathname, window.location.search);
  if (route.kind === 'studio') {
    root.className = '';
    document.title = 'Asbir Sans Studio';
    return false;
  }
  root.className = 'icon-app';
  if (route.kind === 'browse') {
    root.innerHTML = renderBrowsePage(route);
    document.title = 'Asbir Icons — Browse';
    bindBrowse(root, route);
  } else if (route.kind === 'detail') {
    root.innerHTML = renderDetailPage(route);
    const icon = getIcon(route.pack, route.slug);
    document.title = icon ? `Asbir Icons — ${icon.name}` : 'Asbir Icons — Not found';
    bindDetail(root, route);
  } else {
    root.innerHTML = renderNotFoundPage('This route is not in the icon library.', 'Use the browser to find the Soft pack and its icons.');
    document.title = 'Asbir Icons — Not found';
    bindInternalLinks(root);
  }
  return true;
}
