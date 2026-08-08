---
name: Retail Intelligence System
colors:
  surface: '#f9f9fa'
  surface-dim: '#dadadb'
  surface-bright: '#f9f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f5'
  surface-container: '#eeeeef'
  surface-container-high: '#e8e8e9'
  surface-container-highest: '#e2e2e4'
  on-surface: '#1a1c1d'
  on-surface-variant: '#41484c'
  inverse-surface: '#2f3132'
  inverse-on-surface: '#f1f0f2'
  outline: '#72787c'
  outline-variant: '#c1c7cc'
  surface-tint: '#3f6376'
  primary: '#001d29'
  on-primary: '#ffffff'
  primary-container: '#083344'
  on-primary-container: '#779cb0'
  inverse-primary: '#a7cce1'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#2b1600'
  on-tertiary: '#ffffff'
  tertiary-container: '#452907'
  on-tertiary-container: '#b98f64'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c2e8fe'
  primary-fixed-dim: '#a7cce1'
  on-primary-fixed: '#001e2b'
  on-primary-fixed-variant: '#264b5d'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#ffdcbd'
  tertiary-fixed-dim: '#edbe90'
  on-tertiary-fixed: '#2c1600'
  on-tertiary-fixed-variant: '#60401c'
  background: '#f9f9fa'
  on-background: '#1a1c1d'
  surface-variant: '#e2e2e4'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  sidebar_width: 260px
  container_max_width: 1440px
  gutter: 24px
  cell_padding_x: 12px
  cell_padding_y: 8px
---

## Brand & Style

The design system is engineered for high-density retail analytics and demand forecasting. The brand personality is authoritative, precise, and objective, designed to instill confidence in data-driven decision-making.

The aesthetic follows a **Modern Corporate** approach with a focus on **Functional Minimalism**. It prioritizes information density and legibility over decorative elements. The visual language is defined by structured data grids, wide-format visualizations, and a restrained color palette that allows semantic status indicators (risks, warnings, opportunities) to command attention.

To support bilingual requirements (English/Spanish), the interface utilizes flexible container widths and generous horizontal padding to accommodate the increased character count typical of Spanish translations without breaking the layout or causing premature truncation.

## Colors

The palette is anchored by a deep petroleum blue primary color, used for core navigation and primary actions to establish a professional, "executive" tone.

- **Primary:** Petroleum blue is the dominant brand color, used for high-level UI landmarks.
- **Backgrounds:** A cool light gray provides a soft, low-glare canvas for extended data review.
- **Surfaces:** Pure white is reserved for cards, tables, and modal containers to create clear separation from the background.
- **Semantic Palette:** Red, Amber, and Green are used strictly for status signaling. These are calibrated for high legibility against white surfaces, ensuring that "Risk" and "Favorable" metrics are immediately identifiable during rapid scanning.

## Typography

This design system uses a dual-font strategy to balance character and utility. **Hanken Grotesk** is used for headlines to provide a sharp, contemporary professional feel. **Inter** is the workhorse for body text and interface labels, chosen for its exceptional legibility in data-heavy environments and its neutral tone.

For bilingual support, line heights are kept slightly generous to prevent "clipping" of descenders in Spanish text. For numerical data within tables and reports, a monospaced font (JetBrains Mono) is utilized at a smaller scale to ensure vertical alignment of digits, facilitating easier comparison of values.

## Layout & Spacing

The layout utilizes a **Fixed Sidebar** and a **Fluid Content Area** model. The sidebar remains at a constant 260px to provide stable navigation, while the main content area expands to accommodate wide charts and multi-column data tables.

- **Grid:** Built on an 8px base unit. All margins and paddings must be multiples of 8 (8, 16, 24, 32, etc.).
- **Tables:** Optimized for density. Compact vertical padding (8px) allows more rows to be visible above the fold, while horizontal padding (12px) prevents text crowding.
- **Charts:** Visualizations should span a minimum of 6 columns in a standard 12-column logic to ensure trend lines and data points are not compressed.
- **Bilingual Flexibility:** Avoid fixed-width labels. Layout containers should use `min-width` or flexbox with `flex-wrap` to ensure that longer Spanish phrases do not overflow their parent containers.

## Elevation & Depth

To maintain a clean, analytical look, this design system avoids heavy shadows.

- **Tonal Separation:** Depth is primarily established through color contrast between the `#F9FAFB` background and `#FFFFFF` surfaces.
- **Borders:** Low-contrast outlines (`#E5E7EB`) are used to define card boundaries and table cells.
- **Shadows:** A single, very subtle "System Shadow" is used only for floating elements like dropdown menus or active modals (e.g., `0px 4px 6px -1px rgba(0, 0, 0, 0.05)`).
- **Interactive State:** Hover states are indicated by a subtle background color shift (e.g., White to Gray 50) rather than a change in elevation.

## Shapes

The design system uses a **Soft** shape language. A standard radius of 4px (`0.25rem`) is applied to buttons, input fields, and cards. This small radius maintains the professional "grid-like" feel of the application while removing the harshness of 0px corners, making the interface feel modern and approachable.

Large containers like main dashboard cards should use the `rounded-lg` (8px) setting to create a softer visual hierarchy for major content sections.

## Components

- **Buttons:** Primary buttons use the deep petroleum blue with white text. Ghost buttons use an outline of the primary color for secondary actions.
- **Data Tables:** Headers must be sticky. Rows should feature a subtle hover state (`#F3F4F6`). Status indicators within tables (Risk/Warning/Favorable) should use small colored dots or high-contrast pill badges.
- **Chips/Badges:** Used for filtering and status. Badges use a light background version of the semantic colors with dark text for maximum readability (e.g., light red background with dark red text for "Risk").
- **Input Fields:** Clean 1px borders with a 4px border-radius. On focus, the border transitions to the petroleum blue primary color. Labels must be placed above the field to accommodate varying text lengths in different languages.
- **Cards:** White background, 1px light gray border, 8px rounded corners. Cards are the primary container for dashboard widgets and chart groupings.
- **Sidebar Nav:** High contrast (Primary color background or white background with primary color active states). Navigation items must support icons to assist in rapid identification.
