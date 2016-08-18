import cv2
import time
import numpy as np
import glob
import os
from skimage.feature import canny
from skimage import img_as_ubyte

FILENAME = 'raw_trimmed.mp4'
FRAMERATE = 60
RAW_IMAGE_WIDTH = 1280
RAW_IMAGE_HEIGHT = 720
FINAL_IMAGE_SIZE = 150

ACTIVE = True

class Frame:
    def __init__(self, image, basepath, count):
        self.image = image
        self.basePath = basepath
        self.count = count

def extract_frames(video, savePath):
    cap = cv2.VideoCapture(video)
    timeCount = 0.0
    loopCount = 0

    while True:
        succ, image = cap.read()

        if succ:
            print str(timeCount) + str(int(timeCount))
            framesToConvert.append(Frame(image, savePath, int(timeCount)))

        else:
            break

        if loopCount % 1000 == 0:
            manipulate()

        timeCount += (1.0 / FRAMERATE) * 1000.0
        loopCount += 1

    manipulate()


def extract():
    for folderPath in folders:
        extract_frames(folderPath + "/" + FILENAME, folderPath)


def manipulate():
    edges_sigma = 1

    while len(framesToConvert) > 0:
        currentFrame = framesToConvert.pop(-1)

        if not os.path.isdir(currentFrame.basePath + "/raw/"):
            os.mkdir(currentFrame.basePath + "/raw/")
            os.mkdir(currentFrame.basePath + "/grayscale/")
            os.mkdir(currentFrame.basePath + "/cropped/")
            os.mkdir(currentFrame.basePath + "/resize150/")
            os.mkdir(currentFrame.basePath + "/edges_" + str(edges_sigma) + "/")

        cv2.imwrite(currentFrame.basePath + "/raw/FRAME_" + str(currentFrame.count) + ".jpg", currentFrame.image)

        grayscaleImage = cv2.cvtColor(currentFrame.image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(currentFrame.basePath + "/grayscale/FRAME_" + str(currentFrame.count) + ".jpg", grayscaleImage)

        croppedImage = grayscaleImage[0:RAW_IMAGE_HEIGHT, ((RAW_IMAGE_WIDTH - RAW_IMAGE_HEIGHT) / 2):RAW_IMAGE_WIDTH - ((RAW_IMAGE_WIDTH - RAW_IMAGE_HEIGHT) / 2)]
        cv2.imwrite(currentFrame.basePath + "/cropped/FRAME_" + str(currentFrame.count) + ".jpg", croppedImage)

        resizedImage = cv2.resize(croppedImage, (FINAL_IMAGE_SIZE, FINAL_IMAGE_SIZE), interpolation=cv2.INTER_AREA)
        cv2.imwrite(currentFrame.basePath + "/resize150/FRAME_" + str(currentFrame.count) + ".jpg", resizedImage)

        edges = img_as_ubyte(canny(resizedImage, sigma=1.75))
        cv2.imwrite(currentFrame.basePath + "/edges_" + str(edges_sigma) + "/FRAME_" + str(currentFrame.count) + ".jpg", edges)

folders = [path for path in glob.glob(os.getcwd() + "/*") if os.path.isdir(path)]
framesToConvert = []

extract()
