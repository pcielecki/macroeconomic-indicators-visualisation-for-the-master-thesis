from typing import List
import pandas as pd

from indableau.common.common import get_alpha2_by_country
from indableau.indicator_plugins.gdp_per_capita_usd import get_gdp_per_capita_usd
from indableau.indicator_plugins.gdp_per_capita_usd_growth_rate import get_gdp_per_capita_usd_growth_rate
from indableau.indicator_plugins.global_innovation_index import get_gii


_INDICATORS_TO_GETTERS_MAP = {'gdp_per_capita_usd': get_gdp_per_capita_usd,
                              'gdp_per_capita_usd_growth_rate': get_gdp_per_capita_usd_growth_rate,
                              'global_innovation_index': get_gii}


def get_available_indicators() -> List:
    return list(_INDICATORS_TO_GETTERS_MAP.keys())


def get(indicator_name: str, countries: List[str], year_start: int, year_end: int) -> pd.DataFrame:
    country_codes_alpha3 = [get_alpha2_by_country(country) for country in countries]

    if indicator_name not in _INDICATORS_TO_GETTERS_MAP.keys():
        raise ValueError(f'Cannot find an indicator: {indicator_name}')

    return _INDICATORS_TO_GETTERS_MAP[indicator_name](country_codes_alpha3, year_start, year_end)
