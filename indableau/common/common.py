from typing import Tuple, Dict, List
import pycountry as pc
import pandas as pd

DATAFRAME_HEADERS = ('country', 'year', 'value')

DATAFILES_DIR = 'data'

EU_ALPHA2_TO_ACC_YEAR: Dict[str, int] = {'AT': 1995, 'BE': 1952, 'BG': 2007, 'CY': 2004, 'CZ': 2004, 'DK': 1973,
                                         'EE': 2004, 'FI': 1995, 'FR': 1952, 'DE': 1952, 'GR': 1981, 'HU': 2004,
                                         'IE': 1973, 'IT': 1952, 'LV': 2004, 'LT': 2004, 'LU': 1952, 'MT': 2004,
                                         'NL': 1952, 'PL': 2004, 'PT': 1986, 'RO': 2007, 'SK': 2004, 'SI': 2004,
                                         'ES': 1986, 'SE': 1995, 'GB': 1973}

EURO_AREA_ALPHA2_TO_ACC_YEAR: Dict[str, int] = {'AT': 2002, 'BE': 2002, 'CY': 2008, 'EE': 2011, 'FI': 2002,
                                                'FR': 2002, 'DE': 2002, 'GR': 2002, 'IE': 2002, 'IT': 2002,
                                                'LV': 2014, 'LT': 2015, 'LU': 2002, 'MT': 2008, 'NL': 2002,
                                                'PT': 2002, 'SK': 2009, 'SI': 2007, 'ES': 2002}


def get_eu_countries_alpha2_in_year(year: int) -> List[str]:
    return [pc.countries.get(alpha2=country).alpha_3 for country, accession_year in EU_ALPHA2_TO_ACC_YEAR
            if year >= accession_year]


def get_euro_area_countries_alpha2_in_year(year: int) -> List[str]:
    return [pc.countries.get(alpha2=country).alpha_3 for country, accession_year in EURO_AREA_ALPHA2_TO_ACC_YEAR
            if year >= accession_year]


def log(logstr):
    print(logstr)


def get_alpha2_by_country(country: str) -> str:
    country_fuzzy_search_result = [pc.countries.search_fuzzy(country)]

    if isinstance(country_fuzzy_search_result, list):
        print(f'WARNING! Ambiguous country definition {country}. Found: {country_fuzzy_search_result}')
        country_fuzzy_search_result = country_fuzzy_search_result[0][0]

    return country_fuzzy_search_result.alpha_2


def convert_countries_to_alpha2(df: pd.DataFrame) -> pd.DataFrame:
    df_alpha3 = pd.DataFrame(columns=DATAFRAME_HEADERS)
    for country, df_single_country in df.groupby('country'):
        try:
            df_single_country['country'] = get_alpha2_by_country(country)
            df_alpha3 = df_alpha3.append(df_single_country)
        except LookupError as le:
            log(f'WARNING! Cannot find a country: {le}. I\'m dropping all entries related to it.')

    return df_alpha3


def classify_entries_by_memberships_in_eu_and_ea_every_year(entries: pd.DataFrame):
    entries_euroarea = pd.DataFrame(columns=DATAFRAME_HEADERS)
    entries_eu_not_ea = pd.DataFrame(columns=DATAFRAME_HEADERS)

    latest_year = entries['year'].max()

    for country_alpha2, entries_single_country in entries.groupby('country'):
        if country_alpha2 not in EU_ALPHA2_TO_ACC_YEAR:
            continue

        euroarea_accession_year = EURO_AREA_ALPHA2_TO_ACC_YEAR[country_alpha2] \
            if country_alpha2 in EURO_AREA_ALPHA2_TO_ACC_YEAR else latest_year+1

        entries_euroarea = entries_euroarea.append(
            entries_single_country[entries_single_country['year'] >= euroarea_accession_year])

        entries_eu_not_ea = entries_eu_not_ea.append(
            entries_single_country[entries_single_country['year'].isin(
                range(EU_ALPHA2_TO_ACC_YEAR[country_alpha2], euroarea_accession_year))]
        )

    return entries_euroarea, entries_eu_not_ea

