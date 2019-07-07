#Basic Map Builder
import folium
import pandas

#importing data from the Volcanoes file
data = pandas.read_csv("Volcanoes.txt")

#Storing LAT, LON, NAME, ELEV in the respective dictionaries
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])

#Basic method which determines the color of the marker
#based on elevation level
def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

#Setting the map default location to prospect park
map = folium.Map(location=[40.6623656,-73.9682906],zoom_start=14, tiles="Mapbox Bright")

#Adding more Prospect Park features to the feature group
fgpp = folium.FeatureGroup(name="Prospect Park")
fgpp.add_child(folium.Marker(location=[40.6544993,-73.9689021],popup="Prospect Park Lake",icon=folium.Icon(color='green')))
fgpp.add_child(folium.Marker(location=[40.6605054,-73.9660087],popup="The Boat House and Audubon Center",icon=folium.Icon(color='red')))

#Adding the prospect park feature group to the larger map.
map.add_child(fgpp)


#Creating a feature group for the volcanoes
fgv = folium.FeatureGroup(name="Volcanoes")

#Parsing through the volcanoes list and adding markers to the main map
for lt, ln, el in zip(lat,lon,elev):
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=6,popup=str(el)+" m", fill_color=color_producer(el),color='grey',fill_opacity=0.7))

map.add_child(fgv)

#Creating the population feature group
fgp = folium.FeatureGroup(name="Population")

#Adding the color to the countries based on Population

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange'
            if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

#Adding the population feature group to the main map
map.add_child(fgp)

#Adding the layer control to the main map
map.add_child(folium.LayerControl())

#Saving the map
map.save("Map1.html")
