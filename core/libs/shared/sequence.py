#!/usr/bin/env python

# [Icarus] sequence.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# These functions convert formatted sequences to lists and vice-versa.


import re


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


def numRange(num_int_list, quiet=False):
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
				num_range_str = num_range_str + "%d, " %first
			else:
				num_range_str = num_range_str + "%d-%d, " %(first, last)
			first = last = x
	if first is not None:
		if first == last:
			num_range_str = num_range_str + "%d" %first
		else:
			num_range_str = num_range_str + "%d-%d" %(first, last)

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
