from typing import List
import pandas as pd

from indableau.indicator_plugins.gdp_per_capita_usd import get_gdp_per_capita_usd
from indableau.common.common import DATAFRAME_HEADERS


def get_gdp_per_capita_usd_growth_rate(country_codes_alpha3: List[str], year_start: int, year_end: int) -> pd.DataFrame:
    gdp_per_capita_usd = get_gdp_per_capita_usd(country_codes_alpha3, year_start-1, year_end)
    gdp_per_capita_usd_growth_rate = pd.DataFrame(columns=DATAFRAME_HEADERS)

    for country_code_alpha3 in country_codes_alpha3:
        gdp_per_capita_usd_growth_rate_single_country = \
            gdp_per_capita_usd[gdp_per_capita_usd['country'] == country_code_alpha3]

        gdp_per_capita_usd_growth_rate_single_country['value'] = \
            gdp_per_capita_usd_growth_rate_single_country['value'].pct_change()

        gdp_per_capita_usd_growth_rate_single_country = gdp_per_capita_usd_growth_rate_single_country[
            gdp_per_capita_usd_growth_rate_single_country['year'] != year_start-1]

        gdp_per_capita_usd_growth_rate = gdp_per_capita_usd_growth_rate.append(
            gdp_per_capita_usd_growth_rate_single_country, ignore_index=True)
    return gdp_per_capita_usd_growth_rate
