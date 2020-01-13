import sys
import os
import cv2
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt


# Add artificial occlusion on one image using img_patch and displays the result in plot.
# Takes in the file path and the optional destination file/directory path.
def convert_img(src, dst=None):
	if not os.path.exists(src):
		print("Path {} not found".format(src))
		return
	elif not os.path.isfile(src):
		print("Path {} is not a valid file path".format(src))
		return

	plt.imshow(cv2.cvtColor(cv2.imread(src), cv2.COLOR_BGR2RGB))
	plt.show()

	if dst is None:
		# If no destination is given, set default path in the same directory
		name, ext = os.path.splitext(src)
		dst = name + "OCC" + ext
	elif os.path.isdir(dst):
		# If only a destination directory is given, set default path
		filename = os.path.basename(src)
		name, ext = os.path.splitext(filename)
		dst = os.path.join(dst, name + "OCC" + ext)

	img = img_patch(src, dst)

	plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
	plt.show()


# Helper that randomly creates occlusion patch on a single image. Takes in the file path
# and the optional destination path (if dst not given, it overwrites the original file).
def img_patch(src, dst=None):
	# name, ext = os.path.splitext(src)
	# if not ext == '.jpg':
	# 	return
	img = cv2.imread(src)
	height, width, _ = img.shape

	random.seed()
	patch_height = random.randint(int(height/4),int(height/2))
	patch_width = random.randint(int(width/4),int(width/2))
	row = random.randint(0,height-patch_height)
	col = random.randint(0,width-patch_width)

	patch = img[row:row+patch_height, col:col+patch_width]
	patch_reshaped = np.reshape(patch, (patch.shape[0] * patch.shape[1], patch.shape[2]))
	np.random.shuffle(patch_reshaped)
	patch_random = np.reshape(patch_reshaped, patch.shape)

	img[row:row+patch_height, col:col+patch_width] = patch_random

	if dst is None:
		cv2.imwrite(src, img)
	else:
		cv2.imwrite(dst, img)
	return img


# Makes a recursive copy of a given directory (defaults to current working directory) to a
# specified destination. Assuming all files are images, applies an occlusion patch to every
# image copy in the destination directory.
def dir_patch(src=os.getcwd(), dst=None):
	if dst is None:
		print("No destination directory name given. Stopping...")
		return

	# NOTE: Overwrites existing directory of the given name if there is one
	if os.path.exists(dst):
		shutil.rmtree(dst)

	try:
		shutil.copytree(src, dst)
	except shutil.Error as e: # Directories are the same
		print('Directory not copied. Error: %s' % e)
	except OSError as e: # Any error saying that src doesn't exist
		print('Directory not copied. Error: %s' % e)

	# Fill in dictionary here. Uncomment later
	# filenames_to_bboxes(annFile)

	for root, dirs, files in os.walk(dst):
		for filename in files:
			filepath = os.path.abspath(os.path.join(root, filename))
			img_patch(filepath)
	return


if __name__=='__main__':
	dir_patch('PASCALVOC2012', 'new_images')

	# Tests:
	# setup(sys.argv[1], sys.argv[2])
	# convert_img('IMG_3724.jpeg')
	# convert_img('sample_data/IMG_1887.JPG')
	# convert_img('IMG_3723.JPG','sample_data/newpath.jpg')
	# convert_img('IMG_9673.PNG','sample_data')
