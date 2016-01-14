# Name:   animated_gif.py
# Purpose:   Animates all PNGs in a folder as a GIF
# Author:   Andy Bell - ambell@ucdavis.edu
# Created:  11/14/14
#--------------------------------

import os
import re
from images2gif import writeGif
from PIL import Image



# from http://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically
def tryint(s):
	try:
		return int(s)
	except:
		return s

def alphanum_key(s):
	""" Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
	return [tryint(c) for c in re.split('([0-9]+)', s)]

def sort_nicely(l):
	""" Sort the given list in the way that humans expect.
    """
	l.sort(key=alphanum_key)


def animated_gif(folder_with_images, gif_filename, loop_duration, size):
	"""uses images2gif.py to turn all png images in a folder into an animated GIF"""

	os.chdir(folder_with_images) # changes directory to the folder with the images

	png_files = []

	# get list of png files in folder
	for fn in os.listdir(folder_with_images):
		if fn.endswith('.png'):
			png_files.append(fn)

	sort_nicely(png_files)

	print(png_files)

	# number of png_files
	num_pngs = len(png_files)
	png_time = float(loop_duration)/ float(num_pngs)

	images = [Image.open(fn) for fn in png_files]
	dim = (size, size)  # change sizes for the image file dimension
	#for im in images:
	#	im.thumbnail(dim, Image.ANTIALIAS)

	output_file = os.path.join(folder_with_images, gif_filename)   # path for output file
	writeGif(output_file, images, png_time)  # writes out GIF


if __name__ == '__main__':
	animated_gif()