import cv2
import torch
import common.ImageHelper as ImageHelper

class Detector:
    """
    A class ued to detect flags in an image

    ...

    Attributes
    ----------
    model : pytorch model
        A pytorch model created using predefined weights suited to find flags

    Methods
    -------
    detect(image)
        Given an image will detect objects and return an array of x,y locations of those objects

    markup(image, x1, y1, x2, y2, display)
        Given x,y points, a cv2 image and a boolean for display.
        This will draw a box around the points, and display the image if true
    """

    def __init__(self, weightsPath):
        """
        Parameters
        ----------
        weightsPath: str
            File location of the YOLOv5 weights for the model.
        """

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weightsPath, force_reload=True).eval()

    def detect(self, image):
        """
        Given an image will detect objects and return an array of x,y locations of those objects

        Parameters
        ----------
        image: numpy
            cv2 image
        Return
        ------
        x1 : int
            locations that flags were detected
        y1 : int
            locations that flags were detected
        x2 : int
            locations that flags were detected
        y2 : int
            locations that flags were detected
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
        This will draw a box around the points, and display the image if true

        Parameters
        ----------
        image: numpy
            cv2 image
        x1: int
            location of flag detected
        y1: int
            location of flag detected
        x2: int
            location of flag detected
        y2: int
            location of flag detected
        display: bool
            True if image should be displayed

        Return
        ------
        markup : numpy
            cv2 image with markup drawn
        """

        for idx, _ in enumerate(x1):
            markupImg = ImageHelper.drawBoundaryBox(image, x1[idx], y1[idx], x2[idx], y2[idx], idx)

        if display:
            ImageHelper.DisplayImage(markupImg, 'FLAGS DETECTED')

        return markupImg
