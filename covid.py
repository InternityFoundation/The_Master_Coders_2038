# import numpy as np
import pandas as pd
import gmaps
import gmaps.datasets
import googlemaps
import json
# import pprint

API_KEY = ''
gm = googlemaps.Client(key=API_KEY)
gmaps.configure(api_key=API_KEY)
data = pd.read_csv("input_file_v1_dashboard.csv",encoding="ISO-8859-1",low_memory=False)
# print(data.head())
latlon = json.load(open('BMC_Wards.geo.json'))

feat = latlon['features']
l = []
for i in range(len(feat)):
    l.append(feat[i]['geometry']['coordinates'])
# print()

# def Geocode(query):
#     try:
#         geocode_result = gm.geocode(query)[0]       
#         latitude = geocode_result['geometry']['location']['lat']
#         longitude = geocode_result['geometry']['location']['lng']
#         return latitude,longitude
#     except IndexError:
#         return 0
        
# def LocCityState(data):
#     lat=[]
#     lng=[]
#     start = data.index[0]
#     end = data.index[maxRow-1]
#     for i in range(start,end+1,1):
#         isSuccess=True
#         query = data['Ward location'][i] + ' ' + data['City'][i] + ' ' + data['State'][i] 
#         result=Geocode(query)
#     return lat,lng

# [lat,lng]=LocCityState(data)
# df = pd.DataFrame(
#     {'latitude': lat,
#      'longitude': lng
#     })

ciity = gm.geocode('Mumbai')[0]
city_lat=ciity['geometry']['location']['lat']
city_lng=ciity['geometry']['location']['lng']

def drawHeatMap(loc, zoom, intensity, radius):
    heatmap_layer = gmaps.heatmap_layer(loc, dissipating = True)
    heatmap_layer.max_intensity = intensity
    heatmap_layer.point_radius = radius
    fig = gmaps.figure()
    fig = gmaps.figure(center = [city_lat,city_lng], zoom_level=zoom)
    fig.add_layer(heatmap_layer)
    return fig

zoom=15
intensity=7
radius=15
drawHeatMap(l, zoom, intensity, radius)
