#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# modified from: https://github.com/mdiener21/python-geospatial-analysis-cookbook/tree/master/ch08/code
# requires: centerline.py (also downloaded from above)

import json
import shapefile
from shapely.geometry import asShape, mapping
from centerline import Centerline

def create_shapes(shapefile_path):
    '''
    Create our Polygon
    :param shapefile_path: full path to shapefile
    :return: list of Shapely geometries
    '''
    in_ply = shapefile.Reader(shapefile_path)
    ply_shp = in_ply.shapes()
    out_multi_ply = [asShape(feature) for feature in ply_shp]
    print("converting to MultiPolygon: ")
    return out_multi_ply

def generate_centerlines(polygon_shps):
    '''
    Create centerlines
    :param polygon_shps: input polygons
    :return: dictionary of linestrings
    '''
    dct_centerlines = {}
    for i, geom in enumerate(polygon_shps):
        print(" now running Centerline creation ", i)
        center_obj = Centerline(geom, 0.00019) # works for image-extracted rivers (cell res=0.0002), if larger than this it will give me QhullError
        center_line_shply_line = center_obj.create_centerline()
        dct_centerlines[i] = center_line_shply_line
    return dct_centerlines

def write_geojson(geojs_file, centerlines):
    '''
    Write output to GeoJSON file
    :param centerlines: input dictionary of linestrings
    :return: GeoJSON file
    '''
    with open(geojs_file, 'w') as out:
        # the head of the geojson file
        out.write('{"type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },"features": [')
        #out.write('{"type": "FeatureCollection", "features": [')
        for i, key in enumerate(centerlines):
            geom = centerlines[key]
            newline = {'type': "Feature", 'id': key, 'geometry': mapping(geom), 'properties': {'id': key}}
            out.write(json.dumps(newline))
            if i < len(centerlines)-1:
                out.write(',') # comma - only for between lines   
        out.write(']}') # tail of the FeatureCollection geojson

if __name__ == '__main__':

    ### change below, centerline distance threshold (line 32), src in line 45
    input_shp = "rasterRivers.shp"
    shply_ply = create_shapes(input_shp)              # run our function to create Shapely multi-polygon geometries
    res_centerlines = generate_centerlines(shply_ply) # create our centerlines
    print("now creating centerlines geojson")
    outgeojs_file = input_shp.strip().split(".")[0]+'_centerlines.geojson'  # define output file name and location
    write_geojson(outgeojs_file, res_centerlines)     # write the output GeoJSON file to disk
