from vrProjector.vrProjector import EquirectangularProjection, CubemapProjection
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm

source = EquirectangularProjection()
out = CubemapProjection()

panoramaDir = "panoramas"
cubemapDir = "cubemaps"
cubemapSize = 512

def main():
    for d in listdir(panoramaDir):
        cubemapify_project(join(panoramaDir, d))

def cubemapify_project(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    for f in tqdm(files):
        cubemapify_panorama(join(dir, f))

def cubemapify_panorama(path):
    source.loadImage(path)

    out.initImages(cubemapSize, cubemapSize)
    out.reprojectToThis(source)

    outDir = path.replace(panoramaDir, cubemapDir)
    if not exists(outDir):
        makedirs(outDir)

    names = ["front.png", "right.png", "back.png", "left.png", "top.png", "bottom.png"]
    outputs = [join(outDir, n) for n in names]
    out.saveImages(*outputs)

main()
