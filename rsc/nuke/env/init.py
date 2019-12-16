#!/usr/bin/python

# [Icarus] init.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Nuke initialisation.


import os
import sys

# Set environment (should be done first)
os.environ['IC_ENV'] = 'NUKE'

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
from core.app_session import *

# Set up path remapping for cross-platform support
def filenameFix(filename):
	filename = filename.replace(
		os.environ['IC_FILESYSTEM_ROOT_WIN'], 
		os.environ['IC_FILESYSTEM_ROOT'])
	filename = filename.replace(
		os.environ['IC_FILESYSTEM_ROOT_OSX'], 
		os.environ['IC_FILESYSTEM_ROOT'])
	filename = filename.replace(
		os.environ['IC_FILESYSTEM_ROOT_LINUX'], 
		os.environ['IC_FILESYSTEM_ROOT'])
	return filename

# Add locations to Nuke path
nuke.pluginAddPath('../gizmos')
nuke.pluginAddPath('../icons')
nuke.pluginAddPath('../scripts')
nuke.pluginAddPath('../plugins')
# Third-party locations
nuke.pluginAddPath('../gizmos/cryptomatte')
nuke.pluginAddPath('../gizmos/pixelfudger')

# Nuke seems to ditch the main root environment where it has been called from
# so the path needs to be appended again.
# sys.path.append(os.environ['IC_COREDIR'])
from core import icarus__env__
icarus__env__.append_sys_paths()
# Nuke opens a entire new Nuke process with 'File>New Script' and doesn't
# simply create an empty script in the current env.
# The Icarus env has to be set temporarily as NUKE_TMP to avoid Icarus
# detecting an existing Nuke env and opening its UI automatically.
# os.environ['IC_ENV'] = 'NUKE_TMP'
# import icarus__main__
from rsc.nuke.scripts import gpsNodes
# os.environ['IC_ENV'] = 'NUKE'

# Third-party initializations go here
import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()
import collectFiles
import multiEdit

# Shot directories
try:
	nuke.addFavoriteDir('Scripts', os.environ['IC_NUKE_SCRIPTS_DIR'])
	nuke.addFavoriteDir('Renders', os.environ['IC_NUKE_RENDERS_DIR'])
	nuke.addFavoriteDir('Elements', os.environ['IC_NUKE_ELEMENTS_DIR'])
	nuke.addFavoriteDir('Plate', os.path.join('[getenv IC_SHOTPATH]', 'plate'))
	nuke.addFavoriteDir('Elements Library', os.environ['IC_ELEMENTS_LIBRARY'])
except KeyError:
	pass
