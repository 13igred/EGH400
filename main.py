import FlagFind
import ImageStitch
import ImgCompare
import cv2
import os


# path = './data/temp/'
# pano = ImageStitch.InitialisePanorama(path)
# cv2.imshow('title', pano)
# cv2.waitKey(0)

if __name__ == '__main__':
    folderPath = './data/images/'
    for file in os.listdir(folderPath):
        print()
        print('[INFO] Checking Image ' + file)
        image = ImgCompare.Image(folderPath + file)
        image.check()


