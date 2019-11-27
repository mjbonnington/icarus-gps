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
	filename=filename.replace(
		os.environ['FILESYSTEMROOTWIN'], os.environ['FILESYSTEMROOT'])
	filename=filename.replace(
		os.environ['FILESYSTEMROOTOSX'], os.environ['FILESYSTEMROOT'])
	filename=filename.replace(
		os.environ['FILESYSTEMROOTLINUX'], os.environ['FILESYSTEMROOT'])
	return filename

# Adding to Nuke path
nuke.pluginAddPath('../gizmos')
nuke.pluginAddPath('../icons')
nuke.pluginAddPath('../scripts')
nuke.pluginAddPath('../plugins')
# Third-party locations
nuke.pluginAddPath('../gizmos/cryptomatte')
nuke.pluginAddPath('../gizmos/pixelfudger')

# Nuke seems to ditch the main root environment where it has been called from
# so the path needs to be appended again.
# sys.path.append(os.environ['IC_WORKINGDIR'])
from core import env__init__
env__init__.appendSysPaths()
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
	nuke.addFavoriteDir('Scripts', os.environ['NUKESCRIPTSDIR'])
	nuke.addFavoriteDir('Renders', os.environ['NUKERENDERSDIR'])
	nuke.addFavoriteDir('Elements', os.environ['NUKEELEMENTSDIR'])
	nuke.addFavoriteDir('Plate', os.path.join('[getenv IC_SHOTPATH]', 'Plate'))
	nuke.addFavoriteDir('Elements Library', os.environ['ELEMENTSLIBRARY'])
except KeyError:
	pass

# Plate format
# plateFormat = '%s %s %s' % (int(os.environ['RESOLUTIONX']), int(os.environ['RESOLUTIONY']), os.environ['IC_SHOT'])
# proxyFormat = '%s %s %s' % (int(os.environ['PROXY_RESOLUTIONX']), int(os.environ['PROXY_RESOLUTIONY']), '%s_proxy' % os.environ['IC_SHOT'])
# nuke.addFormat(plateFormat)
# nuke.addFormat(proxyFormat)
# nuke.knobDefault('Root.format', os.environ['IC_SHOT'])
# nuke.knobDefault('Root.proxy_type', 'format')
# nuke.knobDefault('Root.proxy_format', '%s_proxy' % os.environ['IC_SHOT'])
# nuke.knobDefault('Root.fps', os.environ['FPS'])
# nuke.knobDefault('Root.first_frame', os.environ['STARTFRAME'])
# nuke.knobDefault('Root.last_frame', os.environ['ENDFRAME'])
