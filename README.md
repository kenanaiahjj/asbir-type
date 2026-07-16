# Asbir Type Studio

Local type-production workspace for the Asbir Sans and Asbir Mono families. The
browser studio provides editable proofs, language samples, OpenType checks, and
download links. Asbir Serif remains paused.

## Run

```sh
python3 -m pip install -r requirements.txt
npm install
npm run dev
```

## Build and package

Roman and true italic families are compiled from editable UFO/designspace
sources. Italics are separate masters and variable files, not a CSS or outline
skew of the Roman family.

```sh
python3 tools/build_fonts.py --family sans --family mono --italic
python3 tools/build_mono_nerd_font.py
python3 tools/package_webfonts.py
python3 tools/package_asbir_sans_release.py
python3 tools/package_asbir_mono_release.py
```

The outputs include nine static TTF and CFF OTF weights plus separate Roman and
italic variable TTFs. Sans exposes `opsz` 14–32 and `wght` 100–900; Mono exposes
`wght` 100–900 and keeps its 600-unit cell. Web kits live in
`public/downloads/web/AsbirSans/` and `public/downloads/web/AsbirMono/`, with
normal and italic WOFF2 faces plus CSS loading files.

Production archives:

- `public/downloads/AsbirSans-1.0.0.zip`
- `public/downloads/AsbirMono-1.0.0.zip`

The Mono archive also includes the separately named Nerd Font / Powerline
terminal companion in `Terminal/`.

## Editable sources

- `sources/asbir-sans/AsbirSans.designspace` — Roman Sans, six Text/Display masters.
- `sources/asbir-sans-italic/AsbirSansItalic.designspace` — true Sans Italic masters.
- `sources/asbir-mono/AsbirMono.designspace` — Roman Mono masters.
- `sources/asbir-mono-italic/AsbirMonoItalic.designspace` — true Mono Italic masters.

## Verification

```sh
python3 -m unittest discover -s tests -v
python3 tools/source_qa.py --family sans --family mono
python3 tools/font_qa.py --mode review --family sans --family mono
python3 tools/font_qa.py --mode production --family sans --family mono
python3 tools/shaping_qa.py --family sans --family mono
python3 tools/run_fontbakery.py --family sans --family mono
npm run build
```

Family-scoped approval records live in `reports/production-signoff.json` and
`reports/mono-production-signoff.json`. The proof artifacts retain `Review`
filenames; the production archives contain clean release names.

Both families are OFL-compliant derivatives. See
`THIRD_PARTY_NOTICES.md` and `FONTBAKERY_WAIVERS.md` for attribution and QA
notes.
