#!/usr/bin/env python

# [Icarus] sequenceLs.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
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

# Get list of files in current directory
for filename in ls:

	# Only work on files, not directories
	if os.path.isfile(os.path.join(path, filename)):

		# Extract file extension
		root, ext = os.path.splitext(filename)

#		try:
#			base, ext = os.path.splitext(filename)
#			prefix, framenumber = base.rsplit('.', 1)
#			padding = len(framenumber)
#			framenumber = int(framenumber)
#
#			# Construct regular expression for matching files in the sequence
#			re_seq_pattern = re.compile( r"^\Q%s\E\.\d{%d}\Q%s\E$" %(prefix, padding, ext) )
#			all_bases.append(re_seq_pattern)
#
#		except ValueError:
#			pass
#			#print "Error: could not parse sequence."
#			#return False, False # need to return tuple to match successful return type (str, str)

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

#		# Find other files in the sequence in the same directory
#		for item in os.listdir(path):
#			if base.match(item) is not None:
#				#frame_ls.append(item) # whole filename
#				frame_ls.append( int(os.path.splitext(item)[0].rsplit('.', 1)[1]) ) # just the frame number

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
		print "%s[%s]%s (%d)" %(base, fr_range, ext, len(frame_ls))

	except (ValueError):
		pass

