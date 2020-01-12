from pycocotools.coco import COCO

import sys
import os
import cv2
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt

d = {}

# Given the annotations json file, fills in dict d that maps filename to GT bounding boxes.
def filenames_to_bboxes(annFile):
	coco = COCO(annFile)
	imgIds = coco.getImgIds()

	for imgId in imgIds:
		img = coco.loadImgs(ids=imgId)[0]
		# This should be the file path relative to working dir
		d[img['file_name']] = []
		annIds = coco.getAnnIds(imgIds=imgId)
		anns = coco.loadAnns(ids=annIds)
		for ann in anns:
			d[img['file_name']].append(ann['bbox'])


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


# Updated img_patch. Helper that creates occlusion on one image with less randomness (???)
def img_patch_2(src, dst=None):
	# name, ext = os.path.splitext(src)
	# if not ext == '.jpg':
	# 	return
	img = cv2.imread(src)
	height, width, _ = img.shape

	random.seed()

	bboxes = d[src] # Array of bounding boxes in [xmin ymin width height] format
	
	min_overlap = 1
	max_overlap = 0
	while min_overlap > 0.5 or max_overlap < 0.25:
		patch_height = random.randint(int(height/4),int(height/2))
		patch_width = random.randint(int(width/4),int(width/2))
		row = random.randint(0,height-patch_height)
		col = random.randint(0,width-patch_width)

		occlusion = [col,row,patch_width,patch_height]
		min_overlap, max_overlap = overlaps(occlusion, bboxes)

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


# Given a rectangular occlusion patch and an array of bounding boxes (all [x y width height]
# format), returns min and max percentages of overlap when comparing the patch to each box.
def overlaps(occlusion, bboxes):
	min_overlap = 1
	max_overlap = 0
	for bbox in bboxes:
		overlap_area = overlap(occlusion, bbox)
		bbox_area = bbox[2]*bbox[3] # Width times height of bounding box
		ratio = overlap_area/bbox_area
		if ratio < min_overlap:
			min_overlap = ratio
		if ratio > max_overlap:
			max_overlap = ratio
	return min_overlap, max_overlap


# Takes in two rectangles as arrays as [x y width height] and returns their overlapping area.
# Adapted from https://stackoverflow.com/questions/27152904/calculate-overlapped-area-between-two-rectangles.
def overlap(a, b):
	a_xmax = a[0]+a[2]
	a_ymax = a[1]+a[3]
	b_xmax = b[0]+b[2]
	b_ymax = b[1]+b[3]
	dx = min(a_xmax, b_xmax) - max(a[0], b[0])
	dy = min(a_ymax, b_ymax) - max(a[1], b[1])
	if (dx>=0) and (dy>=0):
		return (dx*dy)
	return 0


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

			# Replaces name with path to be used in img_patch func
			if filename in d:
				d[filepath] = d[filename]
				del d[filename]

			img_patch(filepath)
	return


if __name__=='__main__':
	dir_patch('sample_data', 'new_data')

	# Tests:
	# setup(sys.argv[1], sys.argv[2])
	# convert_img('IMG_3724.jpeg')
	# convert_img('sample_data/IMG_1887.JPG')
	# convert_img('IMG_3723.JPG','sample_data/newpath.jpg')
	# convert_img('IMG_9673.PNG','sample_data')
