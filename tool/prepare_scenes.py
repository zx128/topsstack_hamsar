# 20210618, xing

# For given constriants such as
# min_lat = 35.57793709766442
# max_lat = 36.21619047354823
# min_lon = -84.70058767311058
# max_lon = -83.94773267597341
# and
# start_date = "2020-10-01"
# end_date = "2020-10-31"
# and
# track_number = 7
#
# do the following
# (*) search for scenes
# (*) create *.{met,dataset}.json files for each scene found.
# (*) download zip for each scene found.


import os

import json

import osaka.main

from query_asf import query_asf

CONTEXT_FILE_NAME = "_context.json"

QUERY_FILE_NAME = "_query.json"

WORK_DIR_PATH = "."

SCENE_DIR_NAME = "scenes"


"""
    [
      35.707214,
      -86.354156
    ],
    [
      36.110172,
      -83.553978
    ],
    [
      34.489815,
      -83.228645
    ],
    [
      34.085041,
      -85.97142
    ]

      "farEndLat": "36.110172",
      "farEndLon": "-83.553978",
      "farStartLat": "34.489815",
      "farStartLon": "-83.228645",

      "nearEndLat": "35.707214",
      "nearEndLon": "-86.354156",
      "nearStartLat": "34.085041",
      "nearStartLon": "-85.97142",
"""


def create_met_json(sceneMetaData):
    sceneId = sceneMetaData["sceneId"]
    sceneDirPath = os.path.join(WORK_DIR_PATH, SCENE_DIR_NAME, sceneId)
    if not os.path.exists(sceneDirPath):
        os.makedirs(sceneDirPath)
    d = {}
    d["bbox"] = [
            [float(sceneMetaData["nearEndLat"]), float(sceneMetaData["nearEndLon"])],
            [float(sceneMetaData["farEndLat"]), float(sceneMetaData["farEndLon"])],
            [float(sceneMetaData["farStartLat"]), float(sceneMetaData["farStartLon"])],
            [float(sceneMetaData["nearStartLat"]), float(sceneMetaData["nearStartLon"])]
        ]
    metJsonFilePath = os.path.join(sceneDirPath, "{}.met.json".format(sceneId))
    print("create {}".format(metJsonFilePath))
    try:
        with open(metJsonFilePath, 'w') as fout:
            json.dump(d, fout, indent=2)
    except Exception as e:
        raise Exception('unable to write file: %s' % e)


def download_zip(sceneMetaData):
    """https://datapool.asf.alaska.edu/SLC/SA/S1A_IW_SLC__1SDV_20201005T233859_20201005T233926_034668_0409B0_2533.zip"""
    sceneId = sceneMetaData["sceneId"]
    downloadUrl = sceneMetaData["downloadUrl"]
    sceneDirPath = os.path.join(WORK_DIR_PATH, SCENE_DIR_NAME, sceneId)
    if not os.path.exists(sceneDirPath):
        os.makedirs(path)
    print("downloading {} to {}".format(downloadUrl, sceneDirPath))
    osaka.main.get(downloadUrl, sceneDirPath)


def amend_context_file(localizeURLs):
    contextFilePath = os.path.join(WORK_DIR_PATH, CONTEXT_FILE_NAME)
    try:
        with open(contextFilePath, 'r') as fin:
            ctx = json.load(fin)
    except Exception as e:
        raise Exception('unable to read context file: %s' % e)
    ctx["localize_urls"] = localizeURLs
    try:
        with open(contextFilePath, 'w') as fout:
            json.dump(ctx, fout, indent=2)
        return
    except Exception as e:
        raise Exception('unable to write context file: %s' % e)


# select scences from query result file for given track number
def select_scenes(queryFilePath, trackNumberString):
    try:
        with open(queryFilePath, 'r') as fin:
            l = json.load(fin)
            sceneList = l[0] # l is a list of list
    except Exception as e:
        raise Exception('unable to read file: %s' % e)

    if len(sceneList) == 0:
        print("No scene found, quit.")
        return
    
    localizeURLs = []
    for x in sceneList:
        # only look for S1A_IW_SLC__1SDV_*.zip
        if not (x["sceneId"].startswith("S1A_IW_SLC__1SDV_") and x["fileName"].endswith(".zip")):
            continue
        if x["track"] != trackNumberString:
            continue

        create_met_json(x)

        download_zip(x)

        localizeURL = {"local_path": "{0}/{0}.zip".format(x["sceneId"])}
        localizeURLs.append(localizeURL)

    amend_context_file(localizeURLs)


def main():

    #minLat = 35.57793709766442
    #maxLat = 36.21619047354823
    #minLon = -84.70058767311058
    #maxLon = -83.94773267597341
    #snwe = [minLat, maxLat, minLon, maxLon]
    queryFileName = QUERY_FILE_NAME
    #flightDirection = "A"
    flightDirection = None
    #startDate = '2020-10-01'
    #endDate = '2020-10-20'

    # read in parameters from _context.txt
    try:
        contextFilePath = os.path.join(WORK_DIR_PATH, CONTEXT_FILE_NAME)
        with open(contextFilePath, 'r') as fin:
            d = json.load(fin)
    except Exception as e:
        raise Exception('unable to read file: %s' % e)

    minLat = d["min_lat"]
    maxLat = d["max_lat"]
    minLon = d["min_lon"]
    maxLon = d["max_lon"]
    snwe = [minLat, maxLat, minLon, maxLon]
    print("minLat, maxLat, minLon, maxLon: {}, {}, {}, {}".format(minLat, maxLat, minLon, maxLon))
    startDate = d["start_date"]
    endDate = d["end_date"]
    print("startDate, endDate: {}, {}".format(startDate, endDate))
    trackNumberString = "{}".format(d["track_number"])
    print("trackNumberString: {}".format(trackNumberString))

    queryFilePath = os.path.join(WORK_DIR_PATH, queryFileName)
    query_asf(snwe, queryFilePath, flightDirection, output_format='json', sat='Sentinel-1A', beam_mode="IW", processing_level="SLC", start_date=startDate, end_date=endDate)
    print("Query result is in file {}".format(queryFilePath))

    select_scenes(queryFilePath, trackNumberString)


if __name__ == "__main__":
    main()
