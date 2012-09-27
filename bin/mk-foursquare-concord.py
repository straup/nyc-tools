#!/usr/bin/env python

import sys
import json
import csv
import urllib
import urllib2
import pprint
from fuzzywuzzy import fuzz
import random

token = ''

def search(station):

    geom = station['geometry']
    coords = geom['coordinates']
    ll = "%s,%s" % (coords[1], coords[0])

    props = station['properties']
    name = "%s (%s)" % (props['name'], props['line'])

    endpoint = 'https://api.foursquare.com/v2/venues/search'

    args = {
        'oauth_token' : token,
        'll': ll,
        'radius': 500,
        'categoryId': '4bf58dd8d48988d129951735',	# trains/subways
        'intent': 'browse',
        'query': 'MTA',
        }

    url = endpoint + '?' + urllib.urlencode(args)

    rsp = urllib2.urlopen(url)
    data = json.load(rsp)

    response = data['response']
    groups = response['groups'][0]
    items = groups['items']

    if len(items) == 0:
        return (station['id'], '', name, '', 0)

    for v in items:

        r = fuzz.partial_ratio(v['name'], name)

        row = (
            station['id'],
            v['id'],
            name,
            v['name'],
            r
            )

        return row

if __name__ == '__main__':

    input = sys.argv[1]		# geojson
    output = sys.argv[2]	# csv

    fh = open(input, 'r')
    data = json.load(fh)
    fh.close()

    fh = open(output, 'w')
    writer = csv.writer(fh)

    writer.writerow(('id', 'foursquare:id', 'name', 'foursquare:name', 'fuzzywuzzy:match'))

    for f in data['features']:

        row = search(f)
        print row
        writer.writerow(row)

    fh.close()
