#!/usr/bin/python

# [Icarus] run.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Launch standalone application and parse command-line arguments.


import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-j', '--job', help="set job")
parser.add_argument('-s', '--shot', help="set shot")
parser.add_argument('-u', '--user', help="override username")
parser.add_argument('-v', '--verbosity', 
	type=int, choices=range(0, 5), default=-1, help="output verbosity level")
parser.add_argument('-c', '--config', help="override config directory")
parser.add_argument("-e", "--expert", 
	action='store_true', help="start in expert mode")
args = parser.parse_args()
kwargs = vars(args)

# Set user override
# Note: this must be done before importing the Icarus package.
# TODO: sanitise username
if args.user:
	os.environ['IC_USERNAME'] = args.user.lower()

# Set verbosity
if args.verbosity != -1:
	os.environ['IC_VERBOSITY'] = str(args.verbosity)

# Set config dir
if args.config:
	os.environ['IC_CONFIGDIR'] = args.config

# Set expert mode
os.environ['IC_EXPERT_MODE'] = str(args.expert)

# Run Icarus and pass in command-line arguments ------------------------------
if __name__ == '__main__':
	# print kwargs
	from core import icarus
	icarus.standalone(**kwargs)
