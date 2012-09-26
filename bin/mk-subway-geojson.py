#!/usr/bin/env python

# TODO
# - get foursquare ID for subway stations
# - get WOE neighbourhood id
# - check for source file (reuse artisanal integers)
# - generate bounding box (based on points)
# - use options and __main__

import sys
import csv
import json
import ArtisinalInts

input = sys.argv[1]
output = sys.argv[2]

fh = open(input, 'U')
reader = csv.DictReader(fh)

features = []

for row in reader:

    id, ignore = ArtisinalInts.get_brooklyn_integer()

    # sigh...

    pt = row['Shape'].strip()
    pt = pt.lstrip("(")
    pt = pt.rstrip(")")
    lat, lon = map(float, pt.split(","))

    geom = {
        'type': 'Point',
        'coordinates': [lon, lat]
        }

    props = {
        'name': row['NAME'],
        'line': row['LINE'],
        'nyc:id': row['OBJECTID'],
        'artisanal:id': id,
        'artisanal:provider': 'http://www.brooklynintegers.com/',
        }

    station = {
        'type': 'Feature',
        'geometry': geom,
        'properties': props,
        'id': id
        }

    features.append(station)
    print station

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

out = open(output, 'w')
json.dump(geojson, out, indent=2)
