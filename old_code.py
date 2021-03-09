# On a map:
data = pd.read_csv(str(DOWNLOADS_PATH / "data.csv"), usecols = ['lon', 'lat', 'total_cases_per_million', 'total_deaths_per_million', 'total_tests_per_thousand']).drop_duplicates()
data = data[data['total_cases_per_million']>THRESHOLD_FOR_CASES_PER_MILLION].dropna()
data = data.pivot_table(index=['lon', 'lat'], values=['total_cases_per_million']).reset_index()

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

