import ImageStitch
import cv2
import os
import numpy
from sewar.full_ref import mse
import time

def loadImages():
    """
    Loads the composite images that make up the current panorama

    :return: an array containing the current images
    """
    images = []
    folderPath = './LiveData/PanoImg/'
    for file in os.listdir(folderPath):
        images.append(numpy.load(folderPath + file))
    return images


class Panorama:
    """
    A class ued to build a panoramic image

    ...

    Attributes
    ----------
    panoramaImage : list
        An array housing the built panoramas, technically an array of numpy[]
    compositeImages : list
        An array housing the images that built each panorama, technically an array of numpy[]
    imageBuffer : list
        An array housing all the images that are to be used to build the initial panorama

    Methods
    -------
    addImageToBuffer(img)
        Adds the input image to the classes image buffer

    createPanorama()
        Stitches together images to create the panorama

    compareUpdate(filePath, panoramaIndex)
        Compares a given image to each of the images in the panorama composite array

    updatePanorama(panoramaIndex)
        Updates the panorama with the compositeImages

    displayPanorama(timeDelay=0)
                Displays the panoramic image, exit display by pressing 'any' key

    savePanorama(filePath=None)
            Saves the panorama in the specified file locaiton or in a default locations

    """
    def __init__(self):
        """
        Initialise the panorama class

        """

        self.panoramaImage = []
        self.compositeImages = []
        self.imageBuffer = []

    def addImageToBuffer(self, img):
        """
        Adds the input image to the classes image buffer

        Parameters
        ----------
        img : numpy
            A cv2 image
        """
        self.imageBuffer.append(img)

    def createPanorama(self):
        """
        Stitches together images to create the panorama
        """
        splitImages = []

        if len(self.imageBuffer) > 20:
            panoList = []

            idx = 0
            jdx = 1
            bufferSize = 0
            while jdx < len(self.imageBuffer):
                # check first image with images in buffer for similarities
                if not checkMSE(self.imageBuffer[idx], self.imageBuffer[jdx]):
                    # the first image checked is no longer similar to the current checked image
                    # in this case we move the first image to the current image
                    idx = jdx
                    jdx += 1

                    # check the next image with the new first image
                    if checkMSE(self.imageBuffer[idx], self.imageBuffer[jdx]):
                        # if its similar enough we continue checking
                        jdx += 1
                    else:
                        # we have determined a block of images store them and this will be used to create a mini panorama.
                        if jdx - bufferSize > 10:
                            for i in range(bufferSize, jdx + 1):
                                panoList.append(self.imageBuffer[i])
                            splitImages.append(panoList)
                            idx = jdx
                            jdx += 1
                            bufferSize = len(panoList)
                            # reset pano list
                            panoList = []
                else:
                    jdx += 1

            # check if all images were similar enough.
            if bufferSize == 0:
                splitImages.append(self.imageBuffer)

            for images in splitImages:
                tempPano, tempComp = ImageStitch.InitialisePanorama(images)
                self.panoramaImage.append(tempPano)
                self.compositeImages.append(tempComp)
            return True
        else:
            print("[ERROR] Not enough images in the buffer.")
            return False

    def compareUpdate(self, image):
        """
        Compares a given image to each of the images in the panorama composite array

        Parameters
        ----------
        image : numpy
            A cv2 image
        """

        minMse = 100000
        minIdx = -1
        for arrIdx, imgArray in enumerate(self.compositeImages):
            for imgIdx, img in enumerate(imgArray):
                mseValue = mse(img, image)
                # calculate the image that has the lowest mse, or is the most similar to the current buffer
                if mseValue < minMse:
                    minMse = mseValue
                    minIdx = imgIdx
            print('[INFO] MSE: ' + str(minMse))
            print('[INFO] IDX: ' + str(minIdx))
            # if the images are similar enough, update  internal register
            if minMse < 1500:
                self.compositeImages[arrIdx][minIdx] = image
                return True, arrIdx, minIdx
            else:
                return False, -1, -1

    def updatePanorama(self):
        """
        Generatess a panoramic image based on images in the internal buffer

        """
        for panoramaIndex, _ in enumerate(self.panoramaImage):
            self.panoramaImage[panoramaIndex], self.compositeImages[panoramaIndex] = ImageStitch.imageStitchNoCheck(self.compositeImages[panoramaIndex])

    def displayPanorama(self, timeDelay=0):
        """
        Displays the panoramic image, exit display by pressing 'any' key

        Parameters
        ----------
        timeDelay: int
            specify time delay image is shown for in mS, default is displayed until key press
        """
        for img in self.panoramaImage:
            cv2.imshow('PANORAMA', img)
            cv2.waitKey(timeDelay)
            cv2.destroyAllWindows()


    def savePanorama(self, path=None):
        """
        Saves the panorama in the specified file locaiton or in a default locations

        """

        for idx, img in enumerate(self.panoramaImage):
            if not path:
                defPath = './LiveData/CompletedPano/'

            fileName = str(time.time()) + '_' + str(idx) + '.png'
            cv2.imwrite(defPath + fileName, img)


def checkMSE(image1, image2, th1=2700, th2=0):
    """
    Compares the difference between two images, returns true if over a threshold

    :param image1: a cv2 img
    :param image2: a cv2 img
    :param th1: upper threshold limit
    :param th2: lower threshold limit
    :return: bool
    """

    test = mse(image1, image2)
    print(test)
    if th1 >= test >= th2:
        return True
    else:
        return False