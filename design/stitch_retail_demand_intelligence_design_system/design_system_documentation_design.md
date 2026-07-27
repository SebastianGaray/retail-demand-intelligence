# Design System: Retail Demand Intelligence

## Visual Identity
A professional, sober, and analysis-oriented interface for exploring retail demand forecasts and inventory risk.

## Design Tokens

### Colors
- **Background**: `#F9FAFB` (Light Gray/Warm)
- **Surface**: `#FFFFFF` (White)
- **Primary (Petroleum Blue)**: `#083344` (Deep Teal)
- **Primary Muted**: `#0E7490`
- **Text Primary**: `#111827`
- **Text Secondary**: `#4B5563`
- **Border**: `#E5E7EB`
- **Risk (Red)**: `#DC2626`
- **Warning (Amber)**: `#D97706`
- **Success (Green)**: `#059669`
- **Chart Accent 1**: `#083344` (Actuals)
- **Chart Accent 2**: `#0E7490` (Forecasts)
- **Chart Highlight**: `#CFFAFE`

### Typography
- **Font Family**: Sans-serif (Inter, Roboto, or System Sans)
- **Scale**:
  - H1: 24px / 32px (Bold)
  - H2: 20px / 28px (Semibold)
  - H3: 16px / 24px (Semibold)
  - Body: 14px / 20px (Regular)
  - Small/Caption: 12px / 16px (Medium)

### Spacing & Layout
- **Base Grid**: 8px
- **Sidebar Width**: 260px
- **Max Content Width**: 1440px
- **Border Radius**: 6px
- **Touch Targets**: Min 44px
- **Density**: High (Compact tables and charts)

### Components
- **Sidebar**: Fixed on desktop, drawer on mobile.
- **Metric Strip**: Horizontal band for top-level stats.
- **Filter Bar**: Consistent layout for store/product selectors.
- **Data Tables**: Compact, sortable, no heavy borders.
- **Charts**: Large areas for data visualization with clear legends and tooltips.

## Localization Strategy
- **Bilingual Support**: English (EN) and Spanish (ES).
- **Expansion Logic**: Components must accommodate longer Spanish strings without truncation.
- **Keys**: 
  - `navigation.overview`: "Overview" / "Resumen"
  - `navigation.forecast`: "Forecast Explorer" / "Explorador de Pronósticos"
  - `navigation.inventory`: "Inventory Risk" / "Riesgo de Inventario"
  - `navigation.performance`: "Model Performance" / "Rendimiento del Modelo"
  - `navigation.about`: "About the Project" / "Acerca del Proyecto"

## Accessibility
- **Contrast**: WCAG AA compliant.
- **Keyboard**: Full navigation support.
- **Focus States**: High-visibility rings on interactive elements.
- **Color Independence**: Indicators use icons or labels alongside color for risk/status.
