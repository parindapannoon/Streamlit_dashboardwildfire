[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appdashboardwildfire-uvch9r5rhparinda.streamlit.app/)
# Installation
```
pip install streamlit
```
```
pip install streamlit-folium
```
Run an app
```
streamlit run f.py
```
# Styling color theme
create config.toml file to define theme colors, in the [theme] section of a ```.streamlit/config.toml``` file can set primaryColor, backgroundColor, secondaryBackgroundColor, and textColor.
```
[theme]
primaryColor="#000000"
backgroundColor="#251507"
secondaryBackgroundColor="#993303"
textColor="#ffffff"
```
# Requirements
```
streamlit==1.34.0
streamlit_folium==0.20.0
geopandas
pandas
plotly==5.17.0
```
# Data source
[Global Wildfire Information System (GWIS)](https://gwis.jrc.ec.europa.eu/apps/country.profile/overview/ADM0/GRC)

# Example
![Screenshot (2398)](https://github.com/parindapannoon/Streamlit_dashboardwildfire/assets/119694198/d8249253-78da-46ad-94dd-ea28c1fde566)
