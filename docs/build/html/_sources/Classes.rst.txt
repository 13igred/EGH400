Classes
=======

Panorama Class
--------------

.. py:class::
    A class ued to build a panoramic image

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

Detector Class
--------------

.. py:class::
    A class ued to detect flags in an image

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

Project Class
--------------

.. py:class::
    This class handles projecting and drawing safe swim zones on the images provided

    Attributes
    ----------
    x1 : int
            locations that flags were detected
    y1 : int
        locations that flags were detected
    x2 : int
        locations that flags were detected
    y2 : int
        locations that flags were detected
    image : numpy
        a cv2 image
    middle : list
         an array contain the mid point of the found flags

    Methods
    -------
    calculate()
        calculate the project zones for the flags.

    markup
        depreciated use drawMarkup.

    drawMarkup(pt1, pt2, display)
        draws the markup onto the image provided and returns that image
