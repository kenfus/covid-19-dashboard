import pandas as pd
from pandas.io.parsers import read_csv
import streamlit as st
import altair as alt
import pathlib
import plotly.express as px
import os 

### Param
DATA_URL = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
ISO_TO_LONLAT_URL = "https://gist.githubusercontent.com/cpl/3dc2d19137588d9ae202d67233715478/raw/3d801e76e1ec3e6bf93dd7a87b7f2ce8afb0d5de/countries_codes_and_coordinates.csv"
DATA_FOR_SELECTION = ['Total cases', 'New cases',
       'New cases smoothed', 'Total deaths', 'New deaths',
       'New deaths smoothed', 'Total cases per million',
       'New cases per million', 'New cases smoothed per million',
       'Total deaths per million', 'New deaths per million',
       'New deaths smoothed per million', 'Reproduction rate', 'Icu patients',
       'Icu patients per million', 'Hosp patients',
       'Hosp patients per million', 'Weekly icu admissions',
       'Weekly icu admissions per million', 'Weekly hosp admissions',
       'Weekly hosp admissions per million', 'New tests', 'Total tests',
       'Total tests per thousand', 'New tests per thousand',
       'New tests smoothed', 'New tests smoothed per thousand',
       'Positive rate', 'Tests per case', 'Tests units', 'Total vaccinations',
       'People vaccinated', 'People fully vaccinated', 'New vaccinations',
       'New vaccinations smoothed', 'Total vaccinations per hundred',
       'People vaccinated per hundred', 'People fully vaccinated per hundred',
       'New vaccinations smoothed per million', 'Stringency index',
       'Population', 'Population density', 'Median age', 'Aged 65 older',
       'Aged 70 older', 'Gdp per capita', 'Extreme poverty',
       'Cardiovasc death rate', 'Diabetes prevalence', 'Female smokers',
       'Male smokers', 'Handwashing facilities', 'Hospital beds per thousand',
       'Life expectancy', 'Human development index']

THRESHOLD_FOR_CASES_PER_MILLION = 10000 # Some countries probably offer no data or clearly wrong data. This is the threshold to filter those out. Also, to keep data lean, we drop a lot of countries.
MAX_COUNTRIES_TO_SHOW = 30 

# HACK This only works when we've installed streamlit with pipenv, so the
# permissions during install are the same as the running process
STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
# We create a downloads directory within the streamlit static asset directory
# and we write output files to it
DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")
if not DOWNLOADS_PATH.is_dir():
    DOWNLOADS_PATH.mkdir()

### Start of Webapp:
# Get Data:
def load_data():
    if not os.path.exists(DATA_URL):
        data = pd.read_csv(DATA_URL)
        long_lat_map = pd.read_csv(ISO_TO_LONLAT_URL, engine='python', sep=',', skipinitialspace=True)[['Alpha-3 code','Latitude (average)', 'Longitude (average)']]
        long_lat_map = long_lat_map.rename(columns={"Latitude (average)": "lat", "Longitude (average)": "lon"})
        data = data.merge(long_lat_map, how = 'inner', left_on = 'iso_code', right_on = 'Alpha-3 code').drop(columns = 'iso_code')
        data.columns = data.columns.str.replace("_", " ")
        data.columns = map(str.capitalize, data.columns)
        data.to_csv(str(DOWNLOADS_PATH / "data.csv"), index=False)


"""
# Covid-19 Data Exploration Dashboard
[![button](https://github.com/kenfus/covid-19-dashboard/blob/master/hosting/GitHub_Logo.png?raw=True)](https://github.com/kenfus/covid-19-dashboard)
"""
st.markdown("<br>", unsafe_allow_html=True)
"""## Explore the Covid-Data from [Our World in Data](https://github.com/owid).
First, you can see, based on the Metric chosen on the left, how the world is doing in the fight against Covid.

Below, it is possible to single out countries. If you want, you can also compare countries against each other and see how they are doing.

Some Countries are missing because the Data is either invalid or does just not exist.
"""

# Load data:
data_load_state = st.text('Loading data...')
load_data()
data_load_state = st.text('New data fetched from https://github.com/owid!')

# Load Data to get information in it:
data = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['Location', 'Total cases per million']).drop_duplicates()
data = data[data['Total cases per million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
data = data.pivot_table(index=['Location'], values=['Total cases per million']).reset_index()


# Load countries in Data.
countries_df = data['Location'].unique()

# Create Sidebar:
# Show selectors for task and framework in sidebar (based on template_dict). These
# selectors determine which template (from template_dict) is used (and also which
# template-specific sidebar components are shown below).
with st.sidebar:
    st.info(
        "🎈 Customize your Dashboard here!"
    )
    st.write("## Global View Metric")
    global_metric = st.selectbox(
        "Which Metric should be shown in the Global View?", list(DATA_FOR_SELECTION)
    )
    st.write("## Analyse specific country")
    country = st.selectbox(
        "Which Country do you want to analyse?", countries_df
    )
    if isinstance(country, str):
        type_data = st.selectbox(
            "Which Metric would you like to see?", list(DATA_FOR_SELECTION)
        )
        # Load Data: Save intermediate steps for readability.
        data_selected = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['Date', 'Location', 'Total cases per million', type_data]).drop_duplicates()
        data_selected = data_selected[data_selected['Total cases per million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
        data_selected['Date'] = pd.to_datetime(data_selected['Date'], format = '%Y-%m-%d')
        data_selected = data_selected.query("Location == @country")

    else:
        pass
    show_second_plot = st.checkbox('Show second country')

# Create relevant data for global view:
# Load Data:
data_global = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['Date', 'Location', 'Alpha-3 code', 'Total cases per million', global_metric]).drop_duplicates()
data_global = data_global[data_global['Total cases per million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
data_global['Date'] = pd.to_datetime(data_global['Date'], format = '%Y-%m-%d')
data_global = data_global.pivot_table(index=['Location', 'Alpha-3 code'], values=[global_metric]).reset_index()
data_global.sort_values(by=[global_metric], inplace=True, ascending=False)

# Title
"""
## Global View
"""
# Plot Data with Plotly:
st.write('Global View: {}'.format(global_metric))
fig = px.choropleth(data_global,
                    locations="Alpha-3 code",
                    color=global_metric, 
                    hover_name="Location",
                    projection="natural earth",
                    color_continuous_scale=px.colors.sequential.Viridis,
                    width=800,
                    height=600,
                    )

st.plotly_chart(fig)

# Plot Data:
st.write("Top {} Countries: {}.".format(MAX_COUNTRIES_TO_SHOW, global_metric))
st.write(alt.Chart(data_global.head(MAX_COUNTRIES_TO_SHOW), width=700).mark_bar().encode(
    x=alt.X('Location', sort=None),
    y=global_metric,
))


# Plot selected Data:
st.write("{}: {}.".format(country, type_data))

# First Plot:

st.write(alt.Chart(data_selected.reset_index(), width=700).mark_line(
    color="lightblue",
    line=True
    ).encode(
        x='Date',
        y=type_data
        )
)

if show_second_plot:
    with st.sidebar:
        st.write("## Second Country")
        country_2 = st.selectbox(
            "Which Country do you want to compare it to?", countries_df
        )
    # Load Data:
    data_selected = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['Date', 'Location', 'Total cases per million', type_data]).drop_duplicates()
    data_selected = data_selected[data_selected['Total cases per million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
    data_selected['Date'] = pd.to_datetime(data_selected['Date'], format = '%Y-%m-%d')
    data_selected = data_selected.query("Location == @country | Location == @country_2")
    # Plot selected Data:
    st.write("{} and {}: {}.".format(country, country_2, type_data))

    st.write(alt.Chart(data_selected.reset_index(), width=700).mark_line(
        color="lightblue",
        line=True
        ).encode(
            x='Date',
            y=type_data,
            color = 'Location'
            )
    )