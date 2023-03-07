import common.ImageHelper as ImageHelper
import torch
import torchvision.transforms as transforms
import numpy as np
import cv2

class Detector:
    def __init__(self, weightsPath):
        """

        :param weightsPath: [String] File location of the YOLOv5 weights for the model.
        """

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weightsPath, force_reload=True).eval()

    def detect(self, image):
        """
        Given an image will detect objects and return an array of x,y locations of those objects

        :param image: [numpy] cv2 image
        :return: [array] x,y locations
        """

        # fix colour from BGR to RGB
        colourFixedImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # get prediction results
        results = self.model(colourFixedImage)

        cords = results.pandas().xyxy[0]

        # define box corners
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        for idx, row in results.pandas().xyxy[0].iterrows():
            if row['name'] == 'SwimFlag' and row['confidence'] > 0.6:
                x1.append(row['xmin'])
                y1.append(row['ymin'])
                x2.append(row['xmax'])
                y2.append(row['ymax'])

        return x1, y1, x2, y2

    def markup(self, image, x1, y1, x2, y2, display):
        """
        Given x,y points, a cv2 image and a boolean for display.
        This will markup the image with the locations and display the image

        :param location: [array] x,y points
        :param image: [numpy] cv2 image
        :param display: [boolean]
        """

        for idx, _ in enumerate(x1):
            markupImg = ImageHelper.drawBoundaryBox(image, x1[idx], y1[idx], x2[idx], y2[idx], idx)

        if display:
            ImageHelper.DisplayImage(markupImg, 'FLAGS DETECTED')

        return markupImg
