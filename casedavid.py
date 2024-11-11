# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 00:19:47 2024

@author: diadav
"""
import geopandas as gpd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def reproject_geojson(input_file):
    # Load the GeoJSON file
    gdf = gpd.read_file(input_file)

    # Reproject the GeoDataFrame to UTM32N (EPSG:25832)
    gdf_utm = gdf.to_crs(epsg=25832)

    # Create the output file path
    output_file = os.path.join(os.path.dirname(input_file), 'reprojected_file.geojson')

    # Save the reprojected GeoDataFrame to a new GeoJSON file
    gdf_utm.to_file(output_file, driver='GeoJSON')

    print(f"Datasettet er reprojisert til UTM32N (EPSG:25832) og lagret som '{output_file}'.")

if __name__ == "__main__":
    # Hide the root window
    Tk().withdraw()

    # Open a file dialog to select the input file
    input_file = askopenfilename(title="Velg input GeoJSON-fil", filetypes=[("GeoJSON files", "*.geojson")])
    if not input_file:
        print("Ingen fil valgt. Avslutter.")
        exit()

    reproject_geojson(input_file)


# Load the reprojected GeoJSON file
gdf = gpd.read_file('C:/Users/diadav/fkb-case/david/reprojected_file.geojson')

# Initialize a list to store invalid geometries
invalid_geometries = []

# Iterate over each geometry in the GeoDataFrame
for i, geom1 in enumerate(gdf.geometry):
    for j, geom2 in enumerate(gdf.geometry):
        if i != j:
            # Check if geometries intersect or touch
            if geom1.intersects(geom2) or geom1.touches(geom2):
                invalid_geometries.append((i, j, 'intersects or touches'))
            # Check if geometries are within 1 meter of each other
            elif geom1.distance(geom2) < 1:
                invalid_geometries.append((i, j, 'within 1 meter'))

# Print the invalid geometries
for invalid in invalid_geometries:
    print(f"Geometry {invalid[0]} and Geometry {invalid[1]} {invalid[2]}")

if not invalid_geometries:
    print("No invalid geometries found.")

import geopandas as gpd
import json

try:
    # Load the GeoJSON file
    file_path = "C:\\Users\\diadav\\fkb-case\\david\\reprojected_file.geojson"
    with open(file_path) as f:
        data = json.load(f)

    # Convert GeoJSON to GeoDataFrame with the specified CRS (EPSG:25832)
    gdf = gpd.GeoDataFrame.from_features(data['features'], crs='EPSG:25832')

    # Function to find invalid geometries
    def find_invalid_geometries(gdf, threshold=1):
        invalid_geometries = []

        # Check for self-intersections and duplicates
        for i, geom in enumerate(gdf.geometry):
            if not geom.is_valid or gdf.geometry.duplicated().iloc[i]:
                invalid_geometries.append(gdf.iloc[i])

        # Check for geometries that are too close to each other
        for i, geom1 in enumerate(gdf.geometry):
            for j, geom2 in enumerate(gdf.geometry):
                if i != j and geom1.distance(geom2) < threshold:
                    invalid_geometries.append(gdf.iloc[i])
                    break

        return gpd.GeoDataFrame(invalid_geometries, crs='EPSG:25832')

    # Find invalid geometries
    invalid_gdf = find_invalid_geometries(gdf)

    # Save invalid geometries to a new GeoJSON file with the same CRS (EPSG:25832)
    invalid_gdf.to_file('invalid_geometries.geojson', driver='GeoJSON')

    print("Invalid geometries have been saved to 'invalid_geometries.geojson' with CRS EPSG:25832.")

except Exception as e:
    print(f"An error occurred: {e}")

