from scipy.stats import ranksums
import pandas as pd
from typing import List
from indableau.common.common import EU_ALPHA2_TO_ACC_YEAR, classify_entries_by_memberships_in_eu_and_ea_every_year
from indableau.indicator_plugins import indicators
import matplotlib.pyplot as plt

YEAR_START = 2013
YEAR_END = 2018

RESULTS_HEADERS = {'indicator_name': 'indicator', 'year': 'year', 'z_dist_index': 'z_val', 'p_value': 'p_val'}

results = pd.DataFrame(columns=list(RESULTS_HEADERS.values()))

for indicator_name in ('global_innovation_index',):#indicators.get_available_indicators():
    ind_all = indicators.get(indicator_name, list(EU_ALPHA2_TO_ACC_YEAR.keys()), YEAR_START, YEAR_END)
    ind_euro_area, ind_eu_not_euroarea = classify_entries_by_memberships_in_eu_and_ea_every_year(ind_all)

    for year in range(YEAR_START, YEAR_END+1):
        ind_euroarea_single_year = ind_euro_area[ind_euro_area['year'] == year]
        ind_eu_not_ea_single_year = ind_eu_not_euroarea[ind_eu_not_euroarea['year'] == year]
        statistics, pvalue = ranksums(ind_euroarea_single_year['value'].tolist(),
                                      ind_eu_not_ea_single_year['value'].tolist())

        result = {
            RESULTS_HEADERS['indicator_name']: indicator_name,
            RESULTS_HEADERS['year']: year,
            RESULTS_HEADERS['z_dist_index']: statistics,
            RESULTS_HEADERS['p_value']: pvalue
        }
        results = results.append(result, ignore_index=True)

print(results)

from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.transform import factor_cmap


def get_palette_for_countries(countries: List[str]) -> List[str]:
    EUROAREA_RGB = '#FFCD00'
    EU_NOT_EA_RGB = '#0011FF'

    return [EUROAREA_RGB if country == 'FR' else EU_NOT_EA_RGB for country in countries]


ind_eu_single_year = pd.concat([ind_euroarea_single_year, ind_eu_not_ea_single_year])
ind_eu_single_year.sort_values(by=['value'], ascending=False, inplace=True)
ind_eu_single_year['color'] = ['#FFCD00' if x == 'FR' else '#0011FF' for x in ind_eu_single_year['country']]
countries = ind_eu_single_year['country'].tolist()
values = ind_eu_single_year['value'].tolist()

from bokeh.models import ColumnDataSource

source = ColumnDataSource(data=ind_eu_single_year)
p = figure(x_range=countries)

# color_settings = factor_cmap('countries', palette=get_palette_for_countries(countries), factors=countries)
p.vbar(x='country', top='value', source=source, color='color', width=0.5)
p.xgrid.grid_line_color = None
p.y_range.start = 0


show(p)

