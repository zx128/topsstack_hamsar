import json

import os

#import osaka
import osaka.main


'''
Function : download_slc
Input : slc_id, location where SLC to be downloaded
Purpose : Download the SLC
Returns : None
'''
#def download_slc(slc_id, path):
def download_slc(url, path):
    #url = "https://datapool.asf.alaska.edu/SLC/SA/{}.zip".format(slc_id)
    #print("Downloading {} : {} to {}".format(slc_id, url, path))
    
    if not os.path.exists(path):
        os.makedirs(path)
    osaka.main.get(url, path)


query_result_file = "ascending.json"

with open("ascending.json", "r") as fr:
    data = json.load(fr)

slc_list = []

#print(data[0])
for d in data[0]:
    if 'downloadUrl' in d:
        if d['downloadUrl'].endswith(".zip") and 'SLC' in d['downloadUrl']:
            slc_list.append(d['downloadUrl'])
            print(d['downloadUrl'])
#
print(slc_list)

dir_path = "zip"
for x in slc_list:
    print(x)
    download_slc(x, dir_path)
