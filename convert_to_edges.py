import os
import cv2
import glob
from skimage.feature import canny
from skimage import img_as_ubyte

SIGMA = 0.75
class Path:
	def __init__(self, base_path):
		self.base_path = base_path
		self.front = base_path + "/front/"
		self.back = base_path + "/back/"

class Image:
	def __init__(self, base_path, file_name):
		self.base_path = base_path
		self.file_name = file_name

def load_images():
	frames_to_convert = []
	folders = [Path(path) for path in glob.glob(os.getcwd() + "/*") if os.path.isdir(path)]

	for path in folders:
		front_frames = glob.glob(path.front + "resize150/*")
		os.mkdir(path.front + "edges_150_" + str(SIGMA) + "/")

		for image_path in front_frames:
			image_name = image_path.split("/")[-1]
			frames_to_convert.append(Image(path.front, image_name))

		back_frames = glob.glob(path.back + "resize150/*")
		os.mkdir(path.back + "edges_150_" + str(SIGMA) + "/")

		for image_path in back_frames:
			image_name = image_path.split("/")[-1]
			frames_to_convert.append(Image(path.back, image_name))

	return frames_to_convert

def manipulate_images(frames_array):
	for image in frames_array:
		image_data = cv2.imread(image.base_path + "resize150/" + image.file_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
		image_edges = img_as_ubyte(canny(image_data, sigma=1))

		cv2.imwrite(image.base_path + "edges_150_" + str(SIGMA) + "/" + image.file_name, image_edges)

manipulate_images(load_images())
