import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static
st.set_page_config(layout="wide")
burned_area_gdf = gpd.read_file('portugal.geojson')
csv_file = 'MCD64.006.yearly-ba-nf.2002-2022.PRT_Portugal.csv'  
geomcsv = 'portugalcsv.csv'
# Read the CSV data
csv_data = pd.read_csv(csv_file)
geom_csv= pd.read_csv(geomcsv)
# Create a Plotly bar chart
fig = px.bar(csv_data, x='Year', y='Burned Area [ha]', title='Burned Area by Region')
# Ensure the CRS is set
if not burned_area_gdf.crs:
    burned_area_gdf.set_crs(epsg=3857, inplace=True)

# Determine the range of 'Burned_Are' and define 5 equal intervals
min_area = burned_area_gdf['Burned_Are'].min()
max_area = burned_area_gdf['Burned_Are'].max()
interval = (max_area - min_area) / 5
bins = [min_area + i * interval for i in range(6)]

# Create a Folium map object centered on Portugal
m = folium.Map(location=[39.5, -8], zoom_start=7, control_scale=True)
folium.TileLayer('cartodbpositron').add_to(m)
# Add the burned area layer as a choropleth with bins for classification
choropleth = folium.Choropleth(
    geo_data=burned_area_gdf,
    data=burned_area_gdf,
    columns=['Region', 'Burned_Are'],
    key_on='feature.properties.Region',
    fill_color='YlOrRd',
    bins=bins,
    fill_opacity=0.8,
    line_weight=1,
    line_color='gray',
    line_opacity=0.5,
    legend_name='Burned area per region [ha/km²]',
    highlight=True
).add_to(m)

# Add a GeoJson layer for district borders with increased line weight and gray color
folium.GeoJson(
            data=burned_area_gdf,
            style_function=lambda x: {'color': 'gray', 'weight': 2, 'fillOpacity': 0},
            tooltip=folium.GeoJsonTooltip(
                fields=['NAME_1', 'Burned_Are'],
                aliases=['Region', 'Average burned Area'],
                localize=True
            )
        ).add_to(m)
# Adding labels to each region
for _, region in burned_area_gdf.iterrows():
    # Ensure the point exists within the geometry
    point = region['geometry'].centroid
    folium.Marker(
        [point.y, point.x],
        icon=folium.DivIcon(
            html=f'<div style="font-size:6pt; color:black;">{region["NAME_1"]}</div>'
        )
    ).add_to(m)
st.markdown("<h3 style='text-align: center; color: white;'>AVERAGE BURNED AREA PER REGION AREA</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Mainland of Portugal, 2002-2022</h4>", unsafe_allow_html=True)

# Create a layout with three columns
text_info, map_column = st.columns((2.5, 3.7), gap='large')

with map_column:
    folium_static(m, width=500, height=680)
    with st.expander('About', expanded=True):
        st.write('''
            - Author: [Parinda Pannoon](<https://parindapannoon.github.io/>)
            - Data: [Global Wildfire Information System (GWIS)](<https://gwis.jrc.ec.europa.eu/apps/country.profile/overview>).
            - Map spatial reference: EPSG 3857
            ''')
# Add a checkbox for selecting years
def display_state_filter(df, state_name):
    state_list = [''] + list(df['Region'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)


def display_fire_filters(geom_csv, title, title1, string_format='{:,}', string_format1='{:,}'):
    state_list = list(geom_csv['Region'].unique())
    state_list.sort()
    selected_state = st.sidebar.selectbox(':orange[Select Region to visualize Burned area and Number of Fires on the text box]', state_list, len(state_list)-1)
    num = geom_csv[geom_csv['Region'] == selected_state]['Burned_Are'].sum()
    num1 = geom_csv[geom_csv['Region']== selected_state]['of_Fires'].sum()    
    st.markdown(f"""
        <div style="background-color:#363131; padding:10px; border-radius:5px; margin-bottom:15px; border: 2px solid #FFCD91; font-size:15px;">
            <strong>{title}:</strong> {"⚠️"} {string_format.format(num)}
        </div>
    """, unsafe_allow_html=True)
   
    st.markdown(f"""
        <div style="background-color:#363131; padding:10px; border-radius:5px; margin-bottom:15px; border: 2px solid #FFCD91; font-size:15px;">
            <strong>{title1}:</strong> {"🔥"} {string_format1.format(num1)}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<h6 style='font-size: 12px; text-align: left; color: gray;'>Burnt areas are computed from MODIS MCD64 A1 and number of fires from the GlobFire database</h6>", unsafe_allow_html=True)

with st.sidebar:
    st.title(':orange[Portugal wildfire dashboard]')
    st.image('Untitled design (4).png', caption='Credit: freepik', width = 90, output_format='PNG')
    variayear = list(csv_data['Year'])
# Add a checkbox for selecting years
    selected_years = st.multiselect(':orange[Select Year(s)to visualize average burned area[ha] on the bar chart]', csv_data['Year'].unique(), default=variayear)

with text_info:
    with st.container(border=True):
# Filter CSV data based on selected years
        filtered_csv_data = csv_data[csv_data['Year'].isin(selected_years)]
    # Create a Plotly bar chart with filtered data

        fig1 = px.bar(filtered_csv_data, x='Year', y='Burned Area [ha]', title='Average Burned Yearly')
        fig1.update_layout(
        paper_bgcolor='rgba(38,38,38,255)',
        margin=dict(l=2, r=2, t=25, b=2),
        plot_bgcolor='rgba(0,0,0,0)',
        height=200,
        width=250
    )
        fig1.update_traces(marker=dict(color='#FFCD91'))
        st.plotly_chart(fig1, use_container_width=True)
        display_fire_filters(geom_csv, 'Average Burned Area[ha/km²]', 'Avg. Nr. of Fires / Region Area (Km²)')
data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'CO [t]': [6003.392, 1833.516, 111.872, 422.329, 570.058, 66.004, 38504.595, 60943.736, 320.565, 474.087, 193.633, 7.088]
}


co_df = pd.DataFrame(data)
# Display the Line chart in the right column
with text_info:
    with st.container(border=True):
        fig_line = px.line(co_df, x='Month', y='CO [t]', title='CO Emissions by Month', markers=True)
        fig_line.update_traces(line_color='#FFCD91')
        fig_line.update_layout(
            
            paper_bgcolor='rgba(38,38,38,255)',
            legend=dict(font=dict(color='gray'), orientation='h', yanchor='bottom', y=-3.5, xanchor='right', x=2),
            margin=dict(l=30, r=50, t=20, b=20), 
            height=220,
            width= 300
        )
        st.plotly_chart(fig_line)
        st.markdown("<h6 style='font-size: 12px; text-align: left; color: gray;'>The dataset is derived from the Global Fire Emission Database (GFED) which combines satellite information on fire activity and vegetation productivity to estimate fire emissions</h6>", unsafe_allow_html=True)


