# Name:   animated_gif.py
# Purpose:   Animates all PNGs in a folder as a GIF
# Author:   Andy Bell - ambell@ucdavis.edu
# Created:  11/14/14
#--------------------------------

from images2gif import writeGif
from PIL import Image
import os


def animated_gif(folder_with_images, gif_filename, loop_duration, size):
	"""uses images2gif.py to turn all png images in a folder into an animated GIF"""

	os.chdir(folder_with_images) # changes directory to the folder with the images
	png_files = sorted((fn for fn in os.listdir(folder_with_images) if fn.endswith('.png')))  # sorts png files

	#number of png_files
	num_pngs = len(png_files)
	png_time = float(loop_duration)/ float(num_pngs)

	images = [Image.open(fn) for fn in png_files]
	dim = (size, size)  # change sizes for the image file dimension
	for im in images:
		im.thumbnail(dim, Image.ANTIALIAS)

	output_file = os.path.join(folder_with_images, gif_filename)   # path for output file
	writeGif(output_file, images, png_time, repeat=True, dither=False, nq=10)  # writes out GIF
	
	# def writeGif(filename, images, duration=0.1, repeat=True, dither=False, nq=0):
    """ writeGif(filename, images, duration=0.1, repeat=True, dither=False)

    Write an animated gif from the specified images.

    Parameters
    ----------
    filename : string
       The name of the file to write the image to.
    images : list
        Should be a list consisting of PIL images or numpy arrays.
        The latter should be between 0 and 255 for integer types, and
        between 0 and 1 for float types.
    duration : scalar or list of scalars
        The duration for all frames, or (if a list) for each frame.
    repeat : bool or integer
        The amount of loops. If True, loops infinitetely.
    dither : bool
        Whether to apply dithering
    nq : integer
        If nonzero, applies the NeuQuant quantization algorithm to create
        the color palette. This algorithm is superior, but slower than
        the standard PIL algorithm. The value of nq is the quality
        parameter. 1 represents the best quality. 10 is in general a
        good tradeoff between quality and speed.

    """


if __name__ == '__main__':
	animated_gif()