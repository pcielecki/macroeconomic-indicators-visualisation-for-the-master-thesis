import os
import pandas as pd
import pycountry
from typing import List
from indableau.common.common import DATAFILES_DIR



_DB_FILENAME = os.path.join(DATAFILES_DIR, 'gdp_per_capita_usd', 'DP_LIVE_14022020203602759.csv')
HEADERS_TO_UNIFIED_HEADERS = {'LOCATION': 'country', 'TIME': 'year', 'Value': 'value'}


def get_gdp_per_capita_usd(country_codes_alpha2: List[str], year_start: int, year_end: int) -> pd.DataFrame:
    gdp = pd.read_csv(_DB_FILENAME).filter(list(HEADERS_TO_UNIFIED_HEADERS.keys()))
    time_span_in_years = list(range(year_start, year_end+1))

    gdp = gdp.rename(columns=HEADERS_TO_UNIFIED_HEADERS)
    gdp['country'] = gdp['country'].map(lambda country_alpha3: pycountry.countries.get(alpha_3=country_alpha3).alpha_2)
   # gdp = convert_countries_to_alpha2(gdp)
    return gdp[gdp['country'].isin(country_codes_alpha2) & gdp['year'].isin(time_span_in_years)]
