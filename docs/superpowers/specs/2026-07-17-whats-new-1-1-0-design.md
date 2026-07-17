# Asbir Type Studio — “What’s New” 1.1.0 Release Panel

## Goal

Make the Asbir Sans and Asbir Mono 1.1.0 release additions discoverable from the specimen website without interrupting the type-testing workflow.

## Experience

- On the first visit after the 1.1.0 release, a compact fixed panel opens automatically in the lower-right corner.
- The panel title is `What’s new · 1.1.0`.
- A small floating trigger remains available after dismissal so the announcement can be reopened.
- Closing the panel stores a versioned browser key. A future release can use a new key and open automatically again.
- The panel does not lock scrolling, dim the page, or behave as a full-screen modal.
- Escape and the close button dismiss the panel. The trigger reopens it.

## Release content

The panel contains two concise update groups:

### Asbir Sans

- True italic family with Roman and italic static weights.
- Separate Roman and italic variable fonts.
- WOFF2 files and a CSS loading kit for web use.
- Versioned 1.1.0 download link.

### Asbir Mono

- Approved production family.
- True italic family with Roman and italic static weights.
- Fixed-cell terminal companion with Nerd Font / Powerline symbols.
- WOFF2 files and a CSS loading kit for web use.
- Versioned 1.1.0 download link.

## Implementation shape

- Render the panel and trigger inside the existing `render()` output so family switching and the current UI lifecycle remain unchanged.
- Keep release-panel state separate from specimen state: `open` is transient UI state; the dismissed version is persisted in `localStorage`.
- Use a versioned key such as `asbir-whats-new-1.1.0-dismissed`.
- Bind the trigger, close button, and Escape listener through the existing `bind()` lifecycle.
- Link directly to `/downloads/AsbirSans-1.1.0.zip` and `/downloads/AsbirMono-1.1.0.zip`.

## Visual direction

- Use the existing black/paper surface, line, muted text, and accent tokens.
- Keep the panel compact and editorial: a ruled header, short release summary, two stacked family rows, and a quiet close action.
- Use the website’s existing Sans/Mono family treatment rather than introducing a new component style.
- Place the trigger above page content with a semantic z-index below the sticky header and above specimen sections.
- On narrow screens, the panel becomes a bottom inset sheet with safe horizontal padding and a full-width trigger row.

## Accessibility and motion

- Use a labelled `aside` or non-modal dialog pattern; do not set `aria-modal="true"`.
- Give the trigger an explicit accessible name and `aria-expanded` state.
- Keep visible focus styles for the trigger and close control.
- Escape closes the panel without trapping focus or changing scroll position.
- Respect `prefers-reduced-motion: reduce` by disabling panel/trigger transitions.
- Maintain WCAG AA contrast for all copy and controls.

## Validation

- Add a lightweight contract test for the 1.1.0 copy, download URLs, versioned storage key, and both family update groups.
- Run the existing Python test suite and `npx vite build`.
- Verify the panel opens automatically with an empty storage key, stays dismissed after closing, and reopens from the floating trigger.
- Check desktop and narrow viewport layout, keyboard Escape behavior, and reduced-motion CSS.
