import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --rdi-primary: #334155;
            --rdi-primary-hover: #475569;
            --rdi-secondary: #515f74;
            --rdi-text: #1c1b1b;
            --rdi-text-secondary: #444748;
            --rdi-border: #c4c7c7;
            --rdi-border-strong: #8d9292;
            --rdi-surface: #ffffff;
            --rdi-surface-subtle: #f7f3f2;
            --rdi-surface-elevated: #ebe7e6;
            --rdi-background: #fdf8f8;
            --rdi-focus: #64748b;
            --rdi-success: #2f6b4f;
            --rdi-warning: #8a5b16;
            --rdi-risk: #ba1a1a;
        }

        .stApp {
            background: var(--rdi-background);
            color: var(--rdi-text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stAppViewContainer"] > .main .block-container {
            max-width: 1600px;
            padding: 1.5rem 1.75rem 2.5rem;
        }

        [data-testid="stSidebar"] {
            background: var(--rdi-surface-subtle);
            border-right: 1px solid var(--rdi-border);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        [data-testid="stSidebar"] hr {
            margin: 1rem 0;
        }

        h1, h2, h3 {
            color: var(--rdi-text);
            font-family: "Source Serif 4", Georgia, serif;
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2rem !important;
            line-height: 1.2 !important;
        }

        h2 {
            font-size: 1.35rem !important;
        }

        div[data-testid="stMetric"] {
            background: var(--rdi-surface);
            border-top: 1px solid var(--rdi-border);
            border-bottom: 1px solid var(--rdi-border);
            padding: 0.9rem 0.75rem;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--rdi-secondary);
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        div[data-testid="stMetricValue"] {
            color: #071f2a;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 1.45rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--rdi-surface);
            border-color: var(--rdi-border);
            border-radius: 0.25rem;
        }

        [data-testid="stAppViewContainer"] > .main
        .block-container > [data-testid="stVerticalBlock"] {
            gap: 1rem;
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stNumberInputContainer"] > div {
            border-radius: 0.25rem;
            min-height: 44px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--rdi-border);
            border-radius: 0.25rem;
            overflow: hidden;
        }

        [data-testid="stElementToolbar"] {
            display: none !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 0.25rem;
        }

        [data-testid="stSidebar"] .stButton button {
            border: 0;
            border-radius: 0.25rem;
            justify-content: flex-start;
            min-height: 44px;
            padding-left: 0.8rem;
            text-align: left;
        }

        [data-testid="stSidebar"] .stButton button[kind="tertiary"] {
            color: var(--rdi-secondary);
        }

        [data-testid="stSidebar"] .stButton button[kind="primary"] {
            background: #e7ecef;
            border: 0;
            border-right: 3px solid var(--rdi-primary);
            color: var(--rdi-primary);
            font-weight: 700;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: #eef1f3;
            color: var(--rdi-primary);
        }

        [data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
            min-height: 44px;
            min-width: 3.25rem;
        }

        [data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-pressed="true"] {
            background: var(--rdi-text);
            color: var(--rdi-background);
            font-weight: 700;
        }

        .rdi-eyebrow {
            color: var(--rdi-secondary);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }

        .rdi-subtitle {
            color: var(--rdi-secondary);
            margin: -0.55rem 0 1rem;
        }

        .rdi-metric-strip {
            background: var(--rdi-surface);
            border: 1px solid var(--rdi-border);
            border-radius: 0.5rem;
            display: grid;
            grid-template-columns: 1.35fr repeat(5, minmax(0, 1fr));
            margin-bottom: 0.25rem;
            overflow: hidden;
        }

        .rdi-metric-item {
            border-right: 1px solid var(--rdi-border);
            min-width: 0;
            padding: 0.7rem 0.85rem;
        }

        .rdi-metric-item:last-child {
            border-right: 0;
        }

        .rdi-metric-item span {
            color: var(--rdi-secondary);
            display: block;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            margin-bottom: 0.3rem;
            text-transform: uppercase;
        }

        .rdi-metric-item strong {
            color: #071f2a;
            display: block;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 1.05rem;
            font-weight: 650;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .rdi-kpi-grid {
            display: grid;
            gap: 0.65rem;
            grid-template-columns: repeat(5, minmax(0, 1fr));
        }

        .rdi-kpi-card {
            background: #ffffff;
            border: 1px solid #c1c7cc;
            border-radius: 0.5rem;
            min-width: 0;
            padding: 0.9rem 1rem;
        }

        .rdi-kpi-grid:has(.rdi-kpi-card:nth-child(4):last-child) {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .rdi-kpi-card.selected {
            border-left: 4px solid var(--rdi-primary);
        }

        .rdi-kpi-card header {
            color: var(--rdi-secondary);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            min-height: 2rem;
        }

        .rdi-kpi-card > div {
            align-items: baseline;
            display: flex;
            gap: 0.45rem;
            justify-content: space-between;
        }

        .rdi-kpi-card strong {
            color: #001d29;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 1.55rem;
        }

        .rdi-kpi-card small {
            color: var(--rdi-secondary);
            font-size: 0.62rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .rdi-kpi-card.risk strong {
            color: var(--rdi-risk);
        }

        .rdi-kpi-card.excess strong {
            color: #505f76;
        }

        [data-testid="stSlider"] [role="slider"] {
            background: var(--rdi-primary);
        }

        .rdi-risk-summary {
            display: grid;
            gap: 0.6rem;
        }

        .rdi-risk-row {
            background: #f7f9fa;
            border-left: 3px solid #91a2ad;
            border-radius: 0.25rem;
            padding: 0.85rem 0.9rem;
        }

        .rdi-risk-row span {
            color: var(--rdi-secondary);
            display: block;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }

        .rdi-risk-row strong {
            color: var(--rdi-primary);
            display: block;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 1.55rem;
        }

        .rdi-risk-row small {
            font-family: inherit;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .rdi-risk-row.is-critical {
            background: #fff1f0;
            border-left-color: var(--rdi-risk);
        }

        .rdi-risk-row.is-critical strong {
            color: var(--rdi-risk);
        }

        .rdi-risk-row.is-excess {
            border-left-color: #0e7490;
        }

        .rdi-risk-row.is-normal {
            border-left-color: #39705a;
        }

        .rdi-help-label {
            color: var(--rdi-secondary);
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            margin: 0.6rem 0 0.15rem;
            text-transform: uppercase;
        }

        .rdi-about-page {
            color: #1a1c1d;
            width: 100%;
        }

        .rdi-about-page svg {
            display: block;
            height: 1.1rem;
            width: 1.1rem;
        }

        .rdi-about-page-header {
            align-items: flex-end;
            border-bottom: 1px solid #c1c7cc;
            display: flex;
            justify-content: space-between;
            padding: 0.25rem 0 1.25rem;
        }

        .rdi-about-page-header h1 {
            font-size: 2rem !important;
            margin: 0 0 0.45rem;
        }

        .rdi-about-page-header > div > span {
            background: #083344;
            border-radius: 0.15rem;
            color: #ffffff;
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.3rem 0.7rem;
        }

        .rdi-about-page-header nav {
            display: flex;
            gap: 0.75rem;
        }

        .rdi-about-page-header a,
        .rdi-about-license {
            align-items: center;
            border: 1px solid #083344;
            border-radius: 0.25rem;
            color: #083344 !important;
            display: inline-flex;
            font-size: 0.78rem;
            font-weight: 600;
            gap: 0.5rem;
            justify-content: center;
            min-height: 40px;
            padding: 0 1rem;
            text-decoration: none !important;
        }

        .rdi-about-page-header a.primary {
            background: #083344;
            color: #ffffff !important;
        }

        .rdi-about-page-header a:hover,
        .rdi-about-license:hover {
            background: #e8eef1;
        }

        .rdi-about-page-header a.primary:hover {
            background: #001d29;
        }

        .rdi-about-grid {
            display: grid;
            gap: 1.25rem;
            grid-template-columns: minmax(0, 7fr) minmax(320px, 5fr);
            margin-top: 1.25rem;
        }

        .rdi-about-purpose,
        .rdi-about-decisions,
        .rdi-about-architecture,
        .rdi-about-notes article {
            background: #ffffff;
            border: 1px solid #d7dcdf;
            border-radius: 0.45rem;
        }

        .rdi-about-purpose,
        .rdi-about-decisions {
            min-height: 310px;
            padding: 1.4rem;
        }

        .rdi-about-purpose-title,
        .rdi-about-decisions > h2,
        .rdi-about-architecture h2 {
            align-items: center;
            display: flex;
            font-size: 1rem !important;
            gap: 0.7rem;
            margin: 0 0 1.25rem;
        }

        .rdi-about-purpose-title > span {
            align-items: center;
            background: #083344;
            border-radius: 0.15rem;
            color: #a7cce1;
            display: flex;
            height: 36px;
            justify-content: center;
            width: 36px;
        }

        .rdi-about-purpose-title > strong {
            color: #071f2a;
            font-size: 1rem;
        }

        .rdi-about-purpose p {
            color: #41484c;
            line-height: 1.55;
            margin: 0;
            max-width: 620px;
        }

        .rdi-about-purpose ul {
            display: grid;
            gap: 0.75rem;
            list-style: none;
            margin: 1.3rem 0 0;
            padding: 0;
        }

        .rdi-about-purpose li {
            align-items: flex-start;
            color: #41484c;
            display: flex;
            gap: 0.65rem;
        }

        .rdi-about-purpose li svg {
            color: #083344;
            flex: 0 0 auto;
            margin-top: 0.1rem;
        }

        .rdi-about-decisions > h2 > span {
            font-size: 1.5rem;
            line-height: 1;
        }

        .rdi-about-decision {
            background: #f1f1f3;
            border-left: 3px solid #083344;
            margin-bottom: 0.7rem;
            padding: 0.85rem 0.9rem;
        }

        .rdi-about-decision.secondary {
            border-left-color: #62758a;
        }

        .rdi-about-decision.neutral {
            border-left-color: #82888c;
        }

        .rdi-about-decision strong,
        .rdi-about-notes h2 {
            color: #083344;
            font-size: 0.68rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .rdi-about-decision p {
            font-size: 0.8rem;
            line-height: 1.45;
            margin: 0.3rem 0 0;
        }

        .rdi-about-architecture {
            margin-top: 1.25rem;
            padding: 1.4rem;
        }

        .rdi-about-architecture header p {
            color: #59656b;
            font-size: 0.82rem;
            margin: -0.8rem 0 0;
        }

        .rdi-about-flow {
            align-items: center;
            display: flex;
            justify-content: space-between;
            padding: 2.3rem 0.25rem 0.75rem;
        }

        .rdi-about-stage {
            align-items: center;
            display: flex;
            flex: 1;
            flex-direction: column;
            min-width: 0;
            text-align: center;
        }

        .rdi-about-stage-icon {
            align-items: center;
            background: #e2e2e4;
            border: 1px solid #c1c7cc;
            border-radius: 0.55rem;
            color: #1a1c1d;
            display: flex;
            height: 52px;
            justify-content: center;
            margin-bottom: 0.75rem;
            transition: background 150ms ease, color 150ms ease;
            width: 52px;
        }

        .rdi-about-stage-icon svg {
            height: 25px;
            width: 25px;
        }

        .rdi-about-stage:last-child .rdi-about-stage-icon,
        .rdi-about-stage:hover .rdi-about-stage-icon {
            background: #083344;
            color: #ffffff;
        }

        .rdi-about-stage strong {
            color: #083344;
            font-size: 0.76rem;
        }

        .rdi-about-stage small {
            color: #59656b;
            font-size: 0.64rem;
            margin-top: 0.2rem;
        }

        .rdi-about-arrow {
            color: #b4bec3;
            font-size: 1.3rem;
            padding-bottom: 2.8rem;
        }

        .rdi-about-notes {
            display: grid;
            gap: 1.25rem;
            grid-template-columns: 1fr 1fr;
            margin-top: 1.25rem;
        }

        .rdi-about-notes article {
            padding: 1rem 1.15rem;
        }

        .rdi-about-notes h2 {
            margin: 0 0 0.55rem;
        }

        .rdi-about-notes article.risk h2 {
            color: #ba1a1a;
        }

        .rdi-about-notes p {
            color: #41484c;
            font-size: 0.8rem;
            line-height: 1.5;
            margin: 0;
        }

        .rdi-about-license {
            margin-top: 0.85rem;
        }

        [data-testid="stPopover"] button {
            border-color: var(--rdi-border);
            border-radius: 999px;
            min-height: 38px;
            min-width: 38px;
            padding: 0.35rem;
        }

        .rdi-brand {
            color: var(--rdi-primary);
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0;
        }

        .rdi-brand-note {
            color: var(--rdi-secondary);
            font-size: 0.75rem;
            letter-spacing: 0.04em;
            margin: 0 0 1.5rem;
        }

        .rdi-site-footer {
            background: var(--rdi-surface-subtle);
            border-top: 1px solid var(--rdi-border);
            margin-top: 3rem;
            padding: 2.25rem 0;
        }

        .rdi-footer-shell,
        .rdi-footer-shell > div,
        .rdi-site-footer nav {
            align-items: center;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .rdi-footer-shell {
            justify-content: space-between;
        }

        .rdi-footer-shell > div > strong {
            color: var(--rdi-text);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.2rem;
        }

        .rdi-footer-shell small {
            color: var(--rdi-secondary);
            font-size: 0.68rem;
            letter-spacing: 0.04em;
        }

        .rdi-site-footer nav a {
            color: var(--rdi-primary);
            font-size: 0.75rem;
        }

        code {
            color: var(--rdi-primary) !important;
        }

        a {
            color: var(--rdi-primary);
            text-underline-offset: 0.22em;
        }

        a:focus-visible,
        button:focus-visible,
        [role="button"]:focus-visible,
        input:focus-visible,
        select:focus-visible {
            border-radius: 2px;
            outline: 2px solid var(--rdi-focus) !important;
            outline-offset: 4px;
        }

        button[kind="primary"]:not([data-testid="stBaseButton-primary"]),
        [data-testid="stBaseButton-primary"] {
            background: #000000;
            border: 1px solid #000000;
            border-radius: 0.25rem;
            color: #ffffff;
            font-weight: 600;
        }

        [data-testid="stBaseButton-primary"]:hover {
            background: var(--rdi-primary-hover);
            border-color: var(--rdi-primary-hover);
            color: #f8fafc;
        }

        [data-testid="stBaseButton-secondary"],
        [data-testid="stDownloadButton"] button,
        [data-testid="stLinkButton"] a {
            background: transparent;
            border: 1px solid var(--rdi-border);
            border-radius: 0.25rem;
            color: var(--rdi-text);
            font-weight: 600;
        }

        [data-testid="stBaseButton-secondary"]:hover,
        [data-testid="stDownloadButton"] button:hover,
        [data-testid="stLinkButton"] a:hover {
            background: var(--rdi-surface-elevated);
            border-color: var(--rdi-border-strong);
        }

        .rdi-kpi-card,
        .rdi-about-purpose,
        .rdi-about-decisions,
        .rdi-about-architecture,
        .rdi-about-notes article {
            background: var(--rdi-surface);
            border-color: var(--rdi-border);
            border-radius: 0.25rem;
        }

        .rdi-kpi-card strong,
        .rdi-metric-item strong,
        .rdi-risk-row strong,
        .rdi-about-purpose-title > strong {
            color: var(--rdi-text);
        }

        .rdi-risk-row {
            background: var(--rdi-surface-subtle);
        }

        .rdi-about-page,
        .rdi-about-purpose p,
        .rdi-about-purpose li,
        .rdi-about-notes p {
            color: var(--rdi-text-secondary);
        }

        .rdi-about-page-header,
        .rdi-about-stage-icon {
            border-color: var(--rdi-border);
        }

        .rdi-about-page-header > div > span,
        .rdi-about-purpose-title > span,
        .rdi-about-stage:last-child .rdi-about-stage-icon,
        .rdi-about-stage:hover .rdi-about-stage-icon {
            background: var(--rdi-primary);
            color: #f8fafc;
        }

        .rdi-about-page-header a,
        .rdi-about-license {
            border-color: var(--rdi-primary);
            color: var(--rdi-primary) !important;
        }

        .rdi-about-page-header a.primary {
            background: #000000;
            border-color: #000000;
            color: #ffffff !important;
        }

        .rdi-about-page-header a:hover,
        .rdi-about-license:hover {
            background: var(--rdi-surface-elevated);
        }

        .rdi-about-page-header a.primary:hover {
            background: var(--rdi-primary-hover);
            border-color: var(--rdi-primary-hover);
        }

        @media (max-width: 780px) {
            [data-testid="stAppViewContainer"] > .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.25rem;
            }

            h1 {
                font-size: 1.65rem !important;
            }

            div[data-testid="stMetric"] {
                min-height: 96px;
            }

            .rdi-metric-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rdi-metric-item {
                border-bottom: 1px solid var(--rdi-border);
            }

            .rdi-metric-item:nth-child(2n) {
                border-right: 0;
            }

            .rdi-kpi-grid,
            .rdi-kpi-grid:has(.rdi-kpi-card:nth-child(4):last-child) {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .rdi-about-page-header {
                align-items: flex-start;
                flex-direction: column;
                gap: 1rem;
            }

            .rdi-about-page-header nav,
            .rdi-about-page-header a {
                width: 100%;
            }

            .rdi-about-grid,
            .rdi-about-notes {
                grid-template-columns: 1fr;
            }

            .rdi-about-purpose,
            .rdi-about-decisions {
                min-height: auto;
            }

            .rdi-footer-shell {
                align-items: flex-start;
                flex-direction: column;
            }

            .rdi-about-flow {
                align-items: stretch;
                flex-direction: column;
                gap: 0.65rem;
            }

            .rdi-about-arrow {
                padding: 0;
                transform: rotate(90deg);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
