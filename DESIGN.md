# Retail Demand Intelligence Design Mapping

## 1. Relationship to the canonical portfolio design

This analytical application adapts `sebastiangaray.github.io/DESIGN.md`, which remains the canonical visual source. The mapping preserves family identity within stable Streamlit theming and intentionally does not reproduce Astro markup.

## 2. Shared visual invariants

Warm neutral canvas and surfaces, slate accent, Source Serif 4 headings, Inter body copy, JetBrains Mono values, filled primary and bordered secondary actions, two-pixel focus, one-pixel borders, four-pixel radii, restrained shadows, evidence-led copy and a visible Portfolio return link are required.

## 3. Exact palette mapping

| Role | Canonical Light | Local implementation | Mapping |
|---|---:|---|---|
| Background | `#fdf8f8` | Streamlit `backgroundColor`, `--rdi-background` | Exact |
| Surface | `#ffffff` | `secondaryBackgroundColor`, `--rdi-surface` | Exact |
| Subtle surface | `#f7f3f2` | `--rdi-surface-subtle` | Exact |
| Elevated surface | `#ebe7e6` | `--rdi-surface-elevated`, code background | Exact |
| Text | `#1c1b1b` | `textColor`, `--rdi-text` | Exact |
| Muted text | `#515f74` | `--rdi-secondary` | Exact |
| Border | `#c4c7c7` | Streamlit border settings, `--rdi-border` | Exact |
| Strong border | `#8d9292` | `--rdi-border-strong` | Exact |
| Accent | `#334155` | `primaryColor`, links, `--rdi-primary` | Exact |
| Accent hover | `#475569` | `--rdi-primary-hover` | Exact |
| Accent active | No standalone canonical token | black primary fill or shared accent selected rule | Adapted from canonical action/selected patterns |
| Accent contrast | `#f8fafc` | filled-action labels | Exact |
| Focus | `#64748b` | `--rdi-focus` | Exact |
| Success | `#2f6b4f` | `greenColor`, `--rdi-success` | Exact |
| Warning | `#8a5b16` | `orangeColor`, `--rdi-warning` | Exact |
| Danger | Not defined | `#ba1a1a` | Adapted for critical inventory and error semantics |
| Info | Not defined | `#334155` | Adapted; informational emphasis uses shared accent |

Dark canonical equivalents are `#1b1918` background, `#292624` surface, `#23201f` subtle, `#312d2a` elevated, `#f1ece7` text, `#aaa098` muted, `#48423e` border, `#6a615b` strong border, `#d8cec5` accent, `#eee6df` hover, `#c5a98f` focus, `#79aa8d` success and `#d5ad6c` warning. They are documented for parity but not injected over Streamlit's own runtime theme selection.

## 4. Theme mapping

The deployed app declares the canonical Light theme through `.streamlit/config.toml`. Streamlit owns its settings-menu theme behavior and does not expose the portfolio's stable three-state control API to application code. Forced CSS dark emulation is prohibited because it would leave native widgets and charts inconsistent. Dark values above are the required mapping if Streamlit adds a maintainable app-level theme API.

## 5. Typography mapping

Streamlit configuration loads Inter for interface copy, Source Serif 4 at weights 600/700 for headings and JetBrains Mono for code and numeric values. CSS reinforces the display family on headings. Platform fallbacks remain sans-serif, Georgia/serif and monospace.

## 6. Button and link mapping

Primary actions use the canonical black fill, white label, four-pixel radius and 600 weight; hover uses `#475569`. Secondary and download actions are transparent with canonical borders and elevated-surface hover. Sidebar navigation retains Streamlit buttons: selected items use an elevated surface, accent text and a three-pixel accent edge for operational wayfinding. Text and external links use the shared accent and `0.22em` underline offset. Focus is `2px solid #64748b` with `4px` offset. Disabled behavior remains native Streamlit.

## 7. Border, radius and shadow mapping

Panels, KPI cards, dataframes and controls use one-pixel canonical borders and four-pixel radii. Selected risk/navigation edges may use three or four pixels because they encode status. Shadows remain limited to Streamlit-owned floating layers.

## 8. Spacing mapping

The operational canvas remains fluid up to 1600px with `1.75rem` desktop and `1rem` narrow gutters. Local groups use a compact 8px-oriented rhythm, 44px controls and `0.65–1.5rem` panel spacing. This is denser than the portfolio by design.

## 9. Navigation and attribution

The expanded Streamlit sidebar owns five task pages, bilingual selection and a full-width external Portfolio link to `https://sebastiangaray.github.io/`. The About page retains repository, documentation and license links.

## 10. Local component patterns

Metric strips and KPI cards prioritize comparable values; selected or risk cards use an accent edge. Forecast and model charts sit in bordered containers. Inventory rows combine status text, numerical values and semantic edge colors. Empty, loading and error states use native Streamlit feedback, concise explanations and recovery commands where applicable.

## 11. Domain-specific identity

The application remains analytical, calm and operational through dense metric groups, persistent task navigation, chart-first sections, coverage thresholds, inventory-risk summaries and decision-support wording.

## 12. Domain-specific semantic colors

Actual demand uses `#1c1b1b`; forecast/champion uses `#334155`; comparison neutrals use `#c4c7c7` and `#8d9292`. Healthy is `#2f6b4f`, watch is `#8a5b16`, elevated/excess is `#0e7490`, and critical is `#ba1a1a`. Uncertainty uses lower-opacity accent or restrained gray when charts require it. Every risk state also has a text label.

## 13. Responsive behavior

Streamlit provides the collapsible sidebar. Below 780px the main gutter contracts, titles reduce, metric grids become two columns, About grids stack and the architecture flow becomes vertical. Spanish labels wrap rather than being clipped.

## 14. Accessibility

Controls retain visible labels and at least 44px height. Focus uses the canonical outline. Risk meaning is communicated with text and color. Charts have adjacent context and data-table alternatives. Loading and error feedback is scoped to the affected workspace; raw traces are not exposed.

## 15. Localization

English and Spanish use identical translation-key sets and preserve the same information architecture. The Portfolio label is localized directly in the sidebar because the destination is application chrome rather than domain content.

## 16. Writing style

Copy is concise, operational and explicit about temporal validation, saved artifacts, synthetic data and limitations. It avoids replenishment prescriptions, live-data implications and unsupported production claims.

## 17. Allowed deviations

Higher density, wider canvases, compact metric typography, persistent sidebar navigation, native Streamlit widgets, chart-specific colors and risk edges are allowed when they preserve the shared foundation and accessibility.

## 18. Prohibited deviations

Do not replace the slate accent with a separate brand hue, restore blue-gray canvases, introduce large radii or decorative shadows, emulate only part of a dark theme, restyle generated hash classes, hide attribution, change forecast/model results for presentation or add controls without behavior.

## 19. Implementation notes for Streamlit

Stable theme properties live in `.streamlit/config.toml`. Reusable CSS is injected once by `dashboard/styles.py` and targets stable `data-testid`, `kind` and application-owned class hooks rather than generated hashes. Altair palettes are declared in `dashboard/pages.py`. Page configuration and navigation remain in `dashboard/app.py`.

## 20. Final-code confirmation

This document matches the final Streamlit configuration, CSS tokens, chart colors, typography, actions, navigation, responsive behavior and Portfolio attribution implemented in this repository.
