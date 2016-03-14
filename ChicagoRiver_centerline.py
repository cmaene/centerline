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
        print(" now running Centerline creation")
        center_obj = Centerline(geom, 5) # 5 is the guessed smallest nodes distance, to avoid QhullError
        center_line_shply_line = center_obj.create_centerline()
        dct_centerlines[i] = center_line_shply_line
    return dct_centerlines

def write_geojson(geojs_file, centerlines):
    '''
    Write output to GeoJSON file
    :param centerlines: input dictionary of linestrings
    :return: write to GeoJSON file
    '''
    with open(geojs_file, 'w') as out:
        # add the head of the geojson file
        out.write('{"type": "FeatureCollection", "crs": { "type": "link", "properties": { "href": "http://spatialreference.org/ref/esri/nad-1983-stateplane-illinois-east-fips-1201-feet/proj4/", "type": "proj4" } },"features": [')
        for i, key in enumerate(centerlines):
            geom = centerlines[key]
            newline = {'type': "Feature", 'id': key, 'geometry': mapping(geom), 'properties': {'id': key}}
            out.write(json.dumps(newline))
            out.write(',')
        out.write(']}') # add the tail of the FeatureCollection geojson

if __name__ == '__main__':

    ### change below and the centerline distance threshold (line 33)
    ### change src param in line 46 (see: http://geojson.org/geojson-spec.html#coordinate-reference-system-objects)
    input_shp = "ChicagoRiver.shp"
    shply_ply = create_shapes(input_shp)              # run our function to create Shapely multi-polygon geometries
    res_centerlines = generate_centerlines(shply_ply) # create our centerlines
    print("now creating centerlines geojson")
    outgeojs_file = input_shp.strip().split(".")[0]+'_centerlines.geojson'  # define output file name and location
    write_geojson(outgeojs_file, res_centerlines)      # write the output GeoJSON file to disk
