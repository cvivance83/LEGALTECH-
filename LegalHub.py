import pandas as pd
import geopandas as gpd
import json
from geopy.geocoders import Nominatim
import utm
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, GeoJSONDataSource, HoverTool
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.palettes import brewer
from bokeh.io import output_notebook
output_notebook()
f='LEGALHUB.xlsx'
data=pd.read_excel(f, header = 0)
list(data)
#countries=sorted(list(set([country.strip() for country in data['Country']])))
cities=sorted(list(set([city.strip() for city in data['City'].dropna()])))
list(cities)
geolocator = Nominatim(user_agent="my-application")
locations = [geolocator.geocode(c) for c in cities]
for location in locations:
    print(location, location.latitude)
    # avec les objets location récupère les attributs de latitude et longitude
latitudes=[location.latitude for location in locations]
longitudes=[location.longitude for location in locations]
# on map a chaque pays sa longitude/latitude au travers de dictionnaires 
latDict=dict(zip(cities, latitudes))
longDict=dict(zip(cities, longitudes))
d=dict(zip(cities,[{'Longitude':'', 'Latitude':''} for c in cities]))
for i in range(len(data)):
    if data['City'][i] in cities:
        d[data['City'][i]]['Type'] = data['Type'][i]
        d[data['City'][i]]['University'] = data['University'][i]
        d[data['City'][i]]['Name'] = data['Name'][i]
        d[data['City'][i]]['Sectors'] = data['Sectors'][i]
        d[data['City'][i]]['Link '] = data['Link '][i]
        d[data['City'][i]]['Longitude'] = longDict[data['City'][i]]
        d[data['City'][i]]['Latitude'] = latDict[data['City'][i]]

ndf=pd.DataFrame.from_dict(d).T
ndfna = ndf[ndf['Type'].notna()]


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
geosource = GeoJSONDataSource(geojson =world.to_json())

#Définir une palette 

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

# Create figure object.
p = figure(title = "LEGAL HUB", 
           plot_height = 700 ,
           plot_width = 1100, 
           toolbar_location = 'below',
           tools='box_zoom, reset, undo, save, pan'
          )
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# On trace la carte du monde grace a notre objet geosource
states = p.patches('xs','ys', source = geosource,
                   fill_color = 'white',
                   line_color = 'black', 
                   line_width = 0.25, 
                   fill_alpha = 1)

sources= ColumnDataSource(
    data=ndfna)

# on positionne les points sur la carte grace aux longitudes et latitudes contenues dans ndf
points = p.circle(x="Longitude", y="Latitude", size=15, fill_color="#FFF8DC", fill_alpha=-9, source=sources)
# on met en hover les infos qu'on veut voir quand on un hover un point
p.add_tools(HoverTool(renderers = [points],
                      tooltips = [
                                ('City','@index'), 
                                ('Name','@{Name}'),
                                ('Type','@Type'),
                                ('Sectors','@{Sectors}'), 
                                ('Link ', '@{Link }')]))


show(p)
