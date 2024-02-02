import geopandas as gpd
import pandas as pd
import geopy.distance
import streamlit as st
import pydeck as pdk
import numpy as np
import requests
import json
import sys
import os
import csv
import geojson
# import folium
# from streamlit_folium import folium_static

st.set_page_config(
    page_title = "Penggunaan Streamlit Peta"
     ,layout='wide'
)

firm = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/api/country/csv/db7fc70ee5fcbfd778719faf49676969/VIIRS_SNPP_NRT/IDN/7')
#print(firm.head())

# # Define the condition for row deletion
# condition = (firm['longitude']  < 94.5 ) | (firm['longitude'] > 105.5 ) | (firm['latitude']  > -1.5 ) | (firm['longitude'] < -5.7 ) # Replace with your actual column name and value
#
#
# # Use the condition to filter out rows to be deleted
# firm = firm[~condition]
# print('Rows with the specified condition have been deleted.')

# Specify the file path where you want to save the CSV file
csv_file_path = 'io.csv'

# Write the DataFrame to a CSV file
firm.to_csv(csv_file_path, index=False)




def csv_to_geojson(csv_file, geojson_file):
    features = []
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # Assuming your CSV has 'latitude' and 'longitude' columns
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            feature = geojson.Feature(
                geometry=geojson.Point((longitude, latitude)),
                properties=row
            )
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    with open(geojson_file, 'w') as f:
        geojson.dump(feature_collection, f, indent=2)

# Replace 'input.csv' and 'output.geojson' with your file names
csv_to_geojson('io.csv', 'output.geojson')


# url = "https://indonesia-geohazard-mitigation-and-assessment-data.p.rapidapi.com/status_gunung_api"
#
# headers = {
# 	"X-RapidAPI-Key": "cfcbcd292bmsh3f8583407dffef5p161481jsn85edc0a9b031",
# 	"X-RapidAPI-Host": "indonesia-geohazard-mitigation-and-assessment-data.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.json())
#
# text = json.dumps(response.json(),sort_keys=True, indent=4)
# print(text)
#
# f = open("output.geojson", "wt")
# f.write(text)

df2 = gpd.read_file('output.geojson')
st.write(df2.head(5))
df2['lon'] = df2.geometry.x  # extract longitude from geometry
df2['lat'] = df2.geometry.y  # extract latitude from geometry
df2 = df2[['lon','lat']]     # only keep longitude and latitude

st.markdown("<h3 style='text-align: center; color: red;'>Peta Titik Api 7 Hari Terakhir</h3>", unsafe_allow_html=True)
# st.map(df2,zoom=8,size=20)


pollute=[]
firms = pd.DataFrame(
        df2,
        columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
        map_provider='carto',
        map_style='dark',
        views=pdk.View(type="mapview",controller=True),
        initial_view_state=pdk.ViewState(
            latitude=-2.9831
,           longitude=104.7527,
            zoom=8,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=pollute,
                get_position='[lon, lat]',
                 get_color='[100, 30, 200, 100]',
                get_radius=3000,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                 data=firms,
                 get_position='[lon, lat]',
                 get_color='[200, 30, 0, 200]',
                 get_radius=500,
            ),
        ],
))


