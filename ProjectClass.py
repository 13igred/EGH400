import common.ImageHelper as ImageHelper
import math


class Project:
    def __init__(self, x1, y1, x2, y2, image):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.image = image
        self.middle = []

    def calculate(self):
        pt1 = 0
        pt2 = 0

        if len(self.x1) == 2:
            # find middle points
            for idx, _ in enumerate(self.x1):
                self.middle.append([int(self.x1[idx] + (self.x2[idx] - self.x1[idx])), int(self.y1[idx] - (self.y1[idx] - self.y2[idx]))])

            # calculate angle between both flags

            # find x lenght and y length between flags
            xLen = abs(self.middle[0][0] - self.middle[1][0])
            yLen = abs(self.middle[0][1] - self.middle[1][1])
            # angle between flags
            theta = math.atan(yLen / xLen)


            # projection angle of flag one
            if yLen / xLen < 0.5:
                # normal perspective
                thetaFlagOne = math.pi/2 - theta
                # projection angle of flag two
                thetaFlagTwo = -math.pi/2 + theta
            else:
                # Left of Image
                thetaFlagOne = math.pi - theta + math.pi / 4
                # projection angle of flag two
                thetaFlagTwo = -math.pi + theta - math.pi / 4

            # find proj points
            projLen = 400
            projX1 = projLen * math.cos(thetaFlagOne)
            projY1 = projLen * math.sin(thetaFlagOne)
            projX2 = projLen * math.cos(thetaFlagTwo)
            projY2 = projLen * math.sin(thetaFlagTwo)

            # calculate image positions
            pt1 = (int(self.middle[0][0] - projX1), int(self.middle[0][1] - projY1))
            pt2 = (int(self.middle[1][0] - projX2), int(self.middle[1][1] + projY2))

        else:
            print('[ERROR] Incorrect number of flags detected')
            return -1, -1, False

        return pt1, pt2, True

    def markup(self):
        if len(self.middle) == 2:
            markupImage = ImageHelper.drawLine(self.image, self.middle[0], self.middle[1])
            ImageHelper.DisplayImage(markupImage, 'MARKUP IMAGE')
        else:
            print('[ERROR] incorrect number of flags detected.')

    def drawMarkup(self, pt1, pt2, display):
        if len(self.middle) == 2:
            markupImage = ImageHelper.drawLine(self.image, self.middle[0], pt1)
            markupImage = ImageHelper.drawLine(self.image, self.middle[1], pt2)
            if display:
                ImageHelper.DisplayImage(markupImage, 'MARKUP IMAGE')

            return markupImage
        else:
            return self.image
