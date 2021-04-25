from image_slicer import slice
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists
from tqdm import tqdm

cubemapDir = "cubemaps"

def main():
    for d in listdir(cubemapDir):
        if isfile(d):
            continue     
        split_project(join(cubemapDir, d))

def split_project(dir):
    if not isdir(dir):
        return
    
    for scan in tqdm(listdir(dir)):
        split_image(join(dir, scan))

def split_image(path):
    if ".DS_Store" in path:
        return
    
    names = ["front.png", "right.png", "back.png", "left.png"]
    outputs = [join(path, n) for n in names]
    for f in outputs:
        slice(f, 2)

main()
