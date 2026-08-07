from typing import Literal

from retail_demand.dashboard.translations.en import CATALOG as EN_CATALOG
from retail_demand.dashboard.translations.es import CATALOG as ES_CATALOG

type Locale = Literal["en", "es"]

TRANSLATIONS: dict[Locale, dict[str, str]] = {
    "en": EN_CATALOG,
    "es": ES_CATALOG,
}


def translate(locale: Locale, key: str) -> str:
    try:
        return TRANSLATIONS[locale][key]
    except KeyError as error:
        raise KeyError(f"missing translation '{key}' for locale '{locale}'") from error


def missing_translation_keys() -> dict[Locale, set[str]]:
    all_keys: set[str] = set()
    for catalog in TRANSLATIONS.values():
        all_keys.update(catalog)
    return {locale: all_keys - catalog.keys() for locale, catalog in TRANSLATIONS.items()}
