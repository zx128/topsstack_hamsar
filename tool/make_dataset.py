# 20210525, Karim
# extracted from utils.py and create_dateset.py in old
# https://github.com/aria-jpl/topsstack

import os
import json
import re
import shutil
from datetime import datetime
import argparse

SLC_SCENES = []

def create_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-b', '--bbox_str', default="", help="poly string including 'POLYGON((*))'")
    args = parser.parse_args()

    return args

def get_union_polygon_from_bbox(env):
    if not isinstance(env, list):
        env = env.split()
    env = [float(i) for i in env] 
    coords = [
        [ env[3], env[0] ],
        [ env[3], env[1] ],
        [ env[2], env[1] ],
        [ env[2], env[0] ],
        [ env[3], env[0] ]
    ]
    return {
        "type": "polygon",
        "coordinates": [ coords ]
    }

def get_dataset_met_json_files(cxt):
    """
    returns 2 lists: file paths for dataset.json files and met.json files
    :param cxt: json from _context.json
    :return: list[str], list[str]
    """
    pwd = os.getcwd()
    localize_urls = cxt['localize_urls']

    met_files, ds_files = [], []
    for localize_url in localize_urls:
        local_path = localize_url['local_path']
        slc_id = local_path.split('/')[0]
        slc_path = os.path.join(pwd, slc_id, slc_id)

        ds_files.append(slc_path + '.dataset.json')
        met_files.append(slc_path + '.met.json')
    return ds_files, met_files

"""
    Function: get_min_max_timestamps
    returns the min timestamp and max timestamp of the stack
    :param scenes_ls: list[str] all slc scenes in stack
    :return: (str, str) 2 timestamp strings, ex. 20190518T161611
"""
def get_min_max_timestamps(scenes_ls):
    
    timestamps = set()

    regex_pattern = r'(\d{8}T\d{6}).(\d{8}T\d{6})'
    for scene in scenes_ls:
        matches = re.search(regex_pattern, scene)
        if not matches:
            raise Exception("regex %s was unable to match with SLC id %s" % (regex_pattern, scene))

        slc_timestamps = (matches.group(1), matches.group(2))
        timestamps = timestamps.union(slc_timestamps)

    #min_timestamp = "{}Z".format(datetime.strptime(min(timestamps), "%Y%m%dT%H%M%S").isoformat())
    #max_timestamp = "{}Z".format(datetime.strptime(max(timestamps), "%Y%m%dT%H%M%S").isoformat())
    
    return min(timestamps), max(timestamps)

def get_min_max_times(scenes_ls):
    """
    returns the min timestamp and max timestamp of the stack
    :param scenes_ls: list[str] all slc scenes in stack
    :return: (str, str) 2 timestamp strings, ex. 20190518T161611
    """
    timestamps = set()

    regex_pattern = r'(\d{8}T\d{6}).(\d{8}T\d{6})'
    for scene in scenes_ls:
        matches = re.search(regex_pattern, scene)
        if not matches:
            raise Exception("regex %s was unable to match with SLC id %s" % (regex_pattern, scene))

        slc_timestamps = (matches.group(1), matches.group(2))
        timestamps = timestamps.union(slc_timestamps)

    #min_timestamp = min(timestamps)
    #max_timestamp = max(timestamps)
    min_timestamp = "{}".format(datetime.strptime(min(timestamps), "%Y%m%dT%H%M%S").isoformat())
    max_timestamp = "{}".format(datetime.strptime(max(timestamps), "%Y%m%dT%H%M%S").isoformat())
    
    return min_timestamp, max_timestamp

'''
Function : generate_dataset_json_data
Input : ctx, version
Purpose : information needed to create datasets.json
Returns : dataset dictionary
'''
def generate_dataset_json_data(scenes, bbox, version):
    """
    :param cxt: _context.json file
    :param dataset_json_files: list[str] all file paths of SLC's .dataset.json files
    :param version: str: version, ex. v1.0
    :return: dict
    """
    dataset_json_data = dict()
    dataset_json_data['version'] = version

    
    try:      
        dataset_json_data['starttime'], dataset_json_data['endtime']  = get_min_max_times(scenes)      
    except Exception as err:
        print(str(err))
  
    try:
        dataset_json_data['location'] = get_union_polygon_from_bbox(bbox)
    except Exception as err:
        print(str(err))

    return dataset_json_data

'''
Function : generate_met_json_data
Input : ctx, bbox, version
Purpose : information needed to create met.json
Returns : metadata dictionary
'''
def generate_met_json_data(scenes, bbox, version):
    """
    :param cxt: _context.json file
    :param met_json_file_paths: list[str] all file paths of SLC's .met.json files
    :param dataset_json_files: list[str] all file paths of SLC's .dataset.json files
    :param version: str: version, ex. v1.0
    :return: dict
    """
    met_json_data = {
        'processing_start': '{}'.format(os.environ['PROCESSING_START']),
        'processing_stop': '{}'.format(datetime.utcnow().isoformat()),
        'version': version
    }

    # generating bbox
    geojson = get_union_polygon_from_bbox(bbox)
    coordinates = geojson['coordinates'][0]
    for coordinate in coordinates:
        coordinate[0], coordinate[1] = coordinate[1], coordinate[0]
    
    met_json_data['bbox'] = bbox
    
    # list of SLC scenes
   
    met_json_data['scenes'] = scenes
    met_json_data['scene_count'] = len(scenes)

    # getting timestamps

    met_json_data['sensing_start'], met_json_data['sensing_stop']  = get_min_max_times(scenes)

    # additional information
    met_json_data['dataset_type'] = 'topsStack_hamsar'

    return met_json_data

'''
Function : read_context
Input : context file
Purpose : Utility function to read the context file and generate a json dict
Returns : json dict of context
''' 
def read_context(ctx_file='_context.json'):
    with open(ctx_file, 'r') as f:
        cxt = json.load(f)
        return cxt

'''
Function : create_dataset
Input : bounding box
Purpose : Utility function to create topsStack product including dataset.json, met.json and copying all the appropriate files in product dir
Returns : product directory (product id)
''' 
def create_dataset(bbox):
    VERSION = 'v1.0'
    DATASET_NAMING_TEMPLATE = 'coregistered_slcs-{min_timestamp}-{max_timestamp}'
    PWD = os.getcwd()

    # creating list of all SLC .dataset.json and .met.json files
    ctx = read_context()
    scenes = []
    for x in ctx["localize_urls"]:
        scenes.append(x["local_path"].split("/")[0])
    #dataset_json_files, met_json_files = get_dataset_met_json_files(ctx)


    # getting list of SLC scenes and extracting min max timestamp
    min_timestamp, max_timestamp = get_min_max_timestamps(scenes)

    # creatin dataset directory
    dataset_name = DATASET_NAMING_TEMPLATE.format(min_timestamp=min_timestamp, max_timestamp=max_timestamp)
    if not os.path.exists(dataset_name):
        os.mkdir(dataset_name)

    # move merged/ master/ slaves/ directory to dataset directory
    move_directories = ['merged', 'reference', 'secondarys']
    for directory in move_directories:
        shutil.move(directory, dataset_name)

    # move _stdout.txt log file to dataset
    shutil.copyfile('_stdout.txt', os.path.join(dataset_name, '_stdout.txt'))

    # generate .dataset.json data
    dataset_json_data = {}
    try:
        dataset_json_data = generate_dataset_json_data(scenes, bbox, VERSION)
    except Exception as err:
        print(str(err))
    dataset_json_data['label'] = dataset_name
    print(json.dumps(dataset_json_data, indent=2))

    # generate .met.json data
    met_json_data = generate_met_json_data(scenes, bbox, VERSION)
    print(json.dumps(met_json_data, indent=2))

    # writing .dataset.json to file
    dataset_json_filename = os.path.join(PWD, dataset_name, dataset_name + '.dataset.json')
    with open(dataset_json_filename, 'w') as f:
        json.dump(dataset_json_data, f, indent=2)

    # writing .met.json to file
    met_json_filename = os.path.join(PWD, dataset_name, dataset_name + '.met.json')
    with open(met_json_filename, 'w') as f:
        json.dump(met_json_data, f, indent=2)

if __name__ == "__main__":
    #bbox = "34.6002832 34.6502392 -79.0801608 -78.9705888"
    inps = create_parser()
    print(inps)
    bbox = inps.bbox_str.split(" ")

    #bbox = "{} {} {} {}".format(MINLAT, MAXLAT, MINLON, MAXLON)
    create_dataset(bbox)
