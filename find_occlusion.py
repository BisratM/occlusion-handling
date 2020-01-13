import json
import os
import shutil

THRESHOLD = 0.3

# function adapted from https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def computeIOU(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
 
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = 0.0
	try:
		iou = interArea / float(boxAArea + boxBArea - interArea)
	except:
		print("divide by 0")

	# return the intersection over union value
	return iou

def find_overlapping(cars_bboxes, i_name):
	for idxA, boxA in enumerate(cars_bboxes):
		for idxB, boxB in enumerate(cars_bboxes):
			if(idxA == idxB):
				continue
			if(i_name == "2009_002613"):
				print(computeIOU(boxA, boxB))
			if(computeIOU(boxA, boxB) >= THRESHOLD):
				return True
	return False



cwd = os.getcwd()
occluded_imgs = {}
for (dirpath, dirnames, filenames) in os.walk(cwd):
	for file in filenames:
		if file.split('.')[-1] != 'json':
			continue
		occluded_imgs[file] = set([])
		img_bboxes = {}
		with open(os.path.join(dirpath, file)) as json_file:
			data = json.load(json_file)
			if(file == 'pascal_train2012.json'):
				train_file_names = data['images']
			for annot in data['annotations']:
				img_name = str(annot['image_id'])[0:4] + '_' + str(annot['image_id'])[4:]
				img_bboxes.setdefault(img_name, []).append(annot['bbox'])
			for name, box_list in img_bboxes.items():
				if find_overlapping(box_list, name):
					occluded_imgs[file].add(name)
print(len(occluded_imgs['pascal_train2012.json']))
print(len(occluded_imgs['pascal_val2012.json']))
import random
random.shuffle(train_file_names)

already_occluded = occluded_imgs['pascal_train2012.json']
count = 0
train_file_names = [x['file_name'] for x in train_file_names]

# uncomment below blocks if needed

# extract occluded data
#while(count < 1000):
#	shutil.move("./new_images/" + train_file_names[count], "./" + train_file_names[count])
#	count += 1

# extract artificial occluded data
#for img in occluded_imgs['pascal_val2012.json']:
#	shutil.move("./JPEGImages/" + img + ".jpg", "./" + img + ".jpg")

# save jsons
#with open('occluded_imgs.json', 'w') as outfile:
#	json.dump(occluded_imgs, outfile)

