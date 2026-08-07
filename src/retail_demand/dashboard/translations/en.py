from typing import Final

CATALOG: Final[dict[str, str]] = {
    "app.title": "Retail Demand Intelligence",
    "app.language": "Language",
    "app.page": "Page",
    "app.missing_artifacts": "Forecast artifacts are not available.",
    "app.missing_help": "Prepare the local demo, then restart the dashboard:",
    "app.artifact_detail": "Artifact validation",
    "app.unexpected": "The selected view could not be loaded.",
    "loading.artifacts": "Reading forecast artifacts…",
    "loading.overview": "Preparing the demand overview…",
    "loading.forecast": "Preparing demand history…",
    "loading.inventory": "Calculating inventory coverage…",
    "loading.performance": "Loading model metrics…",
    "filter.all": "All",
    "view.label": "Display",
    "view.chart": "Chart",
    "view.table": "Table",
    "help.open": "About this view",
    "help.about": "What it shows",
    "help.use": "How to use it",
    "help.value": "Why it matters",
    "help.overview.about": "A summary of the validated dataset and saved forecast run.",
    "help.overview.use": ("Scan the period, scale, demand trend, risk counts, and model metrics."),
    "help.overview.value": "It confirms which data and model results the dashboard is using.",
    "help.overview_demand.about": "Total daily units sold and champion holdout predictions.",
    "help.overview_demand.use": "Compare the forecast line with observed demand near the end.",
    "help.overview_demand.value": (
        "Large gaps reveal periods worth inspecting by store or product."
    ),
    "help.overview_risk.about": "Store-product pairs below or above the coverage thresholds.",
    "help.overview_risk.use": (
        "Use the Inventory Risk page to adjust thresholds and inspect rows."
    ),
    "help.overview_risk.value": "It highlights where stock coverage may need attention.",
    "help.overview_models.about": "Holdout MAE, WAPE, and MASE for every evaluated model.",
    "help.overview_models.use": "Compare models on the same saved test period.",
    "help.overview_models.value": (
        "It shows whether the selected model improves on simple baselines."
    ),
    "help.forecast.about": "Demand history and saved predictions for one store-product pair.",
    "help.forecast.use": (
        "Choose a store and product, then inspect the chart, errors, and events."
    ),
    "help.forecast.value": ("It connects aggregate model scores with concrete forecast behavior."),
    "help.forecast_chart.about": "Observed daily units and predictions on a shared timeline.",
    "help.forecast_chart.use": "Look for level shifts, recurring peaks, and forecast gaps.",
    "help.forecast_chart.value": "It reveals when a model follows demand and when it misses.",
    "help.forecast_errors.about": ("Actual, predicted, and absolute signed error by holdout date."),
    "help.forecast_errors.use": "Sort or scan the largest positive and negative errors.",
    "help.forecast_errors.value": ("Row-level errors make aggregate metrics easier to interpret."),
    "help.forecast_events.about": "Dates associated with promotions or end-of-day stockouts.",
    "help.forecast_events.use": ("Compare event dates with changes in demand and forecast error."),
    "help.forecast_events.value": (
        "Events provide context for unusual demand or constrained sales."
    ),
    "help.inventory.about": ("Coverage-based stockout and excess indicators for saved forecasts."),
    "help.inventory.use": "Filter entities and adjust the low and high coverage thresholds.",
    "help.inventory.value": "It prioritizes combinations that may warrant inventory review.",
    "help.inventory_table.about": "Expected demand, current stock, coverage, and risk flags.",
    "help.inventory_table.use": (
        "Filter first, then inspect rows outside the selected thresholds."
    ),
    "help.inventory_table.value": "It exposes the quantities behind each risk classification.",
    "help.performance.about": "Holdout errors for the baselines and LightGBM.",
    "help.performance.use": (
        "Select a metric, compare models, then review store and product tabs."
    ),
    "help.performance.value": ("It shows whether results are consistent across business segments."),
    "help.performance_chart.about": "One selected error metric for all evaluated models.",
    "help.performance_chart.use": "Lower bars indicate lower forecast error.",
    "help.performance_chart.value": ("It makes baseline and LightGBM differences easy to compare."),
    "help.about_page.about": "The implemented scope, boundaries, data notice, and limitations.",
    "help.about_page.use": "Use the links for source code, documentation, and license details.",
    "help.about_page.value": "It clarifies what the project demonstrates and what it does not.",
    "help.about_architecture.about": (
        "The path from validated data to saved presentation results."
    ),
    "help.about_architecture.use": "Read the stages from left to right.",
    "help.about_architecture.value": (
        "It shows that FastAPI and Streamlit share application services."
    ),
    "help.metric_stockout": "Pairs below the selected stockout coverage threshold.",
    "help.metric_excess": "Pairs above the selected excess coverage threshold.",
    "help.metric_expected": "Champion forecast demand summed across the test horizon.",
    "help.metric_inventory": "Latest inventory available before the test period.",
    "help.metric_coverage": "Current inventory divided by average forecast daily demand.",
    "help.metric_observations": "Rows evaluated for the champion model in the holdout period.",
    "page.overview": "Overview",
    "page.forecast": "Forecast Explorer",
    "page.inventory": "Inventory Risk",
    "page.performance": "Model Performance",
    "page.about": "About the Project",
    "overview.context": "Local view of synthetic retail demand, forecasts, and inventory.",
    "overview.period": "Dataset period",
    "overview.stores": "Stores",
    "overview.products": "Products",
    "overview.observations": "Observations",
    "overview.model": "Current model",
    "overview.version": "Artifact version",
    "overview.synthetic": "This dashboard uses synthetic data.",
    "overview.demand": "Aggregate demand",
    "overview.risk": "Inventory risk",
    "overview.normal": "Within thresholds",
    "overview.pairs": "pairs",
    "overview.models": "Model comparison",
    "forecast.context": "Inspect saved demand history, holdout predictions, and errors.",
    "forecast.store": "Store",
    "forecast.product": "Product",
    "forecast.model": "Selected model",
    "forecast.history": "Historical demand and holdout predictions",
    "forecast.actual": "Actual",
    "forecast.prediction": "Prediction",
    "forecast.error": "Error inspection",
    "forecast.periods": "Promotion and stockout dates",
    "forecast.date": "Date",
    "forecast.price": "Price",
    "forecast.promotion": "Promotion",
    "forecast.stockout": "Stockout",
    "forecast.no_periods": "No promotion or stockout dates for this selection.",
    "inventory.stockout_threshold": "Stockout coverage threshold (days)",
    "inventory.excess_threshold": "Excess coverage threshold (days)",
    "inventory.stockout_count": "Stockout risks",
    "inventory.excess_count": "Excess indicators",
    "inventory.expected": "Expected demand",
    "inventory.current": "Current inventory",
    "inventory.coverage": "Coverage days",
    "inventory.stockout": "Stockout risk",
    "inventory.excess": "Excess inventory",
    "inventory.pairs": "pairs",
    "inventory.units": "units",
    "inventory.days": "days",
    "inventory.context": "Review coverage indicators using adjustable thresholds.",
    "inventory.detail": "Store-product coverage",
    "inventory.no_results": "No saved rows match the selected filters.",
    "inventory.disclaimer": (
        "Coverage indicators support inspection. They are not replenishment recommendations."
    ),
    "performance.context": "Holdout metrics for each model and segment.",
    "performance.comparison": "Baseline comparison",
    "performance.metric": "Comparison metric",
    "performance.observations": "Observations",
    "performance.rows": "rows",
    "performance.by_store": "Results by store",
    "performance.by_product": "Results by product",
    "performance.explanations": "Metric definitions",
    "performance.mae": "MAE: average absolute unit error.",
    "performance.wape": "WAPE: total absolute error divided by total demand.",
    "performance.mase": "MASE: MAE scaled by the training period's weekly naive error.",
    "about.purpose": "Purpose",
    "about.title_tag": "Project overview",
    "about.context": "Project scope, implementation boundaries, and limitations.",
    "about.purpose_text": (
        "Explore a reproducible retail forecasting workflow through saved local artifacts."
    ),
    "about.architecture": "Architecture",
    "about.architecture_text": (
        "Validated Parquet data feeds application services. FastAPI and Streamlit read the "
        "same artifact run independently."
    ),
    "about.choices": "Implementation choices",
    "about.purpose_forecasting": "Forecast demand with chronological validation.",
    "about.purpose_inventory": "Inspect stockout and excess coverage indicators.",
    "about.decision_model": "Model strategy",
    "about.decision_model_text": (
        "Simple baselines establish the benchmark before LightGBM is considered."
    ),
    "about.decision_interfaces": "Interface boundary",
    "about.decision_interfaces_text": (
        "FastAPI and Streamlit use application services. The dashboard reads saved artifacts."
    ),
    "about.decision_language": "Bilingual interface",
    "about.decision_language_text": (
        "Stable translation keys keep English and Spanish views aligned."
    ),
    "about.choices_text": (
        "Chronological splits, horizon-shifted features, baseline-first selection, typed "
        "boundaries, and immutable run metadata."
    ),
    "about.synthetic": "Synthetic-data notice",
    "about.synthetic_text": (
        "All demo stores, products, demand, prices, promotions, and inventory are generated."
    ),
    "about.limitations": "Limitations",
    "about.limitations_text": (
        "The current evaluation uses one validation block and one test block. Inventory risk "
        "is a coverage indicator, not a replenishment recommendation."
    ),
    "about.links": "Links",
    "about.repository": "Repository",
    "about.documentation": "Documentation",
    "about.license": "MIT License",
    "about.stage_data": "Data and validation",
    "about.stage_data_detail": "Parquet and contracts",
    "about.stage_features": "Temporal features",
    "about.stage_features_detail": "Lags and rolling values",
    "about.stage_models": "Baselines and LightGBM",
    "about.stage_models_detail": "Chronological training",
    "about.stage_evaluation": "Evaluation and artifacts",
    "about.stage_evaluation_detail": "Metrics and predictions",
    "about.stage_interfaces": "API and Streamlit",
    "about.stage_interfaces_detail": "Independent readers",
    "language.en": "English",
    "language.es": "Spanish",
    "navigation.portfolio": "Portfolio ↗",
}
