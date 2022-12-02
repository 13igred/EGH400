import numpy as np
import cv2
import os
import json


class Image:
    def __init__(self, img):
        """

        :param img: file path for the new image
        """
        self.img = cv2.imread(img)
        self.value = np.sum(self.img)

    def check(self):
        images = []

        # open the live data of existing images that make up the pano
        folderPath = './LiveData/PanoImage'
        for file in os.listdir(folderPath):
            dictObj = {
                'image': np.load(folderPath + '/' + file),
                'fileName': file
            }
            images.append(dictObj)

        # compare the list of these images to see if the mse is extremely similar
        for img in images:

            # calculate mean square error
            meanSquareError = np.square(np.subtract(self.img, img['image'])).mean()
            # check thresholding values
            if meanSquareError < 40:
                print('[INFO] Matching Image found: ' + img['fileName'])
                print('[INFO] Updating saved image...')
                # np.save(folderPath + '/' + img['fileName'], self.img)
                print('[INFO] Image saved...')

                hozConcat = np.concatenate((self.img, img['image']), axis=1)

                cv2.imshow('HORIZONTAL', hozConcat)
                cv2.waitKey(0)
