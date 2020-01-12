import json
import os

THRESHOLD = 0.4

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
	iou = interArea / float(boxAArea + boxBArea - interArea)
 
	# return the intersection over union value
	return iou

def get_bbox(polygon):
	min_x = polygon[0][0]
	min_y = polygon[0][1]
	max_x = polygon[0][0]
	max_y = polygon[0][1]
	for coord in polygon:
		min_x = min(min_x, coord[0])
		min_y = min(min_y, coord[1])
		max_x = max(max_x, coord[0])
		max_y = max(max_y, coord[1])
	return (min_x, min_y, max_x, max_y)

def find_overlapping(cars_bboxes):
	for idxA, boxA in enumerate(cars_bboxes):
		for idxB, boxB in enumerate(cars_bboxes):
			if(idxA == idxB):
				continue
			if(computeIOU(boxA, boxB) >= THRESHOLD):
				return True
	return False



cwd = os.getcwd()
occluded_imgs = {}
occluded_imgs['test'] = []
occluded_imgs['train'] = []
occluded_imgs['val'] = []
for subdir, dirs, files in os.walk(cwd):
	dir_type = subdir.split('\\')[-2]
	for file in files:
		if(file.split('.')[-1] == 'json'):
			with open(os.path.join(subdir, file)) as json_file:
				data = json.load(json_file)
				cars_bboxes = []
				for obj in data['objects']:
					if obj["label"] == "car":
						cars_bboxes.append(get_bbox(obj["polygon"]))
				if find_overlapping(cars_bboxes):
					occluded_imgs[dir_type].append(file)
with open('occluded_imgs.json', 'w') as outfile:
	json.dump(occluded_imgs, outfile)

