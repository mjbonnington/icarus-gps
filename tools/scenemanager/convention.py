#!/usr/bin/python

# [scenemanager] convention.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Controls the naming convention and  versioning of files.


import os
import glob
import re

# Import custom modules
from shared import os_wrapper
from shared import verbose


__padding__ = 3
__min_version__ = 0
__max_version__ = 999


def get_latest(file_list):
	""" Detect the latest version of a file from the provided list of files.
		Return a list of files containing only the latest versions.
	"""
	seq = get_versions(file_list)
	matches = []
	# print "\n---debug---"
	# import json
	# print(json.dumps(seq, indent=4, sort_keys=True))
	# print "-----------\n"

	# Find latest version
	for prefix, value in seq.iteritems():
		versions = []
		for ver, path in value.iteritems():
			versions.append(int(ver))
		# print prefix, max(versions)
		latest = max(versions)
		matches.append(value[latest])

	return matches


def get_versions(file_list):
	""" Detect versions of a file from the provided list of files.
		Return a nested dictionary in the format:

		base_file_prefix: {
			version: filepath, 
			version: filepath
		}, 
		base_file_prefix: {
			version: filepath
		}
		...
		etc.
	"""
	seq = {}

	for filepath in file_list:
		filepath = os_wrapper.absolutePath(filepath)
		meta = parse(filepath)
		if '<description>' in meta:
			prefix = ".".join([meta['<shot>'], meta['<discipline>'], meta['<description>']])
		else:
			prefix = ".".join([meta['<shot>'], meta['<discipline>']])
		v_int = version_to_int(meta['<version>'])
		try:
			seq[prefix][v_int] = filepath
		except KeyError:
			seq[prefix] = {v_int: filepath}

	return seq


def parse(
	filepath, 
	base_dir=os.environ['SCNMGR_SAVE_DIR'], 
	convention=os.environ['SCNMGR_CONVENTION']):
	""" Parse the given filepath (relative to base_dir) based on a naming
		convention and return a dictionary of elements for processing.
		TODO: check shot, artist, discipline etc. against valid whitelist
	"""
	if not os.path.isfile(filepath):
		verbose.print_("Could not parse filename as file doesn't exist: %s" % filepath)
		return None

	filepath = os.path.normpath(filepath)
	base_dir = os.path.normpath(base_dir)

	# Make filepath relative to base_dir
	if filepath.startswith(base_dir):
		filepath = filepath.replace(base_dir, '', 1)
		filepath = filepath.replace('\\', '/')  # Convert to forward slashes
		if filepath.startswith('/'):
			filepath = filepath.replace('/', '', 1)  # Remove leading slash

	# Find optional parts in naming convention
	# (only one optional section is allowed, if there are more, all optional
	# parts will be ignored.)
	valid_conventions = [convention.replace('[', '').replace(']', '')]
	pattern = r'\[.+?\]'
	optionals = re.findall(pattern, convention)
	if len(optionals) == 1:
		for i, optional in enumerate(optionals):
			valid_conventions.append(convention.replace(optional, '', i+1))
	# print valid_conventions

	# # Find tokens in naming convention
	# pattern = r'<\w+>'
	# tokens = re.findall(pattern, convention)

	# # Remove duplicates & sort list
	# tokens = list(set(tokens))
	# # tokens.sort()
	# print tokens

	# # Generate regular expression to represent naming convention

	token_dict = {}
	success = False
	f = explode_path(filepath)
	for con in valid_conventions:
		c = explode_path(con)

		if same_structure(f, c):
			for i, dirs in enumerate(c):
				for j, token in enumerate(dirs):
					value = f[i][j]
					if token in token_dict:  # Sanity check duplicated tokens
						if token_dict[token] != value:
							verbose.error("Could not parse filename due to a token value mismatch.")
							return None
					else:
						token_dict[token] = value

			success = True

	if success:
		# print(token_dict)
		return token_dict

	else:
		msg = "The filename '%s' could not be parsed because it does not comply with the naming convention." % filepath
		for con in valid_conventions:
			msg += "\n" + con
		verbose.error(msg)
		return None


def explode_path(filepath):
	""" Return a list from a path. First split into directories, then by a
		delimiter character such as '.'
	"""
	path_elem = []
	for d in filepath.split('/'):
		path_elem.append(d.split('.'))
	return path_elem


def same_structure(a, b):
	""" Check if two exploded paths (a and b) have the same structure.
	"""
	x = []; y = []
	for i in a:
		x.append(len(i))
	for j in b:
		y.append(len(j))
	if x==y:
		return True
	else:
		return False


def version_to_int(v_str):
	""" Convert a version string in the format 'v###' to an integer.
		TODO: fail elegantly if v_str is not in the correct format.
	"""
	# if v_str.startswith('v'):
	try:
		return int(v_str.replace('v', '', 1))
	except:
		verbose.warning("Malformed version string: %s" % v_str)
		return -1  # Hack to deal with malformed version strings


def version_to_str(v_int):
	""" Convert an integer to a version string in the format 'v###'.
	"""
	padding = os.environ['SCNMGR_VERSION_CONVENTION'].count('#')
	return 'v' + str(v_int).zfill(padding)


def version_up(base_file):
	""" Detect the version from the given file, and return the filepath with
		the version number incremented.
	"""
	meta = parse(base_file)
	v_int = version_to_int(meta['<version>'])
	v_str = version_to_str(change_version(v_int, 1))

	return base_file.replace(meta['<version>'], v_str)


def version_next(base_file):
	""" Find all related versions of base_file and return a path to the next
		version numerically.
	"""
	meta = parse(base_file)

	shot = meta['<shot>']
	discipline = meta['<discipline>']
	try:
		description = meta['<description>']
	except KeyError:
		description = ""

	return version_next_meta(shot, discipline, description)[0]


def version_next_meta(shot, discipline, description=""):
	""" Find all related versions and return a tuple containing the path to
		the new version, and the number of existing related versions.
	"""
		#os.environ['SCNMGR_CONVENTION'] = "<shot>.<discipline>.[description].<version>.ext"
		# valid_tokens = {
		# 	'<user>': 'SCNMGR_USER', 
		# 	'<user-initials>': 'SCNMGR_USER_INITIALS', 
		# 	'<job>': 'SCNMGR_JOB', 
		# 	'<shot>': 'SCNMGR_SHOT', 
		# 	'<discipline>': 'SCNMGR_DISCIPLINE', 
		# }

		# filename = os.environ['SCNMGR_CONVENTION']
		# filename = filename.replace('<artist>', os.environ['SCNMGR_USER'])
		# filename = filename.replace('<shot>', os.environ['SCNMGR_SHOT'])
		# filename = filename.replace('<discipline>', discipline)
		# filename = filename.replace('[description]', description)
		# filename = filename.replace('<version>', v_str)
		# computed_filename = filename + self.file_ext[0]  # Append file extension

	# Generate filter to search for related versions
	# TODO: make compliant with alt naming and padding conventions
	if description == "":
		ff = ".".join([shot, discipline])
	else:
		ff = ".".join([shot, discipline, description])
	file_filter = "*/%s.v*" % ff

	# Detect the latest version
	existing_versions = match_files(
			os.environ['SCNMGR_SAVE_DIR'], file_filter)
	matches_latest = get_latest(existing_versions)
	if matches_latest:
		n = len(existing_versions)
		computed_filename = os.path.basename(version_up(matches_latest[0]))
		filename = os.path.join(
			os.environ['SCNMGR_SAVE_DIR'], 
			os.environ['SCNMGR_USER'], 
			computed_filename)
		return filename, n

	else:
		return None, 0


def change_version(input_version, value, absolute=False):
	""" Change the version number.
		If absolute is True, set the version to the given value.
		Otherwise, adjust the existing value by the given value.
	"""
	if absolute:
		new_version = value
	else:
		new_version = input_version + value

	# Ensure the new value is within the allowed range
	if __min_version__ <= new_version <= __max_version__:
		return new_version
	else:
		verbose.error("Version number out of bounds.")
		return input_version


def generate_filter(
	shot=os.environ['SCNMGR_SHOT'], 
	discipline=None, 
	artist=None, 
	description=None):
	""" Update the search filter to show filenames based on the currently
		selected values, which match the naming convention described in
		the environment variable 'SCNMGR_CONVENTION'.
	"""
	ignore_list = ["[any]", "[please select]", "", None]

	# Current naming convention for reference:
	# <artist>/<shot>.<discipline>.[<description>.]<version>.ext

	# Remove file extension
	file_filter = os.path.splitext(os.environ['SCNMGR_CONVENTION'])[0]

	# Replace compulsory tokens
	file_filter = file_filter.replace("<shot>", shot)

	# Replace known tokens
	if discipline not in ignore_list:
		file_filter = file_filter.replace("<discipline>", discipline)
	if artist not in ignore_list:
		file_filter = file_filter.replace("<artist>", artist)
	if description not in ignore_list:
		file_filter = file_filter.replace("<description>", description)

	# Replace unspecified tokens with wildcards
	file_filter = file_filter.replace("<artist>", "*")
	file_filter = file_filter.replace("<discipline>", "*")

	if description:
		file_filter = file_filter.replace("[", "")
		file_filter = file_filter.replace("]", "")
		file_filter = file_filter.replace("<version>", "*")
	else:
		file_filter = file_filter.replace("[<description>.]<version>", "*")

	# print file_filter
	return file_filter


def match_files(base_dir, file_filter):
	""" Match files based on the convention given in file_filter and
		return as a list.
	"""
	file_extensions = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

	matches = []
	for filetype in file_extensions:
		search_pattern = os.path.join(base_dir, file_filter+filetype)

		for filepath in glob.glob(search_pattern):
			# Only add files, not directories or symlinks
			if os.path.isfile(filepath) \
			and not os.path.islink(filepath):
				filepath = os_wrapper.absolutePath(filepath)
				matches.append(filepath)

	return matches
