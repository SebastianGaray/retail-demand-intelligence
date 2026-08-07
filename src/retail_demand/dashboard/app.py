from functools import partial
from pathlib import Path
from typing import cast

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
from retail_demand.dashboard.styles import apply_styles
from retail_demand.dashboard.translations import Locale, translate

st.set_page_config(
    page_title="Retail Demand Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()
settings = get_settings()

st.sidebar.markdown('<p class="rdi-brand">Retail Intelligence</p>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<p class="rdi-brand-note">DEMAND &amp; SUPPLY · 0.1.0</p>',
    unsafe_allow_html=True,
)
if "dashboard_locale" not in st.session_state:
    st.session_state.dashboard_locale = settings.default_locale
locale = cast(Locale, st.session_state.dashboard_locale)
text = partial(translate, locale)
navigation = (
    ("overview", "page.overview", ":material/dashboard:"),
    ("inventory", "page.inventory", ":material/warning:"),
    ("forecast", "page.forecast", ":material/trending_up:"),
    ("performance", "page.performance", ":material/analytics:"),
    ("about", "page.about", ":material/info:"),
)
if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "overview"


def _select_page(page: str) -> None:
    st.session_state.dashboard_page = page


for page, label, icon in navigation:
    st.sidebar.button(
        text(label),
        key=f"navigation_{page}",
        icon=icon,
        type="primary" if st.session_state.dashboard_page == page else "tertiary",
        width="stretch",
        on_click=_select_page,
        args=(page,),
    )

st.sidebar.divider()
st.sidebar.selectbox(
    text("app.language"),
    ["en", "es"],
    format_func=lambda value: text(f"language.{value}"),
    key="dashboard_locale",
)
st.sidebar.link_button(
    text("navigation.portfolio"),
    "https://sebastiangaray.github.io/",
    width="stretch",
)
selected = st.session_state.dashboard_page


@st.cache_resource
def _reader(artifact_directory: str) -> ResultReader:
    return ResultReader(Path(artifact_directory))


artifact_directory = str(settings.artifact_directory)
reader = _reader(artifact_directory)
with st.spinner(text("loading.artifacts"), show_time=True):
    artifact_error = reader.availability_error()

if artifact_error is not None:
    st.warning(text("app.missing_artifacts"))
    st.caption(f"{text('app.artifact_detail')}: {artifact_error}")
    st.write(text("app.missing_help"))
    st.code("make demo")
    render_about(text)
else:
    try:
        if selected == "overview":
            render_overview(reader, text)
        elif selected == "forecast":
            render_forecast(reader, text)
        elif selected == "inventory":
            render_inventory(reader, text)
        elif selected == "performance":
            render_performance(reader, text)
        else:
            render_about(text)
    except (OSError, ValueError):
        st.error(text("app.unexpected"))
