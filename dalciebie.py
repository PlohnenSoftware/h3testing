from h3 import h3
import folium

# import geojson file "ms_A00_Granice_panstwa.geojson"
import json
with open('ms_A00_Granice_panstwa.geojson') as f:
    data = json.load(f)


def visualize_hexagons(hexagons, color="red", folium_map=None):
    """
    hexagons is a list of hexcluster. Each hexcluster is a list of hexagons. 
    eg. [[hex1, hex2], [hex3, hex4]]
    """
    polylines = []
    lat = []
    lng = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v:v[0],polyline))
        lng.extend(map(lambda v:v[1],polyline))
        polylines.append(polyline)
    
    if folium_map is None:
        m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
    else:
        m = folium_map
    for polyline in polylines:
        my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color=color)
        m.add_child(my_PolyLine)
    return m
    
def style_function(color):
    return {
        'fillColor': color,
        'color': color,
        'fillOpacity': 0.5,
        'weight': 0
    }

def visualize_polygon(polyline, color):
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
    # my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color=color)

    my_PolyLine = folium.GeoJson(
        {
            "type": "Polygon",
            "coordinates": [polyline]
        },
        style_function=style_function(color)
    )

    m.add_child(my_PolyLine)
    return m

# import geojson file "ms_A00_Granice_panstwa.geojson"
from json import load
with open('ms_A00_Granice_panstwa.geojson') as f:
    borders = load(f)

# borders = {'type': 'Polygon',
#  'coordinates': [[[37.813318999983238, -122.4089866999972145], [ 37.7866302000007224, -122.3805436999997056 ], [37.7198061999978478, -122.3544736999993603], [ 37.7076131999975672, -122.5123436999983966 ], [37.7835871999971715, -122.5247187000021967],  [37.8151571999998453, -122.4798767000009008]]] }

polyline = borders['features'][0]['geometry']['coordinates'][0]
polyline.append(polyline[0])
lat = [p[0] for p in polyline]
lng = [p[1] for p in polyline]
m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color="green")
m.add_child(my_PolyLine)

hexagons = list(h3.polyfill(borders, 8))
polylines = []
lat = []
lng = []
for hex in hexagons:
    polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
    # flatten polygons into loops.
    outlines = [loop for polygon in polygons for loop in polygon]
    polyline = [outline + [outline[0]] for outline in outlines][0]
    lat.extend(map(lambda v:v[0],polyline))
    lng.extend(map(lambda v:v[1],polyline))
    polylines.append(polyline)
for polyline in polylines:
    my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color='red')
    m.add_child(my_PolyLine)

m.save('index.html')