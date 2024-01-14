import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import geopandas as gpd


APP_TITLE = "Diverse Île-de-France"
APP_SUB_TITLE = 'Exploring the Proportion of Immigrants in the Region'

df3 = pd.read_pickle('df_final_immigres.pkl')
df3["Pourcentage d'immigrés"] = pd.to_numeric(df3["Pourcentage d'immigrés"].str.strip().str.replace(",", ".").str.replace(" %",""))
df3 = df3[['insee',"Pourcentage d'immigrés"]]
df3['insee'] = df3['insee'].astype(str)
df3 = df3.rename(columns={'insee': 'com_code'})

gpd_geo = gpd.read_file("communes-france.geojson")
gpd_geo = gpd_geo.merge(df3, on='com_code')
geo_json_data = gpd_geo.to_json()

texte = "Proportion of immigrants expressed as a percentage of the population in Île-de-France"
st.markdown(f"<h1 style='background-color:#FEEAE0;color:rgb(49, 51, 63);font-size:2.75rem;'>{texte}</h1><br/>", unsafe_allow_html=True)

m = folium.Map(location=(48.666667, 2.533333), zoom_start=8, tiles="cartodb positron")

choropleth = folium.Choropleth(
    geo_data=geo_json_data,
    name="choropleth",
    data=df3,
    columns=["com_code", "Pourcentage d'immigrés"],
    key_on="feature.properties.com_code",
    fill_color="Reds",
    fill_opacity=0.7,
    line_opacity=0.2,
    #bins=[0, 10, 20, 30, 40, 50],
    legend_name="Pourcentage (%)"
).add_to(m)

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(fields=["com_name","Pourcentage d'immigrés"],
                                   aliases=['Commune Name :&nbsp;',"Migration Ratio %:&nbsp;"],
                                   labels=True,
                                   localize=True,
                                   sticky=False,
                                   style="""
                                   background-color: #F0EFEF;
                                   border: 2px solid black;
                                   border-radius: 3px;
                                   box-shadow: 3px;
                                   """,)
)

st_data = st_folium(m, width = 725)

st.markdown('Data 2020 - [Linternaute.com](https://www.linternaute.com/ville/classement/villes/immigres) (Source: Insee)')

folium.LayerControl().add_to(m)