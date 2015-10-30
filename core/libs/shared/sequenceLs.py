#!/usr/bin/env python

# List Sequences
# v0.2
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) Gramercy Park Studios 2015
#
# Command-line tool for listing file sequences in a nicely formatted manner.
# TODO: Take arguments to list specific directory or sequence


import argparse, glob, os, re, sys
import sequence


# Set up arguments
parser = argparse.ArgumentParser(description='Detect and list file sequences')
parser.add_argument('path', nargs='*', help='The directory to process. If left blank, the current directory will be used.')
#parser.add_argument('base', help='Specify the base name (the part of the filename before the sequence numbering).')

args = parser.parse_args()

if args.path:
	path = os.path.abspath(args.path[0])
else:
	path = os.getcwd()

# Get directory contents
try:
	ls = os.listdir(path)
	ls.sort()
except OSError:
	sys.exit("No such file or directory: '%s'" %path)

seqRE = re.compile(r'\d+$')

# Create list to hold all basenames of sequences
all_bases = []

# Get list of files in current dir
for filename in ls:

	# Only work on files, not directories
	if os.path.isfile(os.path.join(path, filename)):

		# Extract file extension
		root, ext = os.path.splitext(filename)

		# Match file names which have a trailing number
		match = seqRE.search(root)

		# Store filename prefix
		if match is not None:
			prefix = root[:root.rfind(match.group())]
			all_bases.append(prefix)

# Remove duplicates & sort list
bases = list(set(all_bases))
bases.sort()

#print bases

if bases:
	print "%d file sequence(s) found:" %len(bases)
else:
	sys.exit("No file sequences detected in '%s'" %path)

for base in bases:
	try:
		filter_ls = glob.glob("%s*" %os.path.join(path, base))
		frame_ls = []

		for filename in filter_ls:

			# Extract file extension
			root, ext = os.path.splitext(filename)

			# Match file names which have a trailing number
			match = seqRE.search(root)

			if match is not None:
				num = match.group()
				frame_ls.append(int(num))

		frame_ls.sort()
		fr_range = sequence.numRange(frame_ls)

		# Print output
		print "%s[%s]%s" %(base, fr_range, ext)

	except (ValueError):
		pass

