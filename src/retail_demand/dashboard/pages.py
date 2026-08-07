# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false

from collections.abc import Callable
from html import escape
from math import isnan
from typing import cast

import altair as alt
import pandas as pd
import streamlit as st

from retail_demand.application.read_results import ResultReader

type Translator = Callable[[str], str]


def _help(text: Translator, content_key: str, widget_key: str) -> None:
    with st.popover(
        "",
        icon=":material/help_outline:",
        help=text("help.open"),
        key=widget_key,
    ):
        st.markdown(f'<p class="rdi-help-label">{text("help.about")}</p>', unsafe_allow_html=True)
        st.write(text(f"{content_key}.about"))
        st.markdown(f'<p class="rdi-help-label">{text("help.use")}</p>', unsafe_allow_html=True)
        st.write(text(f"{content_key}.use"))
        st.markdown(f'<p class="rdi-help-label">{text("help.value")}</p>', unsafe_allow_html=True)
        st.write(text(f"{content_key}.value"))


def _heading(title: str, subtitle: str, text: Translator, help_key: str) -> None:
    heading, help_column = st.columns([12, 1], vertical_alignment="center")
    heading.title(title)
    with help_column:
        _help(text, help_key, f"{help_key}_help")
    st.markdown(f'<p class="rdi-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def _section(title: str, text: Translator, help_key: str) -> None:
    heading, help_column = st.columns([12, 1], vertical_alignment="center")
    heading.subheader(title)
    with help_column:
        _help(text, help_key, f"{help_key}_help")


def _number(value: float | int) -> str:
    return f"{value:,.0f}"


def _metric(value: object, digits: int = 2) -> str:
    if value is None:
        return "—"
    try:
        numeric = float(cast(float, value))
    except (TypeError, ValueError):
        return "—"
    return "—" if isnan(numeric) else f"{numeric:,.{digits}f}"


def _metric_strip(items: tuple[tuple[str, str], ...]) -> None:
    metrics = "".join(
        (
            '<div class="rdi-metric-item">'
            f"<span>{escape(label)}</span><strong>{escape(value)}</strong>"
            "</div>"
        )
        for label, value in items
    )
    st.markdown(f'<div class="rdi-metric-strip">{metrics}</div>', unsafe_allow_html=True)


def _kpi_cards(items: tuple[tuple[str, str, str, str, str], ...]) -> None:
    cards = "".join(
        (
            f'<article class="rdi-kpi-card {kind}" title="{escape(help_text)}">'
            f"<header>{escape(label)}</header>"
            f"<div><strong>{escape(value)}</strong>"
            f"<small>{escape(unit)}</small></div></article>"
        )
        for label, value, unit, help_text, kind in items
    )
    st.markdown(f'<div class="rdi-kpi-grid">{cards}</div>', unsafe_allow_html=True)


def _chart_view(text: Translator, key: str) -> str:
    return cast(
        str,
        st.segmented_control(
            text("view.label"),
            options=["chart", "table"],
            format_func=lambda value: text(f"view.{value}"),
            default="chart",
            key=key,
        ),
    )


def _demand_chart(
    frame: pd.DataFrame,
    actual_label: str,
    prediction_label: str,
    *,
    height: int,
) -> alt.Chart:
    chart_data = (
        frame[["date", "quantity", "prediction"]]
        .rename(columns={"quantity": actual_label, "prediction": prediction_label})
        .melt("date", var_name="series", value_name="value")
        .dropna()
    )
    domain = [actual_label, prediction_label]
    return (
        alt.Chart(chart_data)
        .mark_line()
        .encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("value:Q", title=None),
            color=alt.Color(
                "series:N",
                scale=alt.Scale(domain=domain, range=["#1C1B1B", "#334155"]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            strokeDash=alt.StrokeDash(
                "series:N",
                scale=alt.Scale(domain=domain, range=[[1, 0], [7, 5]]),
                legend=None,
            ),
            size=alt.Size(
                "series:N",
                scale=alt.Scale(domain=domain, range=[3, 2]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("series:N", title=None),
                alt.Tooltip("value:Q", title="Units", format=",.2f"),
            ],
        )
        .properties(height=height)
        .interactive()
    )


def _risk_summary(
    rows: tuple[tuple[str, int, float, str], ...],
    item_label: str,
) -> None:
    content = "".join(
        (
            f'<div class="rdi-risk-row {kind}"><span>{escape(label)}</span>'
            f"<strong>{share:.0f}% <small>{count} {escape(item_label)}</small></strong></div>"
        )
        for label, count, share, kind in rows
    )
    st.markdown(f'<div class="rdi-risk-summary">{content}</div>', unsafe_allow_html=True)


def render_overview(reader: ResultReader, text: Translator) -> None:
    _heading(text("page.overview"), text("overview.context"), text, "help.overview")
    with st.spinner(text("loading.overview"), show_time=True):
        overview = reader.overview()
        demand = reader.demand_overview()
        risk = reader.inventory_risk()
        performance = reader.performance("overall")

    _metric_strip(
        (
            (
                text("overview.period"),
                f"{overview['dataset_start']} — {overview['dataset_end']}",
            ),
            (text("overview.stores"), str(overview["store_count"])),
            (text("overview.products"), str(overview["product_count"])),
            (
                text("overview.observations"),
                _number(cast(int, overview["observation_count"])),
            ),
            (text("overview.model"), str(overview["current_model"])),
            (text("overview.version"), str(overview["artifact_version"])),
        )
    )

    chart_column, risk_column = st.columns([5, 2])
    with chart_column, st.container(border=True):
        _section(text("overview.demand"), text, "help.overview_demand")
        if _chart_view(text, "overview_demand_view") == "chart":
            st.altair_chart(
                _demand_chart(
                    demand,
                    text("forecast.actual"),
                    text("forecast.prediction"),
                    height=410,
                ),
                width="stretch",
            )
        else:
            st.dataframe(demand, hide_index=True, width="stretch", height=410)

    with risk_column, st.container(border=True):
        _section(text("overview.risk"), text, "help.overview_risk")
        total = len(risk)
        stockout_count = int(risk["stockout_risk"].sum())
        excess_count = int(risk["excess_inventory"].sum())
        normal_count = total - stockout_count - excess_count
        _risk_summary(
            (
                (
                    text("inventory.stockout_count"),
                    stockout_count,
                    stockout_count / total * 100 if total else 0,
                    "is-critical",
                ),
                (
                    text("inventory.excess_count"),
                    excess_count,
                    excess_count / total * 100 if total else 0,
                    "is-excess",
                ),
                (
                    text("overview.normal"),
                    normal_count,
                    normal_count / total * 100 if total else 0,
                    "is-normal",
                ),
            ),
            text("overview.pairs"),
        )

    with st.container(border=True):
        _section(text("overview.models"), text, "help.overview_models")
        st.dataframe(
            performance[["model", "mae", "wape", "mase", "observations"]],
            hide_index=True,
            width="stretch",
        )

    if overview["synthetic"]:
        st.info(text("overview.synthetic"))


def render_forecast(reader: ResultReader, text: Translator) -> None:
    _heading(text("page.forecast"), text("forecast.context"), text, "help.forecast")
    stores = reader.stores()
    products = reader.products()
    store_names = {item["id"]: item["name"] for item in stores}
    product_names = {item["id"]: item["name"] for item in products}

    with st.container(border=True):
        left, right = st.columns(2)
        store_id = left.selectbox(
            text("forecast.store"),
            list(store_names),
            format_func=lambda identifier: f"{identifier} · {store_names[identifier]}",
        )
        product_id = right.selectbox(
            text("forecast.product"),
            list(product_names),
            format_func=lambda identifier: f"{identifier} · {product_names[identifier]}",
        )

    with st.spinner(text("loading.forecast"), show_time=True):
        model, frame = reader.forecast(store_id, product_id)

    st.markdown(
        f'<p class="rdi-eyebrow">{text("forecast.model")}: {model}</p>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        _section(text("forecast.history"), text, "help.forecast_chart")
        if _chart_view(text, "forecast_demand_view") == "chart":
            st.altair_chart(
                _demand_chart(
                    frame,
                    text("forecast.actual"),
                    text("forecast.prediction"),
                    height=420,
                ),
                width="stretch",
            )
        else:
            st.dataframe(
                frame[["date", "quantity", "prediction"]],
                hide_index=True,
                width="stretch",
                height=420,
            )

    evaluated = frame[frame["prediction"].notna()][
        ["date", "actual", "prediction", "error"]
    ].rename(
        columns={
            "date": text("forecast.date"),
            "actual": text("forecast.actual"),
            "prediction": text("forecast.prediction"),
            "error": text("forecast.error"),
        }
    )
    periods = frame[frame["promotion"] | frame["stockout"]][
        ["date", "price", "promotion", "stockout"]
    ].rename(
        columns={
            "date": text("forecast.date"),
            "price": text("forecast.price"),
            "promotion": text("forecast.promotion"),
            "stockout": text("forecast.stockout"),
        }
    )
    errors, events = st.columns([3, 2])
    with errors, st.container(border=True):
        _section(text("forecast.error"), text, "help.forecast_errors")
        st.dataframe(
            evaluated,
            hide_index=True,
            width="stretch",
            column_config={
                text("forecast.actual"): st.column_config.NumberColumn(format="%.2f"),
                text("forecast.prediction"): st.column_config.NumberColumn(format="%.2f"),
                text("forecast.error"): st.column_config.NumberColumn(format="%.2f"),
            },
        )
    with events, st.container(border=True):
        _section(text("forecast.periods"), text, "help.forecast_events")
        if periods.empty:
            st.caption(text("forecast.no_periods"))
        else:
            st.dataframe(periods, hide_index=True, width="stretch")


def render_inventory(reader: ResultReader, text: Translator) -> None:
    stores = reader.stores()
    products = reader.products()
    store_options: list[str | None] = [None, *(item["id"] for item in stores)]
    product_options: list[str | None] = [None, *(item["id"] for item in products)]
    store_id = cast(str | None, st.session_state.get("inventory_store"))
    product_id = cast(str | None, st.session_state.get("inventory_product"))

    with st.container(border=True):
        heading, low_column, high_column = st.columns([2.2, 1, 1], vertical_alignment="center")
        with heading:
            _heading(text("page.inventory"), text("inventory.context"), text, "help.inventory")
        stockout_threshold = low_column.slider(
            text("inventory.stockout_threshold"),
            min_value=0.0,
            max_value=90.0,
            value=7.0,
            step=1.0,
        )
        excess_threshold = high_column.slider(
            text("inventory.excess_threshold"),
            min_value=stockout_threshold + 1.0,
            max_value=365.0,
            value=max(45.0, stockout_threshold + 1.0),
            step=1.0,
        )

    with st.spinner(text("loading.inventory"), show_time=True):
        risk = reader.inventory_risk(
            stockout_threshold,
            excess_threshold,
            store_id,
            product_id,
        )

    if risk.empty:
        st.warning(text("inventory.no_results"))
        return

    _kpi_cards(
        (
            (
                text("inventory.stockout_count"),
                _number(int(risk["stockout_risk"].sum())),
                text("inventory.pairs"),
                text("help.metric_stockout"),
                "risk",
            ),
            (
                text("inventory.excess_count"),
                _number(int(risk["excess_inventory"].sum())),
                text("inventory.pairs"),
                text("help.metric_excess"),
                "excess",
            ),
            (
                text("inventory.expected"),
                _number(risk["expected_demand"].sum()),
                text("inventory.units"),
                text("help.metric_expected"),
                "",
            ),
            (
                text("inventory.current"),
                _number(risk["current_inventory"].sum()),
                text("inventory.units"),
                text("help.metric_inventory"),
                "",
            ),
            (
                text("inventory.coverage"),
                _metric(risk["estimated_coverage_days"].mean(), 1),
                text("inventory.days"),
                text("help.metric_coverage"),
                "",
            ),
        )
    )

    with st.container(border=True):
        table_heading, store_column, product_column = st.columns(
            [2, 1, 1], vertical_alignment="bottom"
        )
        with table_heading:
            _section(text("inventory.detail"), text, "help.inventory_table")
        store_id = store_column.selectbox(
            text("forecast.store"),
            store_options,
            format_func=lambda value: text("filter.all") if value is None else value,
            key="inventory_store",
        )
        product_id = product_column.selectbox(
            text("forecast.product"),
            product_options,
            format_func=lambda value: text("filter.all") if value is None else value,
            key="inventory_product",
        )
        display = risk.rename(
            columns={
                "expected_demand": text("inventory.expected"),
                "current_inventory": text("inventory.current"),
                "estimated_coverage_days": text("inventory.coverage"),
                "stockout_risk": text("inventory.stockout"),
                "excess_inventory": text("inventory.excess"),
            }
        )
        st.dataframe(
            display,
            hide_index=True,
            width="stretch",
            column_config={
                text("inventory.expected"): st.column_config.NumberColumn(format="%.2f"),
                text("inventory.current"): st.column_config.NumberColumn(format="%.2f"),
                text("inventory.coverage"): st.column_config.NumberColumn(format="%.1f"),
                text("inventory.stockout"): st.column_config.CheckboxColumn(),
                text("inventory.excess"): st.column_config.CheckboxColumn(),
            },
        )
    st.caption(text("inventory.disclaimer"))


def render_performance(reader: ResultReader, text: Translator) -> None:
    _heading(text("page.performance"), text("performance.context"), text, "help.performance")
    with st.spinner(text("loading.performance"), show_time=True):
        metadata = reader.metadata()
        metrics = reader.performance()

    overall = metrics[metrics["scope"] == "overall"]
    champion = overall[overall["model"] == metadata.champion_model].iloc[0]
    _kpi_cards(
        (
            ("MAE", _metric(champion["mae"]), "", text("performance.mae"), ""),
            ("WAPE", _metric(champion["wape"]), "", text("performance.wape"), ""),
            ("MASE", _metric(champion["mase"]), "", text("performance.mase"), "selected"),
            (
                text("performance.observations"),
                _number(int(champion["observations"])),
                text("performance.rows"),
                text("help.metric_observations"),
                "",
            ),
        )
    )

    chart_column, explanation_column = st.columns([2, 1])
    with chart_column, st.container(border=True):
        _section(text("performance.comparison"), text, "help.performance_chart")
        comparison = overall.melt(
            id_vars="model",
            value_vars=["mae", "wape", "mase"],
            var_name="metric",
            value_name="value",
        )
        model_order = ["recent_average", "seasonal_naive", "lightgbm"]
        chart = (
            alt.Chart(comparison)
            .mark_bar(size=28)
            .encode(
                x=alt.X("metric:N", title=None, sort=["mae", "wape", "mase"]),
                xOffset=alt.XOffset("model:N", sort=model_order),
                y=alt.Y("value:Q", title=None),
                color=alt.Color(
                    "model:N",
                    scale=alt.Scale(
                        domain=model_order,
                        range=["#C4C7C7", "#8D9292", "#334155"],
                    ),
                    legend=alt.Legend(title=None, orient="top"),
                ),
                tooltip=[
                    alt.Tooltip("model:N", title="Model"),
                    alt.Tooltip("metric:N", title="Metric"),
                    alt.Tooltip("value:Q", title="Value", format=".4f"),
                ],
            )
            .properties(height=330)
        )
        if _chart_view(text, "performance_comparison_view") == "chart":
            st.altair_chart(chart, width="stretch")
        else:
            st.dataframe(
                overall[["model", "mae", "wape", "mase", "observations"]],
                hide_index=True,
                width="stretch",
                height=330,
            )

    with explanation_column, st.container(border=True):
        st.subheader(text("performance.explanations"))
        st.markdown(
            "\n".join(
                f"- {text(key)}"
                for key in ("performance.mae", "performance.wape", "performance.mase")
            )
        )

    store_tab, product_tab, definitions_tab = st.tabs(
        [
            text("performance.by_store"),
            text("performance.by_product"),
            text("performance.explanations"),
        ]
    )
    with store_tab:
        st.dataframe(
            metrics[metrics["scope"] == "store"],
            hide_index=True,
            width="stretch",
        )
    with product_tab:
        st.dataframe(
            metrics[metrics["scope"] == "product"],
            hide_index=True,
            width="stretch",
        )
    with definitions_tab:
        st.markdown(
            "\n".join(
                f"- {text(key)}"
                for key in ("performance.mae", "performance.wape", "performance.mase")
            )
        )


def render_about(text: Translator) -> None:
    icons = {
        "idea": (
            '<path d="M9 18h6M10 22h4M8.2 14.5A7 7 0 1 1 15.8 14.5'
            'C14.7 15.3 14 16.6 14 18h-4c0-1.4-.7-2.7-1.8-3.5Z"/>'
        ),
        "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/>',
        "code": '<path d="m8 9-3 3 3 3m8-6 3 3-3 3m-2-9-4 12"/>',
        "document": '<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 13h6M9 17h6"/>',
        "database": (
            '<ellipse cx="12" cy="5" rx="8" ry="3"/>'
            '<path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6'
            'c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'
        ),
        "features": '<path d="M4 18 9 12l4 3 7-9M16 6h4v4"/><circle cx="7" cy="6" r="2"/>',
        "model": (
            '<circle cx="12" cy="12" r="7"/><path d="M12 5V2m0 20v-3m7-7h3M2 12h3m3-3 4 3 3-5"/>'
        ),
        "artifact": '<path d="M4 7h16v14H4zM3 3h18v4H3zM9 11h6"/>',
        "interfaces": (
            '<path d="m12 3 4 4-4 4-4-4 4-4Zm-6 8 4 4-4 4-4-4 4-4Z'
            'm12 0 4 4-4 4-4-4 4-4Zm-6 4 4 4-4 4-4-4 4-4Z"/>'
        ),
        "license": '<path d="M12 3v18M5 7h14M7 7l-4 7h8L7 7Zm10 0-4 7h8l-4-7Z"/>',
    }

    def icon(name: str) -> str:
        return (
            '<svg viewBox="0 0 24 24" aria-hidden="true" '
            'fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{icons[name]}</svg>'
        )

    stages = (
        ("database", text("about.stage_data"), text("about.stage_data_detail")),
        ("features", text("about.stage_features"), text("about.stage_features_detail")),
        ("model", text("about.stage_models"), text("about.stage_models_detail")),
        ("artifact", text("about.stage_evaluation"), text("about.stage_evaluation_detail")),
        ("interfaces", text("about.stage_interfaces"), text("about.stage_interfaces_detail")),
    )
    flow = '<span class="rdi-about-arrow">→</span>'.join(
        (
            '<div class="rdi-about-stage">'
            f'<span class="rdi-about-stage-icon">{icon(icon_name)}</span>'
            f"<strong>{escape(stage)}</strong><small>{escape(detail)}</small></div>"
        )
        for icon_name, stage, detail in stages
    )
    decisions = "".join(
        (
            f'<article class="rdi-about-decision {class_name}">'
            f"<strong>{escape(text(title_key))}</strong>"
            f"<p>{escape(text(body_key))}</p></article>"
        )
        for title_key, body_key, class_name in (
            ("about.decision_model", "about.decision_model_text", "primary"),
            ("about.decision_interfaces", "about.decision_interfaces_text", "secondary"),
            ("about.decision_language", "about.decision_language_text", "neutral"),
        )
    )
    st.markdown(
        f"""
        <main class="rdi-about-page">
          <header class="rdi-about-page-header">
            <div>
              <h1>{escape(text("page.about"))}</h1>
              <span>{escape(text("about.title_tag"))}</span>
            </div>
            <nav aria-label="{escape(text("about.links"))}">
              <a class="primary" href="https://github.com/SebastianGaray/retail-demand-intelligence"
                 target="_blank" rel="noopener noreferrer">
                {icon("code")}{escape(text("about.repository"))}
              </a>
              <a href="https://github.com/SebastianGaray/retail-demand-intelligence/tree/master/docs"
                 target="_blank" rel="noopener noreferrer">
                {icon("document")}{escape(text("about.documentation"))}
              </a>
            </nav>
          </header>

          <section class="rdi-about-grid">
            <article class="rdi-about-purpose">
              <div class="rdi-about-purpose-title">
                <span>{icon("idea")}</span>
                <strong>{escape(text("about.purpose"))}</strong>
              </div>
              <p>{escape(text("about.purpose_text"))}</p>
              <ul>
                <li>{icon("check")}<span>{escape(text("about.purpose_forecasting"))}</span></li>
                <li>{icon("check")}<span>{escape(text("about.purpose_inventory"))}</span></li>
              </ul>
            </article>
            <aside class="rdi-about-decisions">
              <h2>{escape(text("about.choices"))}</h2>
              {decisions}
            </aside>
          </section>

          <section class="rdi-about-architecture">
            <header>
              <h2>{escape(text("about.architecture"))}</h2>
              <p>{escape(text("about.architecture_text"))}</p>
            </header>
            <div class="rdi-about-flow">{flow}</div>
          </section>

          <section class="rdi-about-notes">
            <article>
              <h2>{escape(text("about.synthetic"))}</h2>
              <p>{escape(text("about.synthetic_text"))}</p>
            </article>
            <article class="risk">
              <h2>{escape(text("about.limitations"))}</h2>
              <p>{escape(text("about.limitations_text"))}</p>
            </article>
          </section>

          <a class="rdi-about-license"
             href="https://github.com/SebastianGaray/retail-demand-intelligence/blob/master/LICENSE"
             target="_blank" rel="noopener noreferrer">
            {icon("license")}{escape(text("about.license"))}
          </a>
        </main>
        """,
        unsafe_allow_html=True,
    )
