#!/usr/bin/python

# [Icarus] launch.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017-2018 Gramercy Park Studios
#
# Initialises Icarus environment without showing any UI.
# NOT IN USE
# ***WIP*** - look into using __init__.py for env initialisation


import argparse
import os

# Store existing environmnet variables
environ = dict(os.environ)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--job', help="set job")
parser.add_argument('-s', '--shot', help="set shot")
parser.add_argument('-u', '--user', help="override username")
parser.add_argument('-a', '--allvars', action='store_true', default=False,
                    dest='allvars', help="print all environment variables")
args = parser.parse_args()
if args.user:
	os.environ['IC_USERNAME'] = args.user.lower()

# Initialise Icarus environment and add libs to sys path
import env__init__
env__init__.setEnv()

# Import custom modules
import jobs

if args.job and args.shot:
	jobs_data = jobs.Jobs()
	jobs_data.setup(args.job, args.shot, storeLastJob=False)

if __name__ == '__main__':
	try:
		for key in os.environ.keys():
			if args.allvars:  # Print all env vars
				print("%30s = %s" %(key, os.environ[key]))
			elif key not in environ:  # 
				print("%30s = %s" %(key, os.environ[key]))
	except KeyError:
		print("Environment variable(s) not set.")
