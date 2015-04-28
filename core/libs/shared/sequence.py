#!/usr/bin/env python

import re


def numList(num_range_str):
	""" Takes a formatted string describing a range of numbers and returns a sorted integer list.
		e.g. '1-5, 20, 24, 1001-1002'
		returns [1, 2, 3, 4, 5, 20, 24, 1001, 1002]
	"""
	num_int_list = []
	num_format = re.compile(r'^\d+$')
	seq_format = re.compile(r'^\d+-\d+$')

	# split into groups of ranges separated by commas
	grps = re.split(r',\s*', num_range_str)
	for grp in grps:

		# grp is a single number (e.g. 10)
		if num_format.match(grp) is not None:
			num_int_list.append(int(grp))

		# grp is a number sequence (e.g. 1-10)
		elif seq_format.match(grp) is not None:
			seq = re.split(r'-', grp)
			first = int(seq[0])
			last = int(seq[1])
			if first >= last:
				print "ERROR: The first number (%d) in the sequence must be smaller than the last (%d)." %(first, last)
				return False
			else:
				int_list = list(range(first, last+1))
				for num in int_list:
					num_int_list.append(num)

		else:
			print "ERROR: Sequence format is invalid."
			return False

	# remove duplicates & sort list
	return sorted(list(set(num_int_list)), key=int)


def numRange(num_int_list):
	""" Takes a list of integer values and returns a formatted string describing the range of numbers.
		e.g. [1, 2, 3, 4, 5, 20, 24, 1001, 1002]
		returns '1-5, 20, 24, 1001-1002'
	"""
	num_range_str = ''

	# remove duplicates & sort list
	try:
		sorted_list = sorted(list(set(num_int_list)), key=int)
	except (ValueError, TypeError):
		print "ERROR: Number list only works woth integer values."
		return False
		

	# find sequences
	first = None
	for x in sorted_list:
		if first is None:
			first = last = x
		elif x == last+1:
			last = x
		else:
			#yield first, last
			if first == last:
				num_range_str = num_range_str + "%d, " %first
			else:
				num_range_str = num_range_str + "%d-%d, " %(first, last)
			first = last = x
	if first is not None:
		#yield first, last
		if first == last:
			num_range_str = num_range_str + "%d" %first
		else:
			num_range_str = num_range_str + "%d-%d" %(first, last)

	return num_range_str
