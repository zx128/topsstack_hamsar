#  20210615, Mohammed Karim

from shapely.geometry import box

import requests


def query_asf(snwe,  output_query_file, flight_direction, output_format='json', sat='Sentinel-1A', beam_mode = "IW", processing_level= "*", start_date='2007-01-01', end_date='2012-01-01'):
    '''
    The function to query the Sentinel-1 archive of Alaska Satellite Facility (ASF)

    print(snwe)
    
    Parameters:
    snwe: a list of coordinates as [south, north, west, east]
    output_query_file: filename for the output jason file
    flight_direction: Ascending / Descending
    output_format='json', 'kml', ...
    sat: the satellite to query (Sentinel-1A or Sentinel-1B, ALOS, etc)
    beam_mode = "IW", FBS, FBD, ...
    processing_level= "L1.0", 
    start_date: start date e.g., '2007-01-01', 
    end_date: end date e.g., '2012-01-01'
    
    Check ASF api for more parameters: https://asf.alaska.edu/api/
    
    '''
    print('Querying ASF Vertex...')
    miny, maxy, minx, maxx = snwe
    roi = box(minx, miny, maxx, maxy)
    polygonWKT = roi.to_wkt()

    baseurl = 'https://api.daac.asf.alaska.edu/services/search/param'
    data=dict(intersectsWith=polygonWKT,
            platform=sat,
            #processingLevel=processing_level,
            #beamMode=beam_mode,
            start = start_date,
            end = end_date,
            flightDirection=flight_direction,
            output=output_format)

    r = requests.get(baseurl, params=data)
    #print(r.text)
    with open(output_query_file, 'w') as j:
        j.write(r.text)

    return None


def main():
    MINLAT = 35.57793709766442
    MAXLAT = 36.21619047354823
    MINLON = -84.70058767311058
    MAXLON = -83.94773267597341
    snwe = [MINLAT, MAXLAT, MINLON, MAXLON]
    output_query_file = "ascending.json"
    flight_direction = "A"
    sat = 'Sentinel-1A'
    beam_mode = "IW"
    processing_level = "*"
    #start_date = '2015-03-15'
    start_date = '2020-10-01'
    #end_date = '2016-04-15'
    end_date = '2020-11-01'

    #query_asf([MINLAT, MAXLAT, MINLON, MAXLON],  "Ascending.json", "A", sat='Sentinel-1A', beam_mode = "*", processing_level="*", start_date='2015-03-15', end_date='2016-04-15')
    #query_asf(snwe,  output_query_file, flight_direction, output_format='json', sat='Sentinel-1A', beam_mode = "IW", processing_level= "*", start_date='2007-01-01', end_date='2012-01-01'):
    query_asf(snwe,  output_query_file, flight_direction, output_format='json', sat=sat, beam_mode=beam_mode, processing_level=processing_level, start_date=start_date, end_date=end_date)


if __name__ == "__main__":
    main()
