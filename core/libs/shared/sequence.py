#!/usr/bin/python

# [Icarus] sequence.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# These functions convert formatted sequences to lists and vice-versa.


import glob, os, re


def numList(num_range_str, quiet=False):
	""" Takes a formatted string describing a range of numbers and returns a sorted integer list.
		e.g. '1-5, 20, 24, 1001-1002'
		returns [1, 2, 3, 4, 5, 20, 24, 1001, 1002]
	"""
	num_int_list = []
	num_format = re.compile(r'^\d+$')
	seq_format = re.compile(r'^\d+-\d+$')

	# Split into groups of ranges separated by commas
	grps = re.split(r',\s*', num_range_str)
	for grp in grps:

		# 'grp' is a single number (e.g. 10)
		if num_format.match(grp) is not None:
			num_int_list.append(int(grp))

		# 'grp' is a number sequence (e.g. 1-10)
		elif seq_format.match(grp) is not None:
			seq = re.split(r'-', grp)
			first = int(seq[0])
			last = int(seq[1])
			if first > last:
				if not quiet:
					print "ERROR: The last number (%d) in the sequence cannot be smaller than the first (%d)." %(last, first)
				return False
			else:
				int_list = list(range(first, last+1))
				for num in int_list:
					num_int_list.append(num)

		else:
			if not quiet:
				print "ERROR: Sequence format is invalid."
			return False

	# Remove duplicates & sort list
	return sorted(list(set(num_int_list)), key=int)


def numRange(num_int_list, padding=0, quiet=False):
	""" Takes a list of integer values and returns a formatted string describing the range of numbers.
		e.g. [1, 2, 3, 4, 5, 20, 24, 1001, 1002]
		returns '1-5, 20, 24, 1001-1002'
	"""
	num_range_str = ''

	# Remove duplicates & sort list
	try:
		sorted_list = sorted(list(set(num_int_list)), key=int)
	except (ValueError, TypeError):
		if not quiet:
			print "ERROR: Number list only works with integer values."
		return False
		

	# Find sequences
	first = None
	for x in sorted_list:
		if first is None:
			first = last = x
		elif x == last+1:
			last = x
		else:
			if first == last:
				num_range_str = num_range_str + "%s, " %str(first).zfill(padding)
			else:
				num_range_str = num_range_str + "%s-%s, " %(str(first).zfill(padding), str(last).zfill(padding))
			first = last = x
	if first is not None:
		if first == last:
			num_range_str = num_range_str + "%s" %str(first).zfill(padding)
		else:
			num_range_str = num_range_str + "%s-%s" %(str(first).zfill(padding), str(last).zfill(padding))

	return num_range_str


def seqRange(sorted_list, gen_range=False):
	""" Generate first and last values, or ranges of values, from sequences.
	"""
	first = None
	for x in sorted_list:
		if first is None:
			first = last = x
		elif x == last+1:
			last = x
		else:
			if gen_range:
				yield range(first, last+1)
			else:
				yield first, last
			first = last = x
	if first is not None:
		if gen_range:
			yield range(first, last+1)
		else:
			yield first, last


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def getBases(path):
	""" Find file sequence bases in path.
		Returns a list of bases (the first part of the filename, stripped of frame number padding and extension).
	"""
	# Get directory contents
	try:
		ls = os.listdir(path)
		ls.sort()
	except OSError:
		print "No such file or directory: '%s'" %path
		return False

	# Create list to hold all basenames of sequences
	all_bases = []

	# Get list of files in current directory
	for filename in ls:

		# Only work on files, not directories, and ignore files that start with a dot
		if os.path.isfile(os.path.join(path, filename)) and not filename.startswith('.'):

			# Extract file extension
			root, ext = os.path.splitext(filename)

			# Match file names which have a trailing number separated by a dot
			seqRE = re.compile(r'\.\d+$')
			match = seqRE.search(root)

			# Store filename prefix
			if match is not None:
				prefix = root[:root.rfind(match.group())]
				all_bases.append('%s.#%s' % (prefix, ext))

	# Remove duplicates & sort list
	bases = list(set(all_bases))
	bases.sort()
	return bases


def getFirst(path):
	""" TEMPORARY BODGE
	"""
	#filter_ls = glob.glob("%s*" %os.path.join(path, base))
	path = path.replace('#', '*')
	filter_ls = glob.glob(path)
	filter_ls.sort()

	return filter_ls[0]


def getSequence(path, pattern):
	""" Looks for other frames in a sequence that fit a particular pattern.
		Pass the first (lowest-numbered) frame in the sequence to the detectSeq function and return its results.
	"""
	#filter_ls = glob.glob("%s*" %os.path.join(path, base))
	pattern = pattern.replace('#', '*')
	filter_ls = glob.glob( os.path.join(path, pattern) )
	filter_ls.sort()
	#frame_ls = []

	return detectSeq( filter_ls[0] )


def detectSeq(filepath):
	""" Detect file sequences based on the provided file path.
		Returns a tuple containing 5 elements:
		1. path - the directory path containing the file
		2. prefix - the first part of the filename
		3. frame - the sequence of frame numbers computed from the numeric part of the filename, represented as a string
		4. ext - the filename extension
		5. num_frames - the number of frames in the sequence
	"""
	lsFrames = [] # Clear frame list

	# Parse file path
	try:
		filename = os.path.basename(filepath)
		path = os.path.dirname(filepath)
		base, ext = os.path.splitext(filename)
		prefix, framenumber = base.rsplit('.', 1)
		padding = len(framenumber)
		framenumber = int(framenumber)
	except ValueError:
		print "Error: could not parse sequence."
		return

	# Construct regular expression for matching files in the sequence
	re_seq_str = r"^%s\.\d{%d}%s$" %( re.escape(prefix), padding, re.escape(ext) )
	#print re_seq_str
	re_seq_pattern = re.compile(re_seq_str)

	# Find other files in the sequence in the same directory
	for item in os.listdir(path):
		if re_seq_pattern.match(item) is not None:
			#lsFrames.append(item) # whole filename
			lsFrames.append( int(os.path.splitext(item)[0].rsplit('.', 1)[1]) ) # just the frame number

	#print "Found %d frames." %len(lsFrames)

	#return lsFrames
	return (path, prefix, numRange(lsFrames, padding=padding), ext, len(lsFrames))
	#return (path, prefix, numRange(lsFrames), ext, len(lsFrames))

