# WET - FS21 - Abgabe Vincenzo Timmel
![Covid-19 Dashboard](https://github.com/kenfus/covid-19-dashboard/blob/master/hosting/covid-19-dashboard.png?raw=true)
## Requirements
Requirements can be installed with `pip install requirements.txt`.

It's recommended to first create a virtual environment (e.g. with conda)

## Deploy the Streamlit-App
The app can be started in the Terminal with `streamlit run main.py`. A new Window should open, showing the Dashboard. If not, follow the URL mentioned in the Terminal.

## Testing
The testing can be done with `.\tests\test_interactivity.py --demo --browser=<YOUR BROSWER> --maximize-window` with Browser being one of:
- firefox
- chrome
- edge 

The Tests are also automatically run on every Push to GitHub.

## Overview of App
The App is a simple Dashboard to display Data about COVID-19 with Data from [Our World in Data](https://github.com/owid). On the App, you can see how most Countries are doing on a Global View in regards with over 20 COVID-19 related Metrics. Also, you can single-out Countries and compare them to each other.

## Missing Countries
Some Countries are missing because they offer no or clearly wrong Data. 