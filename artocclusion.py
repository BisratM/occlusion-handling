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


# Adapted from https://www.freecodecamp.org/news/image-augmentation-make-it-rain-make-it-snow-how-to-modify-a-photo-with-machine-learning-163c0cb3843f/
def generate_random_lines(imshape, slant, drop_length):
	random.seed()
	drops = []
	for i in range(1000):
		x = np.random.randint(0,imshape[1]-slant)
		y = np.random.randint(0,imshape[0]-drop_length) 
		drops.append((x,y))
	return drops


# Helper that artificially adds rain over a single image. Takes in the file path
# and the optional destination path (if dst not given, it overwrites the original file).
# Adapted from https://www.freecodecamp.org/news/image-augmentation-make-it-rain-make-it-snow-how-to-modify-a-photo-with-machine-learning-163c0cb3843f/
def add_rain(src, dst=None):
	# name, ext = os.path.splitext(src)
	# if not ext == '.jpg':
	# 	return
	img = cv2.imread(src)
	imshape = img.shape
	random.seed()
	slant = np.random.randint(-5,5)
	drop_length = np.random.randint(int(imshape[0]/100), int(imshape[0]/40))
	drop_width = 1
	drop_color = (200,200,200) # Gray
	rain_drops = generate_random_lines(imshape,slant,drop_length)
	for rain_drop in rain_drops:
		cv2.line(img,(rain_drop[0],rain_drop[1]),(rain_drop[0]+slant,rain_drop[1]+drop_length),drop_color,drop_width)
	image = cv2.blur(img,(5,5)) # Add slight blur
	brightness_coefficient = 0.9 # Add slight shadow
	image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) # Convert to HLS    
	image_HLS[:,:,1] = image_HLS[:,:,1]*brightness_coefficient ## scale pixel values down for channel 1(Lightness)    
	image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) # Convert to RGB
	
	if dst is None:
		cv2.imwrite(src, image_RGB)
	else:
		cv2.imwrite(dst, image_RGB)
	return image_RGB

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
	dir_patch('sample_data', 'new_images')

	# Tests:
	# setup(sys.argv[1], sys.argv[2])
	# convert_img('IMG_3724.jpeg')
	# convert_img('sample_data/IMG_1887.JPG')
	# convert_img('IMG_3723.JPG','sample_data/newpath.jpg')
	# convert_img('IMG_9673.PNG','sample_data')
