#!/usr/bin/python
import os, sys
import time
import random
import string
import argparse
import cPickle
import exif.EXIF


"""
Image Namer
Version 1.0 - Tue 22 May 2012

by Reimund Trost <reimund@code7.se>
<http://lumens.se/imagenamer/>

Requires EXIF.py and argparse.
"""

def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser(description='Rename image files with a sequence number.')
	parser.add_argument('-i', metavar='input dir', help='rename images in this directory.')
	parser.add_argument('-s', metavar='string', help='the resulting files will have this prefix.')
	parser.add_argument('-d', metavar='digits', help='the number of digits to use.')
	parser.add_argument('-v', action='store_true', help='verbose output.')

	args = vars(parser.parse_args())

	img_namer = ImageNamer(args)
	img_namer.rename()


class ImageNamer:
	
	def __init__(self, args):
		self.input_directory = '.' if args['i'] == None else args['i']
		self.prefix = '' if args['s'] == None else args['s']
		self.verbose = args['v']
		self.digits = 4 if args['d'] == None else args['d']
		self.input_files = self.get_images(self.input_directory)

		# Store references to files temporary renamed to avoid name collisions.
		self.collisions = {}


		if self.verbose:
			if args['i'] == None:
				print('No input directory specified, using current working directory.')
			if args['d'] == None:
				print('Number of digits not specified, using default value(' + str(self.digits) + ').')
			if args['i'] == None or args['d'] == None:
				print(' ')

		print('Renaming files...')
		#sys.stdout.flush()

	def rename(self):
		files = {}
		i = 1

		for f in self.input_files:
			# Associate each file with a string consisting of the date (in seconds)
			# and the file size.
			# Eg { my_img: 1337437445.0,11951550 }
			files[f] = ''.join([
				str(time.mktime(exif_get_struct_time(f))), ',',
				str(os.path.getsize(f))
			])


		for key, value in sorted(files.iteritems(), key=lambda (k,v): (v,k)):
			name, ext = os.path.splitext(key)
			padded = ('{0:0' + str(self.digits) + '}').format(i)
			self.safe_rename(key, os.path.dirname(key) + '/' + self.prefix + padded + ext)
			i += 1



	# Does the actual renaming.
	def safe_rename(self, src, dst):

		if (src != dst and os.path.isfile(dst)):
			tmp = self.temp_file(os.path.dirname(dst))
			self.collisions[dst] = tmp

			if (self.verbose):
				print('Temporary renaming {0} to {1}.'.format(dst, tmp))

			os.rename(dst, tmp)

		# Rename files that has collided.
		if (src in self.collisions):

			if (self.verbose):
				print('Renaming {0} to {1}.'.format(self.collisions[src], dst))
			os.rename(self.collisions[src], dst)
		else:
			if (self.verbose):
				print('Renaming {0} to {1}.'.format(src, dst))
			os.rename(src, dst)
			


	# Constructs a random file name that does not already exist in the specified
	# directory.
	def temp_file(self, dir):
		tmp = dir + '/' + self.rand_str(16)

		if(os.path.isfile(tmp)):
			tmp = dir + '/' + self.rand_str(16)
		
		return tmp


	def rand_str(self, n):

		return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(n))



	def get_images(self, path):
		
		images = []
		if (os.path.isdir(path)):
			dir_files = [path + '/' + x for x in os.listdir(path)]

			for file in dir_files:
				if file.endswith((
					'.jpg',
					'.jpeg',
					'.gif',
					'.png',
					'.cr2',
					'.CR2',
					'.nef',
					'.NEF',
				)):
					images.append(file)

		return images


def exif_get_struct_time(file):
	"""
	Extracts and parses DateTimeOriginal from the image and if no optional format is
	passed then returns the default format.  Otherwise it converts into a struct_time and
	is formatted with the optional parameter.
	"""

	# Retrieve EXIF DateTimeOriginal tag.
	f = open(file, 'rb')
	tags = exif.EXIF.process_file(f, details=False, stop_tag='DateTimeOriginal')
	f.close()

	# Convert to string and split it.
	try:
		str = cPickle.dumps(tags['EXIF DateTimeOriginal']).split()
		d = str[9][2:] #grabs the date
		t = str[10][:-1] #grabs the time
		
		# Return the time as a struct_time, always assume tm_isdst=-1.
		return time.strptime(d + ' ' + t, '%Y:%m:%d %H:%M:%S')

	except KeyError: # Handles missing timestamps.
		raise TimeError("missing")
	except ValueError: # Handles malformed timestamps.
		raise TimeError("malformed")



if __name__ == "__main__":
    sys.exit(main())

