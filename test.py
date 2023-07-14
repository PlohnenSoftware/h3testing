from json import load
with open('ms_A00_Granice_panstwa.geojson') as f:
    borders = load(f)

# print borders

print(borders['features'][0]['geometry']['coordinates'][0])