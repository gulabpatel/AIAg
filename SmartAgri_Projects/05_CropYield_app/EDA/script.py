import pandas as pd
from gmplot import gmplot


data = pd.read_csv('historical_actual_crop_yield_by_CAR.csv')

data = data[~(data == -999.0).any(axis=1)]

data.to_csv('Cleaned_data.csv')

unique_crops = data['CROP'].unique()

print("Number of unique crops: ", len(unique_crops))

print("Unique crops: ", unique_crops)

unique_coords = data[['LATITUDE', 'LONGITUDE']].drop_duplicates().values

print("Number of unique coordinates: ", len(unique_coords))

gmap = gmplot.GoogleMapPlotter(unique_coords[:,0].mean(), unique_coords[:,1].mean(), zoom=5)

for lat, lon in unique_coords:
    gmap.marker(lat, lon, color='cornflowerblue')

gmap.draw("map.html")