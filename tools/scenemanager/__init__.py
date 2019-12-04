#!/usr/bin/python

# [scenemanager] __init__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Initialise Scene Manager environment


import os

os.environ['SCNMGR_USER_PREFS_DIR'] = os.environ['IC_USERPREFS']
os.environ['SCNMGR_VENDOR_INITIALS'] = os.environ['IC_VENDOR_INITIALS']
os.environ['SCNMGR_JOB'] = os.environ['IC_JOB']
os.environ['SCNMGR_SHOT'] = os.environ['IC_SHOT']
os.environ['SCNMGR_USER'] = os.environ['IC_USERNAME']
os.environ['SCNMGR_APP'] = os.environ['IC_ENV']

# Define naming conventions.
# Tokens are defined like so: <token>
# Each token must be separated by / . _ -
# Optional tokens should be encased in square brackets.
# No more than one optional section allowed.
os.environ['SCNMGR_CONVENTION'] = "<artist>/<shot>.<discipline>.[<description>.]<version>.ext"
os.environ['SCNMGR_VERSION_CONVENTION'] = "v###"

if os.environ['IC_ENV'] == "STANDALONE":
	pass
elif os.environ['IC_ENV'] == "MAYA":
	os.environ['SCNMGR_SAVE_DIR'] = os.environ['IC_MAYA_SCENES_DIR']
	os.environ['SCNMGR_FILE_EXT'] = ".ma" + os.pathsep + ".mb"
elif os.environ['IC_ENV'] == "HOUDINI":
	os.environ['SCNMGR_SAVE_DIR'] = os.environ['HIP']
	os.environ['SCNMGR_FILE_EXT'] = ".hip"
elif os.environ['IC_ENV'] == "NUKE":
	os.environ['SCNMGR_SAVE_DIR'] = os.environ['IC_NUKE_SCRIPTS_DIR']
	os.environ['SCNMGR_FILE_EXT'] = ".nk" + os.pathsep + ".nknc"
