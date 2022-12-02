import os
import cv2
import torch
import common.ImageHelper as ImageHelper
import math


def findFlag(folderPath='./data/images/', weightsPath='./runs/train/exp6/weights/best.pt'):
    """
    Finds the location of objects within a folder, accepts a folder and weights to be used

    :param folderPath: string of folder path that contains the images to be checked
    :param weightsPath: string of the weights path that are to be used to find images
    :return: xyxy position of detected objects.
    """

    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weightsPath, force_reload=True)
    model.eval()

    # todo: think of something smart to fix the flag pole height offset
    beachOffset = 80

    for i in os.listdir(folderPath):
        r = model(os.path.join(folderPath, i))

        # load image as open cv image
        img = cv2.imread(os.path.join(folderPath, i))

        pts = []
        # only do this if there are more than 1 flag in frame
        if len(r.pandas().xyxy[0]) > 1:
            swimmerFlag = 0

            # loop over data frame
            for idx, row in r.pandas().xyxy[0].iterrows():

                # find number of swimmer flags
                if row.loc['name'] == 'SwimFlag':
                    swimmerFlag += 1

                    # cast points to an int so that opencv can read them
                    pts.append([int(row.loc['xmin']), int(row.loc['ymin']) + beachOffset])

            # if there are 2 swimmer flags, draw a line between, use for projection purposes.
            if swimmerFlag > 1:
                dimg = ImageHelper.DrawLines(img, pts[0], pts[1])

                # calculate angle for projection
                x = abs(pts[0][0] - pts[1][0])
                y = abs(pts[0][1] - pts[1][1])
                theta = math.degrees(math.atan(y / x))

                # lower proj
                lowY = -100 + pts[1][1]
                lowX = -100 * math.cos(90 - theta) + pts[1][0]
                lowPts = [int(lowX), int(lowY)]

                # high proj
                highY = -100 + pts[0][1]
                highX = 100 * math.cos(theta) + pts[0][0]
                highPts = [int(highX), int(highY)]

                limg = ImageHelper.DrawLines(dimg, pts[1], lowPts, (255, 0, 0))
                himg = ImageHelper.DrawLines(limg, pts[0], highPts, (255, 0, 0))


                ImageHelper.DisplayImage(himg)

    return 'null'