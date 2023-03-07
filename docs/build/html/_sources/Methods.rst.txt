Methods
=======

Creating A Panorama
-------------------

The first step is to add images to the classes buffer

.. py:function:: addImageToBuffer(self, img)
    Adds the input image to the classes image buffer

    Parameters
    ----------
    img : numpy
        A cv2 image

Once the buffer has a sufficient number of images > 20, createPanorama can perform the image stitching process.

Depending on the amount of images this can take a significant time.

.. py:function:: createPanorama()
    Stitches together images to create the panorama

Once a panorama has been built it can be continuously updated by using compareUpdate.

This function compares the given image with the images that made up the panorama.

If there is a significant similarity between images the passes image becomes the new basis for the next panorama.

.. py:function:: compareUpdate(image)
    Compares a given image to each of the images in the panorama composite array

    Parameters
    ----------
    image : numpy
        A cv2 image

updatePanorama is used to generate a new panorama based on updated images.

.. py:function:: updatePanorama()
    Generatess a panoramic image based on images in the internal buffer

To display the panorama, displayPanorama can be used.

.. py:function:: displayPanorama(timeDelay=0):
        Displays the panoramic image, exit display by pressing 'any' key

        Parameters
        ----------
        timeDelay: int
            specify time delay image is shown for in mS, default is displayed until key press

Finally to save the panorama

.. py:function:: savePanorama(path=None):
        Saves the panorama in the specified file location or in a default locations


Detecting Flags in an Image
---------------------------

The detector class handles finding flags in an image.

It creates a yolov5 model using pytorch and weights that are included in the github repo.

the methods used include:

.. py:function:: detect(image):
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

.. py:function:: markup(self, image, x1, y1, x2, y2, display):
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


Projecting Safe Swim Zones
--------------------------
The final aspect of this project was to project safe swim zones onto the panoramic images.

The goal of this was to assist life savers in easily identifying those outside of the safe swim zone.

The methods are detailed below:

.. py:function:: calculate():
        calculate the projection zones for the flags.

        Return
        ------
        pt1 : list
            contains the location of the 1st flag
        pt2 : list
            contains the location of the 2nd flag
        bool
            true if successful

.. py:function:: markup():
        Depreciated use drawMarkup

.. py:function:: drawMarkup(pt1, pt2, display):
        draws the markup onto the image provided and returns that image.

        Parameter
        ----------
        pt1 : list
            locations of the first points to be drawn
        pt2: list
            locations of the second points to be drawn
        display: bool
            Displays the image if true

        Return
        ------
        numpy
            a cv2 image