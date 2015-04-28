#!/usr/bin/env python

import os, re, glob
import sequence

path = os.getcwd()
ls = os.listdir(path)
ls.sort()

seqRE = re.compile(r'\d+$')

# create list to hold all basenames of sequences
all_bases = []

# get list of files in current dir
for filename in ls:

	# extract file extension
	root, ext = os.path.splitext(filename)

	# match file names which have a trailing number
	match = seqRE.search(root)

	# store filename prefix
	if match is not None:
		prefix = root[:root.rfind(match.group())]
		all_bases.append(prefix)

# remove duplicates & sort list
bases = list(set(all_bases))
bases.sort()

#print bases
print "%d file sequences found:" %len(bases)

for base in bases:
	try:
		filter_ls = glob.glob("%s*" %base)
		frame_ls = []

		for filename in filter_ls:

			# extract file extension
			root, ext = os.path.splitext(filename)

			# match file names which have a trailing number
			match = seqRE.search(root)
			num = match.group()
			frame_ls.append(int(num))

		frame_ls.sort()
		fr_range = sequence.numRange(frame_ls)

		print "%s[%s]%s" %(base, fr_range, ext)

	except ValueError:
		pass
