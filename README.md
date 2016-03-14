# centerline
Generate geojson centerlines for network-like polygons (e.g. polygon rivers and streets) with Python/scipy.spatial/OGR-shapely - based on the centerline script from python-geospatial-analysis-cookbook (https://github.com/mdiener21/python-geospatial-analysis-cookbook/tree/master/ch08/code). The downloaded scripts were modified to make it work with my shapefiles.

Result (would probably need cleaning but this will be a good start):

rasterRivers_centerline.geojson: centerlines extracted from river networks shapefiles which was based on satelite-imagery-base raster data (see rasterRivers.zip).

ChicagoRiver_centerline.geojson: centerline extracted from Chicago river network based on Hydro file from the Chicago Data Portal (see ChicagoRiver.zip)

References:

python-geospatial-analysis-cookbook: https://github.com/mdiener21/python-geospatial-analysis-cookbook/tree/master/ch08/code

Base idea about the process: https://commons.wikimedia.org/wiki/File:Voronoi_centerlines_skeleton.gif

About geojson specs: http://geojson.org/geojson-spec.html

This was helpful in writing geojson: http://www.andrewdyck.com/how-to-convert-csv-data-to-geojson/

