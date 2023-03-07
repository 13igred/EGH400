import os
import time
import cv2
import imutils
import numpy
import numpy as np
from sewar.full_ref import mse


def InitialisePanorama(images):
    """
    Builds a panorama image

    :param path: file path where the array of images is kept
    :return returns the panoramic openCV image
    """
    pano, compositeImg = imageStitch(images)

    return pano, compositeImg


# def LoadNumpy():
#     folderPath = './LiveData/PanoImage/'
#     imgs = []
#     for file in os.listdir(folderPath):
#         imgs.append(numpy.load(folderPath + file))
#
#     return imageStitchNoCheck(imgs)


def imageStitch(imgIn):
    """
    Compares the imgIn images and cleans up bulk data for panoramic stitching

    :param imgIn: a openCV image array
    :return: returns the panoramic openCV image
    """
    start = time.time()
    print('[INFO] Image comparison starting with ' + str(len(imgIn)) + ' images')
    images = []
    for index, i in enumerate(imgIn):
        imgDict = {
            'id': index,
            'img': i
        }
        images.append(imgDict)

    # What a fucking mess
    imgs = []
    first = True
    second = True
    for i in range(len(images)):
        if i + 1 < len(images):
            # check for differences in images # Base numbers are 2000 and 1300
            if imageDifference(images[i]['img'], images[i + 1]['img'], 2000, 700):
                if imgs:
                    for j in imgs:
                        if j['id'] == images[i]['id']:
                            first = False
                        if j['id'] == images[i + 1]['id']:
                            second = False
                    if first:
                        imgs.append(images[i])
                    if second:
                        imgs.append(images[i + 1])
                else:
                    imgs.append(images[i])
                    imgs.append(images[i + 1])
        first = True
        second = True
    # unpack dict
    stitchImgs = []
    for i in imgs:
        stitchImgs.append(i['img'])

    end = time.time()
    print('[INFO] Image comparison complete.\nTime Taken: ' + str((round((end - start), 6))) + " [s]")

    pano, compositeImg = ImageStitch(stitchImgs)

    return pano, compositeImg


def imageStitchNoCheck(imgIn):
    """
    Compares the imgIn images and cleans up bulk data for panoramic stitching

    :param imgIn: a openCV image array
    :return: returns the panoramic openCV image
    """
    start = time.time()
    print('[INFO] Image comparison starting with ' + str(len(imgIn)) + ' images')
    images = []
    for index, i in enumerate(imgIn):
        imgDict = {
            'id': index,
            'img': i
        }
        images.append(imgDict)

    # What a fucking mess
    imgs = []
    first = True
    second = True
    for i in range(len(images)):
        if i + 1 < len(images):
                if imgs:
                    for j in imgs:
                        if j['id'] == images[i]['id']:
                            first = False
                        if j['id'] == images[i + 1]['id']:
                            second = False
                    if first:
                        imgs.append(images[i])
                    if second:
                        imgs.append(images[i + 1])
                else:
                    imgs.append(images[i])
                    imgs.append(images[i + 1])
        first = True
        second = True
    # unpack dict
    stitchImgs = []
    for i in imgs:
        stitchImgs.append(i['img'])

    end = time.time()
    print('[INFO] Image comparison complete.\nTime Taken: ' + str((round((end - start), 6))) + " [s]")

    return ImageStitch(stitchImgs)



def ImageStitch(images):
    """
    Performs panoramic image stitching.
    Additional Info at: https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/

    :param images: an array of cv2 images
    :return: a stitched cv2 image
    """
    start = time.time()
    # initialize OpenCV's image sticher object and then perform the image
    # stitching
    print("[INFO] stitching " + str(len(images)) + " images...")

    # save images that are going to be stitched
    # folderPath = './LiveData/PanoImg/'
    # for idx, img in enumerate(images):
    #     np.save(folderPath + str(idx), img)

    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)

    # if the status is '0', then OpenCV successfully performed image
    # stitching
    if status == 0:
        # create a 10 pixel border surrounding the stitched image
        # unclear what this does, but it break if i disable it
        stitched = cv2.copyMakeBorder(stitched, 2, 2, 2, 2,
                                      cv2.BORDER_CONSTANT, (0, 0, 0))

        # convert the stitched image to grayscale and threshold it
        # such that all pixels greater than zero are set to 255
        # (foreground) while all others remain 0 (background)
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        # find all external contours in the threshold image then find
        # the *largest* contour which will be the contour/outline of
        # the stitched image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # allocate memory for the mask which will contain the
        # rectangular bounding box of the stitched image region
        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # create two copies of the mask: one to serve as our actual
        # minimum rectangular region and another to serve as a counter
        # for how many pixels need to be removed to form the minimum
        # rectangular region
        minRect = mask.copy()
        sub = mask.copy()

        # keep looping until there are no non-zero pixels left in the
        # subtracted image
        while cv2.countNonZero(sub) > 0:
            # erode the minimum rectangular mask and then subtract
            # the thresholded image from the minimum rectangular mask
            # so we can count if there are any non-zero pixels left
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)

        # find contours in the minimum rectangular mask and then
        # extract the bounding box (x, y)-coordinates
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)

        # use the bounding box coordinates to extract the our final
        # stitched image
        stitched = stitched[y:y + h, x:x + w]

        end = time.time()
        print('[INFO] Stitching complete.\nTime Taken: ' + str((round((end - start), 6))) + " [s]")

        return stitched, images

        # write the output stitched image to disk
        # display the output stitched image to our screen
        # cv2.imshow("Stitched", stitched)
        # cv2.waitKey(0)

    # otherwise the stitching failed, likely due to not enough keypoints
    # being detected
    else:
        print("[ERROR] image stitching failed ({})".format(status))
        return None


def imageDifference(image1, image2, th1=2000, th2=750):
    """
    Compares the difference between two images, returns true if over a threshold

    :param image1: a cv2 img
    :param image2: a cv2 img
    :param th1: upper threshold limit
    :param th2: lower threshold limit
    :return: bool
    """

    test = mse(image1, image2)
    if th1 > test > th2:
        return True
