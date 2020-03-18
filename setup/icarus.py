#!/usr/bin/python

# [Icarus] icarus.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019-2020
#
# Launch Icarus and parse command-line arguments. Place each version of Icarus
# in a folder with the same name as its version, i.e. 'v0.10.0' (without
# quotes). Ensure that a script named 'run.py' exists in each version folder
# to launch that specific version. Place this script in the same folder as
# all the version folders.


import argparse
import glob
import os
import subprocess

cwd = os.path.dirname(os.path.realpath(__file__))

# Define pattern to detect versions
version_pattern = '*'

# Define name of command to run Icarus
run_cmd = 'run.py'


def get_versions(base_dir, pattern):
	""" Match version folders based on the given pattern and return as a list.
	"""
	matches = []
	search_pattern = os.path.join(base_dir, pattern)

	for filepath in glob.glob(search_pattern):
		# Only add directories
		if os.path.isdir(filepath):
			matches.append(os.path.basename(filepath))

	return matches


def get_latest(available_versions):
	""" Return the latest version from the list of available versions.
	"""
	v = {}
	for version in available_versions:
		try:  # Convert version to int
			v_split = version.lstrip('v').split('.')
			v_int = int(v_split[0])*10000 + int(v_split[1])*100 + int(v_split[2])
			v[v_int] = version
		except (ValueError, KeyError):
			pass

	try:
		return v[max(v)]
	except (ValueError, KeyError):
		return None


def print_versions(available_versions):
	""" Output list of available versions.
	"""
	print("available versions:")
	for version in available_versions:
		print("  " + version)


def run():
	""" Parse command-line arguments and execute command.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--version', help="launch specific version")
	parser.add_argument("-a", "--allversions", 
		action='store_true', help="list all versions")
	parser.add_argument('-u', '--user', help="override username")
	args = parser.parse_args()
	kwargs = vars(args)

	available_versions = get_versions(cwd, version_pattern)

	# Set user override
	if args.user:
		print("override username: %s" % args.user.lower())
		os.environ['IC_USERNAME'] = args.user.lower()

	# List all versions
	if args.allversions:
		print_versions(available_versions)
		return 0

	# Set version
	if args.version:
		if args.version in available_versions:
			exec_str = os.path.join(cwd, args.version, run_cmd)
			subprocess.call(exec_str, shell=True)
		else:
			print("error: version %s does not exist." % args.version)
			print_versions(available_versions)
			return -1
	else:
		exec_str = os.path.join(cwd, get_latest(available_versions), run_cmd)
		subprocess.call(exec_str, shell=True)


if __name__ == '__main__':
	run()
