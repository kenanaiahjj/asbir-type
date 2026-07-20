import { iconAssetUrl } from './catalog.js';

const SAFE_COLOR = /^(?:currentColor|transparent|[a-zA-Z]+|#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\))$/;

export function escapeHtml(value = '') {
  return String(value).replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  }[character]));
}

export function renderInlineSvg(svg, { size = 24, color = 'currentColor' } = {}) {
  if (typeof svg !== 'string' || !svg.trim()) throw new Error('Invalid SVG');
  if (/<script\b|(?:href|xlink:href)\s*=\s*["']https?:\/\/|url\(/i.test(svg)) {
    throw new Error('Unsafe SVG markup');
  }
  if (!/viewBox=["']0 0 24 24["']/i.test(svg)) throw new Error('SVG must use the Asbir 24x24 viewBox');
  if (!SAFE_COLOR.test(String(color))) throw new Error('Unsafe SVG color');
  const root = svg.match(/<svg\b[^>]*>/i)?.[0];
  if (!root) throw new Error('Invalid SVG root');
  const sizeValue = Number(size);
  if (!Number.isFinite(sizeValue) || sizeValue <= 0) throw new Error('Invalid SVG size');
  let nextRoot = root;
  nextRoot = /\bwidth=/.test(nextRoot) ? nextRoot.replace(/\bwidth=["'][^"']*["']/i, `width="${sizeValue}"`) : nextRoot.replace('<svg', `<svg width="${sizeValue}"`);
  nextRoot = /\bheight=/.test(nextRoot) ? nextRoot.replace(/\bheight=["'][^"']*["']/i, `height="${sizeValue}"`) : nextRoot.replace('<svg', `<svg height="${sizeValue}"`);
  return svg.replace(root, nextRoot).replaceAll('currentColor', String(color));
}

function svgBody(svg) {
  return svg.replace(/<svg\b[^>]*>/i, '').replace(/<\/svg>\s*$/i, '').trim();
}

export function codeExamples(icon, variant, svg) {
  const body = svgBody(svg);
  const componentName = `${icon.name.replace(/[^a-zA-Z0-9]+/g, '')}Icon`;
  const asset = iconAssetUrl(icon, variant);
  const direct = renderInlineSvg(svg, { size: 24, color: 'currentColor' });
  const inlineProps = 'width={size} height={size} viewBox="0 0 24 24" fill="none" color={color}';
  return {
    js: `const icon = ${JSON.stringify(direct)};\ndocument.body.insertAdjacentHTML('beforeend', icon);`,
    cdn: `<img src="${asset}" width="24" height="24" alt="${escapeHtml(icon.name)} icon" />`,
    react: `export function ${componentName}({ size = 24, color = 'currentColor', ...props }) {\n  return (\n    <svg ${inlineProps} {...props}>${body}</svg>\n  );\n}`,
    reactNative: `export function ${componentName}({ size = 24, color = 'currentColor' }) {\n  return <Svg width={size} height={size} viewBox="0 0 24 24">${body}</Svg>;\n}`,
    vue: `<template>\n  <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" :color="color">${body}</svg>\n</template>`,
    svelte: `<script>\n  export let size = 24;\n  export let color = 'currentColor';\n</script>\n<svg width={size} height={size} viewBox="0 0 24 24" fill="none" color={color}>${body}</svg>`,
    flutter: `Icon(${componentName}.data, size: 24, color: color)`,
    direct,
  };
}
