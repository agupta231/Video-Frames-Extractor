import cv2
import time
import numpy as np
import glob
import os

FILENAME = 'rawTrimmed.mp4'
FRAMERATE = 60
RAW_IMAGE_WIDTH = 1280
RAW_IMAGE_HEIGHT = 720
FINAL_IMAGE_SIZE = 150

ACTIVE = True

class Path:
    def __init__(self, basePath):
        self.basePath = basePath
        self.front = self.basePath + "/front/"
        self.back = self.basePath + "/back/"


class Frame:
    def __init__(self, image, basepath, count):
        self.image = image
        self.basePath = basepath
        self.count = count

def extract_frames(video, savePath):
    cap = cv2.VideoCapture(video)
    timeCount = 0.0

    while True:
        succ, image = cap.read()

        if succ:
            print str(timeCount) + str(int(timeCount))
            framesToConvert.append(Frame(image, savePath, int(timeCount)))

        else:
            break

        timeCount += (1.0 / FRAMERATE) * 1000.0


def extract():
    for folderPath in folders:
        extract_frames(folderPath.front + FILENAME, folderPath.front)
        print len(framesToConvert)
        manipulate()

        extract_frames(folderPath.back + FILENAME, folderPath.back)
        print len(framesToConvert)
        manipulate()


def manipulate():
    while len(framesToConvert) > 0:
        currentFrame = framesToConvert.pop(-1)

        if not os.path.isdir(currentFrame.basePath + "/raw/"):
            os.mkdir(currentFrame.basePath + "/raw/")
            os.mkdir(currentFrame.basePath + "/grayscale/")
            os.mkdir(currentFrame.basePath + "/cropped/")
            os.mkdir(currentFrame.basePath + "/resize150/")

        cv2.imwrite(currentFrame.basePath + "/raw/FRAME_" + str(currentFrame.count) + ".jpg", currentFrame.image)

        grayscaleImage = cv2.cvtColor(currentFrame.image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(currentFrame.basePath + "/grayscale/FRAME_" + str(currentFrame.count) + ".jpg", grayscaleImage)

        croppedImage = grayscaleImage[0:RAW_IMAGE_HEIGHT, ((RAW_IMAGE_WIDTH - RAW_IMAGE_HEIGHT) / 2):RAW_IMAGE_WIDTH - ((RAW_IMAGE_WIDTH - RAW_IMAGE_HEIGHT) / 2)]
        cv2.imwrite(currentFrame.basePath + "/cropped/FRAME_" + str(currentFrame.count) + ".jpg", croppedImage)

        resizedImage = cv2.resize(croppedImage, (FINAL_IMAGE_SIZE, FINAL_IMAGE_SIZE), interpolation=cv2.INTER_AREA)
        cv2.imwrite(currentFrame.basePath + "/resize150/FRAME_" + str(currentFrame.count) + ".jpg", resizedImage)


folders = [Path(path) for path in glob.glob(os.getcwd() + "/*") if os.path.isdir(path)]
framesToConvert = []

extract()
