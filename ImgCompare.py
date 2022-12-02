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
        count = 0
        for img in images:

            # calculate mean square error
            meanSquareError = np.square(np.subtract(self.img, img['image'])).mean()
            # check thresholding values
            if meanSquareError < 80:
                count += 1
                print('[INFO] Matching Image found: ' + img['fileName'])
                print('[INFO] Updating saved image...')
                np.save(folderPath + '/' + img['fileName'], self.img)
                print('[INFO] Image saved...')

                #scale images
                scalePercent = 60
                width = int(self.img.shape[1] * scalePercent / 100)
                height = int(self.img.shape[0] * scalePercent / 100)
                dim = (width, height)
                width1 = int(img['image'].shape[1] * scalePercent / 100)
                height1 = int(img['image'].shape[0] * scalePercent / 100)
                dim1 = (width1, height1)

                resized = cv2.resize(self.img, dim, interpolation=cv2.INTER_AREA)
                resized1 = cv2.resize(img['image'], dim, interpolation=cv2.INTER_AREA)

                hozConcat = np.concatenate((resized, resized1), axis=1)

                # cv2.imshow('HORIZONTAL', hozConcat)
                # cv2.waitKey(0)
                break
        print('[INFO] Number of matches: ' + str(count))
        if count > 0:
            return True
        else:
            return False
