import pandas as pd
import numpy as np
from pandas.io.parsers import read_csv
import streamlit as st
import pydeck as pdk
import altair as alt
import pathlib

### Param
DATA_URL = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
ISO_TO_LONLAT_URL = "https://gist.githubusercontent.com/cpl/3dc2d19137588d9ae202d67233715478/raw/3d801e76e1ec3e6bf93dd7a87b7f2ce8afb0d5de/countries_codes_and_coordinates.csv"
LOCATION_COLUMN = 'location'
THRESHOLD_FOR_CASES_PER_MILLION = 10000 # Some countries probably ofer no data. This is the threshold to filter those out. Also, to keep data lean, we drop a lot of countries.

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
    data = pd.read_csv(DATA_URL)
    long_lat_map = pd.read_csv(ISO_TO_LONLAT_URL, engine='python', sep=',', skipinitialspace=True)[['Alpha-3 code','Latitude (average)', 'Longitude (average)']]
    long_lat_map = long_lat_map.rename(columns={"Latitude (average)": "lat", "Longitude (average)": "lon"})
    data = data.merge(long_lat_map, how = 'inner', left_on = 'iso_code', right_on = 'Alpha-3 code').drop(columns = 'iso_code')
    data.to_csv(str(DOWNLOADS_PATH / "data.csv"), index=False)


# Load data:
data_load_state = st.text('Loading data')
# Create a text element and let the reader know the data is loading.
load_data()
data = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['location', 'total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand']).drop_duplicates()
data = data[data['total_cases_per_million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
data = data.pivot_table(index=['location'], values=['total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand'])
data_load_state.text("Done!")

# Show total cases per million per country:
st.bar_chart(data)

# On a map:
data = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['lon', 'lat', 'total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand']).drop_duplicates()
data = data[data['total_cases_per_million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
data = data.pivot_table(index=['lon', 'lat'], values=['total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand']).reset_index()

st.map(data)

##
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=42.8182,
        longitude=9.2275,
        zoom=2,
        pitch=50
    ),
    layers=[
        pdk.Layer(
           'ColumnLayer',
           data=data,
           get_position='[lon, lat]',
           radius=40000,
           elevation_scale=10,
           get_elevation="total_cases_per_million",
           auto_highlight=True,
           pickable=False,
           extruded=True,
        ),
    ],
))

