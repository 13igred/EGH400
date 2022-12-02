import FlagFind
import ImageStitch
import ImgCompare
import cv2
import os
import time


path = './data/temp/'
pano = ImageStitch.InitialisePanorama(path)
# cv2.imshow('title', pano)
# cv2.waitKey(0)

folderPath = './data/images/'
count = 0
for file in os.listdir(folderPath):
    print()
    print('[INFO] Checking Image ' + file)
    image = ImgCompare.Image(folderPath + file)
    if image.check():
        count += 1
        if count % 20 == 0:
            pano = ImageStitch.LoadNumpy()
            cv2.imshow('Panorama', pano)
            key = cv2.waitKey(100)  # pauses for 2 seconds before fetching next image

if __name__ == '__main__':
    pass


