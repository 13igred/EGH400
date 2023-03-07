import common.ImageHelper as ImageHelper
import torch
import torchvision.transforms as transforms
import numpy as np
import cv2

class Image:
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
