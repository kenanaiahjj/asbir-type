#!/usr/bin/env python3
"""Generate the original Asbir Icons Soft pack and its browser manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEWBOX = '0 0 24 24'
STROKE = '2'
CATEGORIES = (
    'Actions', 'Arrows', 'Communication', 'Commerce', 'Content',
    'Devices', 'Files', 'Interface', 'Location', 'Media',
    'Navigation', 'People', 'Security', 'Status', 'Time',
)

ICON_NAMES = {
    'Actions': 'add remove edit delete save refresh undo redo copy paste move more'.split(),
    'Arrows': 'arrow-up arrow-down arrow-left arrow-right chevron-up chevron-down chevron-left chevron-right external-link expand collapse swap'.split(),
    'Communication': 'mail send message chat phone video-call mic voicemail at-sign mention bell inbox'.split(),
    'Commerce': 'cart bag credit-card wallet receipt tag price gift coupon cash barcode store'.split(),
    'Content': 'file file-text folder image video music link paperclip clipboard archive book bookmark'.split(),
    'Devices': 'laptop desktop tablet mobile keyboard mouse printer camera headphones speaker wifi battery'.split(),
    'Files': 'upload download cloud cloud-upload cloud-download database server hard-drive file-plus file-minus file-check file-lock'.split(),
    'Interface': 'search filter sliders grid list settings eye eye-off lock unlock code'.split(),
    'Location': 'map map-pin compass globe navigation route car bus train airplane bicycle parking'.split(),
    'Media': 'play pause stop skip-next skip-prev volume volume-off fullscreen cast radio tv live'.split(),
    'Navigation': 'home dashboard activity calendar clock history trend-up trend-down sort nav-menu sidebar login'.split(),
    'People': 'user users user-plus user-minus user-check user-x team profile id-card accessibility baby smile'.split(),
    'Security': 'shield shield-check shield-alert key password fingerprint scan verified security-warning danger privacy safe'.split(),
    'Status': 'check check-circle close close-circle info question alert success pending error offline online status-dot'.split(),
    'Time': 'calendar-add calendar-check calendar-close stopwatch timer hourglass schedule sun moon sunrise sunset timezone'.split(),
}

DISPLAY_OVERRIDES = {
    'at-sign': 'At sign', 'credit-card': 'Credit card', 'file-text': 'File text',
    'hard-drive': 'Hard drive', 'map-pin': 'Map pin', 'nav-menu': 'Navigation menu',
    'user-plus': 'User plus', 'user-minus': 'User minus', 'user-check': 'User check',
    'user-x': 'User remove', 'video-call': 'Video call', 'skip-next': 'Skip next',
    'skip-prev': 'Skip previous', 'trend-up': 'Trend up', 'trend-down': 'Trend down',
    'calendar-add': 'Calendar add', 'calendar-check': 'Calendar check',
    'calendar-close': 'Calendar close', 'security-warning': 'Security warning',
    'status-dot': 'Status dot',
}

SYNONYMS = {
    'add': ['create', 'new', 'plus'], 'remove': ['subtract', 'minus'], 'edit': ['write', 'pencil'],
    'delete': ['trash', 'discard'], 'refresh': ['reload', 'sync'], 'copy': ['duplicate'],
    'mail': ['email', 'envelope'], 'message': ['chat', 'conversation'], 'cart': ['basket', 'shopping'],
    'file': ['document'], 'folder': ['directory'], 'image': ['photo', 'picture'],
    'search': ['find', 'magnify'], 'settings': ['preferences', 'gear'], 'map-pin': ['location', 'marker'],
    'user': ['account', 'person'], 'shield': ['protection', 'security'], 'check': ['confirm', 'done'],
    'close': ['cancel', 'dismiss'], 'clock': ['time'], 'calendar': ['date', 'schedule'],
}


def line(x1, y1, x2, y2):
    return f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}"/>'


def rect(x, y, width, height, radius=0):
    radius_attr = f' rx="{radius:g}"' if radius else ''
    return f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}"{radius_attr}/>'


def circle(cx, cy, radius):
    return f'<circle cx="{cx:g}" cy="{cy:g}" r="{radius:g}"/>'


def path(d):
    return f'<path d="{d}"/>'


def polygon(points):
    return f'<path d="M{points[0][0]:g} {points[0][1]:g}' + ''.join(
        f'L{x:g} {y:g}' for x, y in points[1:]
    ) + 'Z"/>'


def motif(kind):
    if kind == 'search':
        return circle(10.5, 10.5, 5.5) + line(14.5, 14.5, 20, 20)
    if kind == 'plus':
        return line(12, 5, 12, 19) + line(5, 12, 19, 12)
    if kind == 'minus':
        return line(5, 12, 19, 12)
    if kind == 'check':
        return path('M4 12.5L9.2 17.5L20 6.5')
    if kind == 'close':
        return line(6, 6, 18, 18) + line(18, 6, 6, 18)
    if kind == 'arrow-up':
        return line(12, 19, 12, 5) + path('M6 11L12 5L18 11')
    if kind == 'arrow-down':
        return line(12, 5, 12, 19) + path('M6 13L12 19L18 13')
    if kind == 'arrow-left':
        return line(19, 12, 5, 12) + path('M11 6L5 12L11 18')
    if kind == 'arrow-right':
        return line(5, 12, 19, 12) + path('M13 6L19 12L13 18')
    if kind == 'chevron-up':
        return path('M5 15L12 8L19 15')
    if kind == 'chevron-down':
        return path('M5 9L12 16L19 9')
    if kind == 'chevron-left':
        return path('M15 5L8 12L15 19')
    if kind == 'chevron-right':
        return path('M9 5L16 12L9 19')
    if kind == 'heart':
        return path('M12 20.5S4 15.8 4 9.5C4 6.7 5.8 5 8.2 5C10 5 11.2 6 12 7.4C12.8 6 14 5 15.8 5C18.2 5 20 6.7 20 9.5C20 15.8 12 20.5 12 20.5Z')
    if kind == 'star':
        return path('M12 3L14.8 8.7L21 9.6L16.5 14L17.6 20.2L12 17.3L6.4 20.2L7.5 14L3 9.6L9.2 8.7Z')
    if kind == 'bell':
        return path('M6 17H18L16.5 14V10C16.5 7.5 14.6 5.5 12 5.5C9.4 5.5 7.5 7.5 7.5 10V14Z') + path('M10 20H14')
    if kind == 'calendar':
        return rect(4, 5.5, 16, 14, 2) + line(4, 9.5, 20, 9.5) + line(8, 3.5, 8, 7.5) + line(16, 3.5, 16, 7.5) + circle(8, 13.5, .7) + circle(12, 13.5, .7) + circle(16, 13.5, .7)
    if kind == 'mail':
        return rect(3.5, 5.5, 17, 13, 2) + path('M4 7L12 13L20 7')
    if kind == 'chat':
        return path('M4 5.5H20V16H10L6 19V16H4Z') + line(8, 9.5, 16, 9.5) + line(8, 12.5, 13, 12.5)
    if kind == 'phone':
        return path('M7 4L10 7L8 9C9.4 12.1 11.9 14.6 15 16L17 14L20 17L18 20C10.7 19.4 4.6 13.3 4 6Z')
    if kind == 'user':
        return circle(12, 8, 3.5) + path('M5 20C5.5 15.9 8.1 13.5 12 13.5C15.9 13.5 18.5 15.9 19 20Z')
    if kind == 'users':
        return circle(9, 8, 3) + circle(16.5, 9, 2.5) + path('M3.5 20C4 16.2 6 14 9 14C12 14 14 16.2 14.5 20Z') + path('M14 14.5C17.2 14.1 19.7 16 20.5 19.5')
    if kind == 'home':
        return path('M3.5 11.5L12 4L20.5 11.5V20H14.5V14H9.5V20H3.5Z')
    if kind == 'settings':
        return circle(12, 12, 3) + path('M19 13.5L20.2 15L18 18L16.2 17.2L14.5 18L14.2 20H9.8L9.5 18L7.8 17.2L6 18L3.8 15L5 13.5L4.8 11.5L3.5 10L5.7 6.8L7.5 7.6L9.2 7L9.8 4H14.2L14.8 7L16.5 7.6L18.3 6.8L20.5 10L19.2 11.5Z')
    if kind == 'lock':
        return rect(5, 10, 14, 10, 2) + path('M8 10V7.5C8 5.3 9.8 3.5 12 3.5C14.2 3.5 16 5.3 16 7.5V10') + line(12, 14, 12, 17)
    if kind == 'folder':
        return path('M3.5 7H9L11 9H20.5V19.5H3.5Z')
    if kind == 'file':
        return path('M6 3.5H14L18.5 8V20.5H6Z') + path('M14 3.5V8H18.5')
    if kind == 'image':
        return rect(3.5, 4.5, 17, 15, 2) + circle(8.5, 9, 1.5) + path('M4.5 17L9.5 12L13 15L15.5 12.5L19.5 17')
    if kind == 'play':
        return polygon([(8, 5), (19, 12), (8, 19)])
    if kind == 'pause':
        return rect(6, 5, 4, 14, 1) + rect(14, 5, 4, 14, 1)
    if kind == 'camera':
        return rect(3.5, 7, 17, 12, 2) + path('M8 7L9.5 4.5H14.5L16 7') + circle(12, 13, 3.5)
    if kind == 'map-pin':
        return path('M12 21S5 14.5 5 9.5C5 5.9 8.1 3 12 3C15.9 3 19 5.9 19 9.5C19 14.5 12 21 12 21Z') + circle(12, 9.5, 2)
    if kind == 'globe':
        return circle(12, 12, 8.5) + path('M3.5 12H20.5') + path('M12 3.5C14.2 5.8 15.2 8.6 15.2 12C15.2 15.4 14.2 18.2 12 20.5C9.8 18.2 8.8 15.4 8.8 12C8.8 8.6 9.8 5.8 12 3.5Z')
    if kind == 'clock':
        return circle(12, 12, 8.5) + line(12, 7, 12, 12) + line(12, 12, 16, 14)
    if kind == 'cart':
        return path('M4 5H6L8 15H18L20 8H7') + circle(9.5, 19, 1.3) + circle(17, 19, 1.3)
    if kind == 'tag':
        return path('M4 5H13L20 12L12 20L4 12Z') + circle(8.5, 8.5, 1.2)
    if kind == 'download':
        return line(12, 4, 12, 15) + path('M7 11L12 16L17 11') + path('M5 20H19')
    if kind == 'upload':
        return line(12, 20, 12, 9) + path('M7 13L12 8L17 13') + path('M5 4H19')
    if kind == 'cloud':
        return path('M7.5 18.5H18C20.2 18.5 21.5 17.1 21.5 15.2C21.5 13.4 20.2 12 18.4 11.8C18 8.4 15.4 6 12 6C8.9 6 6.4 8.1 5.8 11.1C3.6 11.3 2.5 12.8 2.5 14.8C2.5 17 4.2 18.5 7.5 18.5Z')
    if kind == 'filter':
        return path('M4 5H20L14 12V19L10 17V12Z')
    if kind == 'eye':
        return path('M2.5 12S6.5 5.5 12 5.5S21.5 12 21.5 12S17.5 18.5 12 18.5S2.5 12 2.5 12Z') + circle(12, 12, 2.5)
    if kind == 'shield':
        return path('M12 3L19 6V11.5C19 16 16.2 19.2 12 21C7.8 19.2 5 16 5 11.5V6Z')
    if kind == 'key':
        return circle(8, 15.5, 3.5) + line(10.5, 13, 20, 3.5) + line(16, 7.5, 18, 9.5) + line(13.5, 10, 15.5, 12)
    if kind == 'info':
        return circle(12, 12, 8.5) + line(12, 10.5, 12, 16.5) + circle(12, 7.5, .7)
    if kind == 'warning':
        return path('M12 3.5L21 20H3Z') + line(12, 9, 12, 14) + circle(12, 17, .7)
    if kind == 'sun':
        return circle(12, 12, 3.5) + line(12, 2.5, 12, 5) + line(12, 19, 12, 21.5) + line(2.5, 12, 5, 12) + line(19, 12, 21.5, 12) + line(5.3, 5.3, 7, 7) + line(17, 17, 18.7, 18.7) + line(18.7, 5.3, 17, 7) + line(7, 17, 5.3, 18.7)
    if kind == 'moon':
        return path('M19.5 15.5C18.2 16.1 16.8 16.5 15.3 16.5C10.5 16.5 7 13 7 8.3C7 6.8 7.4 5.3 8 4C4.7 5.5 2.5 8.8 2.5 12.5C2.5 17.5 6.5 21.5 11.5 21.5C15.2 21.5 18.5 19.3 20 16Z')
    return None


def generic_motif(slug):
    digest = hashlib.sha1(slug.encode()).digest()
    mode = digest[0] % 5
    offset = digest[1] % 3
    if mode == 0:
        return rect(4, 4, 16, 16, 4) + circle(12, 12, 3 + offset) + line(7, 17, 17, 7)
    if mode == 1:
        return circle(12, 12, 8) + rect(8, 8, 8, 8, 2) + line(5, 12, 7, 12) + line(17, 12, 19, 12)
    if mode == 2:
        return polygon([(12, 3), (20, 12), (12, 21), (4, 12)]) + circle(12, 12, 2 + offset)
    if mode == 3:
        return rect(4, 6, 16, 12, 6) + line(7, 12, 17, 12) + line(8, 9, 8, 9) + line(12, 9, 12, 9) + line(16, 9, 16, 9)
    return rect(5, 4, 14, 16, 2) + line(8, 9, 16, 9) + line(8, 12, 16, 12) + line(8, 15, 13 + offset, 15)


EXACT_MOTIFS = {
    'add': 'plus', 'remove': 'minus', 'check': 'check', 'close': 'close',
    'close-circle': 'close', 'arrow-up': 'arrow-up', 'arrow-down': 'arrow-down',
    'arrow-left': 'arrow-left', 'arrow-right': 'arrow-right',
    'chevron-up': 'chevron-up', 'chevron-down': 'chevron-down',
    'chevron-left': 'chevron-left', 'chevron-right': 'chevron-right',
    'mail': 'mail', 'chat': 'chat', 'message': 'chat', 'phone': 'phone',
    'bell': 'bell', 'user': 'user', 'users': 'users', 'home': 'home',
    'settings': 'settings', 'lock': 'lock', 'folder': 'folder', 'file': 'file',
    'file-text': 'file', 'image': 'image', 'play': 'play', 'pause': 'pause',
    'camera': 'camera', 'map-pin': 'map-pin', 'globe': 'globe', 'clock': 'clock',
    'cart': 'cart', 'tag': 'tag', 'download': 'download', 'upload': 'upload',
    'cloud': 'cloud', 'search': 'search', 'filter': 'filter', 'eye': 'eye',
    'shield': 'shield', 'key': 'key', 'info': 'info', 'warning': 'warning',
    'alert': 'warning', 'sun': 'sun', 'moon': 'moon',
}


def display_name(slug):
    return DISPLAY_OVERRIDES.get(slug, slug.replace('-', ' ').title())


def svg_parts(slug, index):
    kind = EXACT_MOTIFS.get(slug)
    parts = motif(kind) if kind else None
    if parts is None:
        parts = generic_motif(f'{slug}-{index}')
    return {'outline': parts, 'filled': parts}


def icon_svg(parts, variant):
    style = (
        'fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"'
        if variant == 'outline' else
        'fill="currentColor" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"'
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" aria-hidden="true"><g {style}>{parts}</g></svg>\n'


def all_icon_specs():
    return [(category, slug) for category in CATEGORIES for slug in ICON_NAMES[category]]


def make_records(version):
    specs = all_icon_specs()
    slugs = [slug for _, slug in specs]
    records = []
    for index, (category, slug) in enumerate(specs):
        aliases = SYNONYMS.get(slug, [])
        keywords = sorted(set([slug.replace('-', ' '), category.lower(), *aliases]))
        related = [candidate for candidate in slugs[index + 1:] if candidate != slug][:3]
        if len(related) < 3:
            related.extend(candidate for candidate in slugs if candidate != slug and candidate not in related)
        records.append({
            'pack': 'soft',
            'slug': slug,
            'name': display_name(slug),
            'category': category,
            'aliases': aliases,
            'keywords': keywords,
            'outlineAsset': f'/icons/soft/{slug}/outline.svg',
            'filledAsset': f'/icons/soft/{slug}/filled.svg',
            'related': related[:3],
            'contextExamples': ['sidebar', 'buttons', 'metric', 'notification', 'input', 'tabs'],
            'introducedIn': version,
            '_parts': svg_parts(slug, index),
        })
    return records


def write_pack(records, version):
    asset_root = ROOT / 'public' / 'icons' / 'soft'
    if asset_root.exists():
        shutil.rmtree(asset_root)
    asset_root.mkdir(parents=True)

    for record in records:
        target = asset_root / record['slug']
        target.mkdir()
        for variant in ('outline', 'filled'):
            (target / f'{variant}.svg').write_text(icon_svg(record['_parts'][variant], variant))

    public_records = [{key: value for key, value in record.items() if key != '_parts'} for record in records]
    manifest = {
        'version': version,
        'license': 'MIT',
        'packs': [{
            'id': 'soft',
            'name': 'Soft',
            'version': version,
            'description': 'A soft-rounded UI icon pack for web and product interfaces.',
            'iconCount': len(public_records),
        }],
        'icons': public_records,
    }
    catalog_path = ROOT / 'src' / 'icons' / 'catalog.json'
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pack', choices=('soft',), default='soft')
    parser.add_argument('--version', default='1.0.0')
    args = parser.parse_args()
    records = make_records(args.version)
    manifest = write_pack(records, args.version)
    print(f"Generated Asbir Icons {args.pack.title()} {args.version}: {len(manifest['icons'])} icons, {len(manifest['icons']) * 2} SVG variants")


if __name__ == '__main__':
    main()
