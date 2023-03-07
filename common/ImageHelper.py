import cv2
import numpy as np

def DrawLines(image, pointA, pointB, colour=(0,0,255)):
    '''
    Draw a line between one point and one/many points

    :param image: OpenCv2 image
    :param pointA: starting point for the line
    :param points: points to be drawn to
    :return: a OpenCV2 image that has been drawn on
    '''

    thickness = 2

    cv2.line(image, pointA, pointB, colour, thickness)

    return image


def DisplayImage(image, title='Display Image'):
    """
    Display the image in a new window
    Can be resized if given new window dimensions

    :param image: provided a cv2 image
    :param title: provide a string title
    """

    cv2.imshow(title, image)
    cv2.waitKey(0)

def DrawCircle(img, pointsArray, xOff=0, yOff=0):
    """
    Draws a Circle on the image provided at the points provided.

    :param pointsArray: List contain the points that are to be drawn
    :param xOff: x offset of the template
    :param yOff: y offset of the template
    :param img: a cv2 img

    :return: the resized image with the circles drawn
    """

    for points in pointsArray:
        x = int(points[0] + (xOff / 2))
        y = int(points[1] + (yOff / 2))

        cv2.circle(img, (x, y), 5, (0, 255, 0), 2)

    return img


def drawLine(img, pt1, pt2):
    colour = (0, 0, 255)
    thickness = 2
    cv2.line(img, pt1, pt2, colour, thickness)
    return img


def drawBoundaryBox(img, x1, y1, x2, y2, idx):
    """
    Draws a boundary box between the specified points

    :param img:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    """

    pt1 = (int(x1), int(y1))
    pt2 = (int(x2), int(y1))
    pt3 = (int(x1), int(y2))
    pt4 = (int(x2), int(y2))

    colour = (0, 0, 255)
    thickness = 2
    cv2.putText(img, str(idx), (pt1[0], pt1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    cv2.line(img, pt1, pt2, colour, thickness)
    cv2.line(img, pt1, pt3, colour, thickness)
    cv2.line(img, pt3, pt4, colour, thickness)
    cv2.line(img, pt2, pt4, colour, thickness)

    return img
