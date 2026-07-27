# pyright: reportUnknownMemberType=false

from collections.abc import Callable

import streamlit as st

from retail_demand.application.read_results import ResultReader

type Translator = Callable[[str], str]


def render_overview(reader: ResultReader, text: Translator) -> None:
    overview = reader.overview()
    st.header(text("page.overview"))
    st.caption(text("overview.context"))
    period, stores, products = st.columns(3)
    period.metric(
        text("overview.period"),
        f"{overview['dataset_start']} — {overview['dataset_end']}",
    )
    stores.metric(text("overview.stores"), str(overview["store_count"]))
    products.metric(text("overview.products"), str(overview["product_count"]))
    observations, model, version = st.columns(3)
    observations.metric(text("overview.observations"), str(overview["observation_count"]))
    model.metric(text("overview.model"), str(overview["current_model"]))
    version.metric(text("overview.version"), str(overview["artifact_version"]))
    if overview["synthetic"]:
        st.info(text("overview.synthetic"))


def render_forecast(reader: ResultReader, text: Translator) -> None:
    st.header(text("page.forecast"))
    stores = reader.stores()
    products = reader.products()
    store_names = {item["id"]: item["name"] for item in stores}
    product_names = {item["id"]: item["name"] for item in products}
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
    _, frame = reader.forecast(store_id, product_id)
    chart = frame.set_index("date")[["quantity", "prediction"]].rename(
        columns={
            "quantity": text("forecast.actual"),
            "prediction": text("forecast.prediction"),
        }
    )
    st.subheader(text("forecast.history"))
    st.line_chart(chart)

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
    st.subheader(text("forecast.error"))
    st.dataframe(evaluated, hide_index=True, use_container_width=True)

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
    st.subheader(text("forecast.periods"))
    if periods.empty:
        st.caption(text("forecast.no_periods"))
    else:
        st.dataframe(periods, hide_index=True, use_container_width=True)


def render_inventory(reader: ResultReader, text: Translator) -> None:
    st.header(text("page.inventory"))
    left, right = st.columns(2)
    stockout_threshold = left.number_input(
        text("inventory.stockout_threshold"),
        min_value=0.0,
        max_value=90.0,
        value=7.0,
        step=1.0,
    )
    excess_threshold = right.number_input(
        text("inventory.excess_threshold"),
        min_value=stockout_threshold + 1.0,
        max_value=365.0,
        value=max(45.0, stockout_threshold + 1.0),
        step=1.0,
    )
    risk = reader.inventory_risk(stockout_threshold, excess_threshold)
    stockouts, excess = st.columns(2)
    stockouts.metric(text("inventory.stockout_count"), int(risk["stockout_risk"].sum()))
    excess.metric(text("inventory.excess_count"), int(risk["excess_inventory"].sum()))
    display = risk.rename(
        columns={
            "expected_demand": text("inventory.expected"),
            "current_inventory": text("inventory.current"),
            "estimated_coverage_days": text("inventory.coverage"),
            "stockout_risk": text("inventory.stockout"),
            "excess_inventory": text("inventory.excess"),
        }
    )
    st.dataframe(display, hide_index=True, use_container_width=True)


def render_performance(reader: ResultReader, text: Translator) -> None:
    st.header(text("page.performance"))
    st.caption(text("performance.context"))
    metrics = reader.performance()
    overall = metrics[metrics["scope"] == "overall"][
        ["model", "mae", "wape", "mase", "observations"]
    ]
    st.subheader(text("performance.comparison"))
    st.dataframe(overall, hide_index=True, use_container_width=True)
    st.subheader(text("performance.by_store"))
    st.dataframe(
        metrics[metrics["scope"] == "store"],
        hide_index=True,
        use_container_width=True,
    )
    st.subheader(text("performance.by_product"))
    st.dataframe(
        metrics[metrics["scope"] == "product"],
        hide_index=True,
        use_container_width=True,
    )
    st.subheader(text("performance.explanations"))
    st.markdown(
        "\n".join(
            f"- {text(key)}" for key in ("performance.mae", "performance.wape", "performance.mase")
        )
    )


def render_about(text: Translator) -> None:
    st.header(text("page.about"))
    sections = (
        ("about.purpose", "about.purpose_text"),
        ("about.architecture", "about.architecture_text"),
        ("about.choices", "about.choices_text"),
        ("about.synthetic", "about.synthetic_text"),
        ("about.limitations", "about.limitations_text"),
    )
    for heading, body in sections:
        st.subheader(text(heading))
        st.write(text(body))
    st.subheader(text("about.links"))
    st.markdown(
        f"- [{text('about.repository')}](https://github.com/SebastianGaray/retail-demand-intelligence)\n"
        f"- [{text('about.documentation')}](https://github.com/SebastianGaray/retail-demand-intelligence/tree/master/docs)"
    )
