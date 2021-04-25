import requests
from os.path import join, isfile, isdir, exists
from os import listdir, makedirs
from tqdm import tqdm
import json 

session = requests.Session()
url = 'https://yf.cognitiveservices.azure.com/vision/v3.0/analyze?visualFeatures=Tags&language=en'
url_obj = 'https://yf.cognitiveservices.azure.com/vision/v3.0/detect'
headers = {
    'content-type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': "YOUR_KEY_HERE",
}

cubemapDir = "../pano-conversion/cubemaps"

def main():
    results = []
    for project in listdir(cubemapDir):
        if isfile(project):
            continue

        results += analyze_project(join(cubemapDir, project))
        
    with open('objects.json', 'w') as f:
        json.dump(results, f)

def analyze_project(dir):
    if not isdir(dir):
        return []
    
    results = []
    for scan in tqdm(listdir(dir)):
        results += analyze_scan(join(dir, scan))
    return results

def analyze_scan(path):
    if ".DS_Store" in path:
        return []
    return [analyze(f) for f in [join(path, n) for n in listdir(path)]]

def analyze(path) -> dict:
    with open(path, 'rb') as f:
        data = f.read()

    img_dict = dict()
    img_dict["filename"] = path
    tags = session.post(url, headers=headers, data=data).json()
    objects = session.post(url_obj, headers=headers, data=data).json()
    img_dict["tags"] = tags["tags"]
    img_dict["objects"] = objects["objects"]
    return img_dict

main()
