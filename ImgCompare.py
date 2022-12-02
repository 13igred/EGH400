import numpy as np
import cv2
import os
import json


class Image:
    def __init__(self, img):
        """

        :param img: file path for the new image
        """
        self.img = img
        self.value = np.sum(self.img)

    def check(self):
        images = []

        # open the live data of existing images that make up the pano
        folderPath = './LiveData/PanoImg'
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
            if meanSquareError < 60:
                print('[INFO] Matching Image found: ' + img['fileName'])
                print('[INFO] Updating saved image...')
                np.save(folderPath + '/' + img['fileName'], self.img)
                print('[INFO] Image saved...')


img = cv2.imread('./data/images/scene02041.png')
i = Image(img)
i.check()

# path = './LiveData/PanoImg/test3'
#
# # when we open the image we will save is as such
# dictionary = {
#     'image': img,
#     'fileName': path
# }
#
# np.save(dictionary['fileName'], img)
