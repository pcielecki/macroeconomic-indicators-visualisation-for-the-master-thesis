import os

from typing import List
import pandas as pd

from indableau.common.common import DATAFRAME_HEADERS, DATAFILES_DIR, convert_countries_to_alpha2

GII_EARLIEST_REPORT = 2013
GII_LATEST_REPORT = 2019

_DB_FILENAMES = {year: os.path.join(DATAFILES_DIR, 'global_innovation_index', f'gii_{year}.csv') for year in range(GII_EARLIEST_REPORT, GII_LATEST_REPORT+1)}

HEADERS_TO_UNIFIED_HEADERS_POINTS = {'Economy': 'country', 'year': 'year', 'Score': 'value'}


def get_gii(country_codes_alpha3: List[str], year_start: int, year_end: int) -> pd.DataFrame:
    gii = pd.DataFrame(columns=list(HEADERS_TO_UNIFIED_HEADERS_POINTS.keys()))

    for year in range(year_start, year_end+1):
        gii_single_year = pd.read_csv(_DB_FILENAMES[year])
        gii_single_year.insert(loc=0, column='year', value=year)
        gii_single_year = gii_single_year[list(HEADERS_TO_UNIFIED_HEADERS_POINTS.keys())]
        gii = gii.append(gii_single_year)

    gii = gii.rename(columns=HEADERS_TO_UNIFIED_HEADERS_POINTS)

    gii = convert_countries_to_alpha2(gii)

    time_span_in_years = list(range(year_start, year_end+1))
    return gii[gii['country'].isin(country_codes_alpha3) & gii['year'].isin(time_span_in_years)]


