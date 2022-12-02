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