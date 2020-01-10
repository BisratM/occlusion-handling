import sys
import os
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt

def main():
	setup(sys.argv[1], sys.argv[2])


# Takes in two arguments: a file path and a destination path/directory
def convert_img(path, dest=None):
	if not os.path.exists(path):
		print("Path {} not found".format(path))
		return
	elif not os.path.isfile(path):
		print("Path {} is not a valid image file".format(path))
		return

	plt.imshow(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB))
	plt.show()

	img = img_patch(path, dest)

	plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
	plt.show()


def img_patch(path, dest):
	if dest is None:
		# If no destination is given, set default path in the same directory
		name, ext = os.path.splitext(path)
		dest = name + "OCC" + ext
	elif os.path.isdir(dest):
		# If only a destination directory is given, set default path
		filename = os.path.basename(path)
		name, ext = os.path.splitext(filename)
		dest = os.path.join(dest, name + "OCC" + ext)
	
	img = cv2.imread(path)
	height, width, _ = img.shape

	random.seed()
	patch_height = random.randint(0,int(height/2))
	patch_width = random.randint(0,int(width/2))
	row = random.randint(0,height-patch_height)
	col = random.randint(0,width-patch_width)

	patch = img[row:row+patch_height, col:col+patch_width]
	patch_reshaped = np.reshape(patch, (patch.shape[0] * patch.shape[1], patch.shape[2]))
	np.random.shuffle(patch_reshaped)
	patch_random = np.reshape(patch_reshaped, patch.shape)

	img[row:row+patch_height, col:col+patch_width] = patch_random

	cv2.imwrite(dest, img)
	return img


if __name__=='__main__':
	main()

	# tests
    # convert_img('IMG_3724.jpeg')
    # convert_img('sample_data/IMG_1887.JPG')
    # convert_img('IMG_3723.JPG','sample_data/newpath.jpg')
    # convert_img('IMG_9673.PNG','sample_data')
