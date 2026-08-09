# Global controls requirements

## Goal

Align application-owned language chrome with the portfolio family while retaining Streamlit's complete native theme surface.

## Requirements

- Replace the language select with a compact `EN / ES` segmented control near the top of the sidebar.
- Place language before page navigation and retain the selection for the session.
- Keep theme selection in Streamlit's settings menu because the framework owns widget and chart themes.
- Explain the platform exception in the interface mapping and tests.

## Acceptance criteria

- Integration tests change locale through the segmented control.
- Navigation, artifacts, responsive behavior, and the native theme contract remain intact.
