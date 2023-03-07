import common.ImageHelper as ImageHelper
import torch
import torchvision.transforms as transforms
import numpy as np
import cv2

### NOT USED ####
### NOT USED ####
### NOT USED ####
### NOT USED ####
### NOT USED ####


class Image:
    """
    A class ued to detect objects within an image.

    ...

    Attributes
    ----------
    img : numpy
        A cv2 image
    torchModel : pytorch model
        A pytorch model created using predefined weights suited to find flags
    results : pytorch results
        results of the pytorch detection algorithm
    flagLocations: list
        the locations of flags found in the image provided

    Methods
    -------
    detectObject(img)
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
    def __init__(self, img, model):
        """

        :param img: file path for the new image
        """
        self.img = img
        self.torchModel = model
        self.results = self.detectObjects()
        self.flagLocation = self.locateFlags()

    def detectObjects(self):

        expanded = np.expand_dims(self.img, axis=0)
        transposed = np.transpose(expanded, [0, 3, 1, 2])

        # Define a transform to convert
        # the image to torch tensor
        # transform = transforms.ToTensor()
        # tensor = transform.__call__(expanded)

        test = torch.from_numpy(transposed)

        im = cv2.imread('./data/testimg/test1.png')

        return self.torchModel(im)


    def locateFlags(self):
        pts = []
        # loop over data frame
        for idx, row in self.results.pandas().xyxy[0].iterrows():

            # find number of swimmer flags
            if row.loc['name'] == 'SwimFlag':
                # cast points to an int so that opencv can read them
                pts.append([int(row.loc['xmin']), int(row.loc['ymin'])])

        return pts

    def displayDetected(self):
        drawnImg = ImageHelper.DrawCircle(self.img, self.flagLocation)
        ImageHelper.DisplayImage(drawnImg, 'FLAGS DETECTED')
