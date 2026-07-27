from functools import partial

import streamlit as st

from retail_demand.application.read_results import ResultReader
from retail_demand.configuration.settings import get_settings
from retail_demand.dashboard.pages import (
    render_about,
    render_forecast,
    render_inventory,
    render_overview,
    render_performance,
)
from retail_demand.dashboard.translations import Locale, translate

st.set_page_config(
    page_title="Retail Demand Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

locale: Locale = st.sidebar.selectbox(
    "Language / Idioma",
    ["en", "es"],
    format_func=lambda value: "English" if value == "en" else "Español",
)
text = partial(translate, locale)
st.sidebar.title(text("app.title"))
pages = {
    text("page.overview"): "overview",
    text("page.forecast"): "forecast",
    text("page.inventory"): "inventory",
    text("page.performance"): "performance",
    text("page.about"): "about",
}
selected = pages[st.sidebar.radio(text("app.page"), list(pages))]
reader = ResultReader(get_settings().artifact_directory)

if not reader.available():
    st.warning(text("app.missing_artifacts"))
    st.write(text("app.missing_help"))
    st.code("make demo")
    render_about(text)
elif selected == "overview":
    render_overview(reader, text)
elif selected == "forecast":
    render_forecast(reader, text)
elif selected == "inventory":
    render_inventory(reader, text)
elif selected == "performance":
    render_performance(reader, text)
else:
    render_about(text)
