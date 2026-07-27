from typing import Literal

type Locale = Literal["en", "es"]

TRANSLATIONS: dict[Locale, dict[str, str]] = {
    "en": {
        "app.title": "Retail Demand Intelligence",
        "app.language": "Language",
        "app.page": "Page",
        "app.missing_artifacts": "Forecast artifacts are not available.",
        "app.missing_help": "Prepare the local demo, then restart the dashboard:",
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
        "forecast.store": "Store",
        "forecast.product": "Product",
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
        "performance.context": "Holdout metrics for each model and segment.",
        "performance.comparison": "Baseline comparison",
        "performance.by_store": "Results by store",
        "performance.by_product": "Results by product",
        "performance.explanations": "Metric definitions",
        "performance.mae": "MAE: average absolute unit error.",
        "performance.wape": "WAPE: total absolute error divided by total demand.",
        "performance.mase": "MASE: MAE scaled by the training period's weekly naive error.",
        "about.purpose": "Purpose",
        "about.purpose_text": (
            "Explore a reproducible retail forecasting workflow through saved local artifacts."
        ),
        "about.architecture": "Architecture",
        "about.architecture_text": (
            "Validated Parquet data feeds application services. FastAPI and Streamlit read the "
            "same artifact run independently."
        ),
        "about.choices": "Implementation choices",
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
    },
    "es": {
        "app.title": "Inteligencia de Demanda Minorista",
        "app.language": "Idioma",
        "app.page": "Página",
        "app.missing_artifacts": "Los artefactos de pronóstico no están disponibles.",
        "app.missing_help": "Prepara la demostración local y reinicia el dashboard:",
        "page.overview": "Resumen",
        "page.forecast": "Explorador de Pronósticos",
        "page.inventory": "Riesgo de Inventario",
        "page.performance": "Rendimiento del Modelo",
        "page.about": "Acerca del Proyecto",
        "overview.context": "Vista local de demanda sintética, pronósticos e inventario.",
        "overview.period": "Período del dataset",
        "overview.stores": "Tiendas",
        "overview.products": "Productos",
        "overview.observations": "Observaciones",
        "overview.model": "Modelo actual",
        "overview.version": "Versión del artefacto",
        "overview.synthetic": "Este dashboard utiliza datos sintéticos.",
        "forecast.store": "Tienda",
        "forecast.product": "Producto",
        "forecast.history": "Demanda histórica y predicciones del período de prueba",
        "forecast.actual": "Valor real",
        "forecast.prediction": "Predicción",
        "forecast.error": "Inspección de errores",
        "forecast.periods": "Fechas con promoción o quiebre de stock",
        "forecast.date": "Fecha",
        "forecast.price": "Precio",
        "forecast.promotion": "Promoción",
        "forecast.stockout": "Quiebre de stock",
        "forecast.no_periods": "No hay promociones ni quiebres de stock para esta selección.",
        "inventory.stockout_threshold": "Umbral de cobertura para riesgo de quiebre (días)",
        "inventory.excess_threshold": "Umbral de cobertura para exceso (días)",
        "inventory.stockout_count": "Riesgos de quiebre",
        "inventory.excess_count": "Indicadores de exceso",
        "inventory.expected": "Demanda esperada",
        "inventory.current": "Inventario actual",
        "inventory.coverage": "Días de cobertura",
        "inventory.stockout": "Riesgo de quiebre",
        "inventory.excess": "Exceso de inventario",
        "performance.context": "Métricas del período de prueba para cada modelo y segmento.",
        "performance.comparison": "Comparación de baselines",
        "performance.by_store": "Resultados por tienda",
        "performance.by_product": "Resultados por producto",
        "performance.explanations": "Definiciones de métricas",
        "performance.mae": "MAE: error absoluto promedio en unidades.",
        "performance.wape": "WAPE: error absoluto total dividido por la demanda total.",
        "performance.mase": "MASE: MAE escalado por el error naive semanal del entrenamiento.",
        "about.purpose": "Propósito",
        "about.purpose_text": (
            "Explorar un flujo reproducible de pronóstico minorista mediante artefactos locales "
            "guardados."
        ),
        "about.architecture": "Arquitectura",
        "about.architecture_text": (
            "Los datos Parquet validados alimentan servicios de aplicación. FastAPI y Streamlit "
            "leen la misma ejecución de artefactos de forma independiente."
        ),
        "about.choices": "Decisiones de implementación",
        "about.choices_text": (
            "Períodos cronológicos, variables desplazadas por el horizonte, selección basada "
            "primero en baselines, límites tipados y metadatos inmutables."
        ),
        "about.synthetic": "Aviso sobre datos sintéticos",
        "about.synthetic_text": (
            "Todas las tiendas, productos, demandas, precios, promociones e inventarios de "
            "demostración son generados."
        ),
        "about.limitations": "Limitaciones",
        "about.limitations_text": (
            "La evaluación actual usa un período de validación y uno de prueba. El riesgo de "
            "inventario es un indicador de cobertura, no una recomendación de reposición."
        ),
        "about.links": "Enlaces",
        "about.repository": "Repositorio",
        "about.documentation": "Documentación",
    },
}


def translate(locale: Locale, key: str) -> str:
    try:
        return TRANSLATIONS[locale][key]
    except KeyError as error:
        raise KeyError(f"missing translation '{key}' for locale '{locale}'") from error


def missing_translation_keys() -> dict[Locale, set[str]]:
    all_keys: set[str] = set()
    for translations in TRANSLATIONS.values():
        all_keys.update(translations)
    return {locale: all_keys - translations.keys() for locale, translations in TRANSLATIONS.items()}
