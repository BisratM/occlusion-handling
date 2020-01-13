import json
import os
import shutil

filenames = []
with open('occluded_imgs.json') as json_file:
	data = json.load(json_file)
	filenames = data['pascal_val2012.json']

# Fill this out manually
directory = 'Annotations'
newDirectory = 'Annotations2'
ext = '.xml'

if not os.path.exists(newDirectory):
	os.makedirs(newDirectory)

for file in filenames:
	path = os.path.join(directory,file+ext)
	if not os.path.isfile(path):
		print("Error, some file with the filename {} does not exist").format(file)
	# Move everything
	os.rename(os.path.join(directory,file+ext), os.path.join(newDirectory, file+ext))

