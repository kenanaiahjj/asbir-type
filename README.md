# Asbir Sans Studio

A local type-production workspace centered on **Asbir Sans**: an OFL-compliant,
high-x-height geometric grotesk derived from Inter 4.001, with an authored Asbir
character system. The browser app provides a live editable proof and
Inter/Geist comparison. Asbir Sans is the approved production release; Asbir
Mono is an active review build for coding and data use. Serif remains paused.

## Run

```sh
python3 -m pip install -r requirements.txt
npm install
npm run dev
```

`python3 tools/build_fonts.py --family sans` generates the current Sans review
artifacts before the web app is bundled:

- `*-Review-{Thin,ExtraLight,Light,Regular,Medium,SemiBold,Bold,ExtraBold,Black}.ttf`
- `*-Review-{Thin,ExtraLight,Light,Regular,Medium,SemiBold,Bold,ExtraBold,Black}.otf` (CFF)
- `*-Review-VF.ttf` (a true `wght` variable TTF)

## Editable Sans source

The source of truth is `sources/asbir-sans/AsbirSans.designspace`, with six
UFO masters (Text/Display at Thin, Regular, and Black) for further drawing in
Glyphs, RoboFont, FontLab, or another UFO-compatible editor. It builds a true
two-axis variable TTF: `opsz` 14–32 and `wght` 100–900, plus the nine static
weights in TTF and CFF OTF.

The proof artifacts retain **Review** filenames so the local studio stays
isolated from the distributable files. The approved production package lives
in `release/AsbirSans-1.0.0/`. It includes practical modern Latin, Greek, Cyrillic, and Vietnamese
coverage, kerning, figure systems (`pnum`, `tnum`, `zero`), and numerator,
denominator, superior, inferior, and ordinal features. See
[FONT_AUDIT.md](FONT_AUDIT.md) for evidence and release blockers.

## Font QA

Use these Sans-only gates while Sans is active:

```sh
python3 tools/source_qa.py --family sans
python3 tools/build_fonts.py --family sans
python3 tools/font_qa.py --mode review --family sans
python3 tools/shaping_qa.py --family sans
python3 tools/run_fontbakery.py --family sans
```

The approved human signoff is recorded in `reports/production-signoff.json`.
Automated review success is release evidence, not a claim of typeface-quality
parity with an established family's full design and maintenance program.

## Asbir Mono review build

Asbir Mono is a Geist Mono-derived coding/data review build with a two-storey
`a`, slashed zero, fixed 600-unit cell, default ligatures for common coding
operators, and Unicode `⇐ ⇒ ⇔`. Build and verify it with:

```sh
python3 tools/build_fonts.py --family mono
python3 tools/build_mono_nerd_font.py
python3 tools/source_qa.py --family mono
python3 tools/font_qa.py --mode review --family mono
python3 tools/shaping_qa.py --family mono
python3 tools/run_fontbakery.py --family mono
```

`AsbirMono-NerdFont-Review-Regular.ttf` is a separately named Regular TTF for
terminal use. It adds Nerd Fonts/Powerline symbols without bloating the core
Mono variable or static fonts. See `THIRD_PARTY_NOTICES.md` for attribution.
