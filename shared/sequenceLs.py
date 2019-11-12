#!/usr/bin/python

# [Icarus] sequenceLs.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Command-line tool for listing file sequences in a nicely formatted manner.
# TODO: Take arguments to list specific directory or sequence


import argparse
import os
import sys

from . import sequence


# Set up arguments
parser = argparse.ArgumentParser(description='Detect and list file sequences')
parser.add_argument('path', nargs='*', help='The directory to process. If left blank, the current directory will be used.')
#parser.add_argument('base', help='Specify the base name (the part of the filename before the sequence numbering).')

args = parser.parse_args()

if args.path:
	path = os.path.abspath(args.path[0])
else:
	path = os.getcwd()

# Get list of file sequence bases in specified directory
bases = sequence.getBases(path)

if bases:
	print("%d file sequence(s) found:" %len(bases))
else:
	sys.exit("No file sequences detected in '%s'" %path)

for base in bases:
	path, prefix, fr_range, ext, num_frames = sequence.getSequence(path, base)

	# Print output
	print("%s.[%s]%s (%d)" %(prefix, fr_range, ext, num_frames))

