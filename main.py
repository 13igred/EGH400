import os
import cv2
import DetectorClass
import PanoramaClass
import ProjectClass

# ------------ Pano Tester ------------
# Load pano images - TESTING PURPOSES
# use path to define opening point
path = './data/initPanorama/Noosa1/'
images = []
weightsPath = './runs/train/exp6/weights/best.pt'
detector = DetectorClass.Detector(weightsPath)

for file in os.listdir(path):
    img = cv2.imread(path + file)
    images.append(img)

for idx, cImg in enumerate(images):
    x1, y1, x2, y2 = detector.detect(cImg)
    project = ProjectClass.Project(x1, y1, x2, y2, cImg)
    pt1, pt2, valid = project.calculate()

    if valid:
        # todo: pass to crowd counting algorithm. Get people positions and see if they are inside the flags,
        # todo: highlight outside of flag?
        images[idx] = project.drawMarkup(pt1, pt2, False)


pano = PanoramaClass.Panorama()
for img in images:
    pano.addImageToBuffer(img)

bufferValid = pano.createPanorama()

if bufferValid:
    # todo: count crowds

    pano.displayPanorama(10000)
    pano.savePanorama()

    folderPath = './data/images/Noosa/'
    count = 0

    for file in os.listdir(folderPath):
        print()
        print('[INFO] Checking Image ' + file)
        updated, imgIdx = pano.compareUpdate(folderPath + file, 0)
        if updated:
            print('[INFO] Panorama composite image no. ' + str(imgIdx) + ' has been updated')
            count += 1
            if count > 10:
                count = 0
                pano.updatePanorama(0)
                pano.displayPanorama(0)
                pano.savePanorama()

    pano.updatePanorama()
    pano.displayPanorama()


if __name__ == '__main__':
    pass


