#!/usr/bin/python
#support   :Nuno Pereira - nuno.pereira@gps-ldn.com
#support   :Mike Bonnington - mike.bonnington@gps-ldn.com
#title     :init.py
#copyright :Gramercy Park Studios

# This file contains Nuke's initializing procedures
import os, sys

# Set up path remapping for cross-platform support
def filenameFix(filename):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		return filename.replace( os.environ['JOBSROOTOSX'], os.environ['JOBSROOTWIN'] )
	else: # Linux or OS X
		return filename.replace( os.environ['JOBSROOTWIN'], os.environ['JOBSROOTOSX'] )

# Adding to Nuke path
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./scripts')
nuke.pluginAddPath('./plugins')
# Third-party locations
nuke.pluginAddPath('./gizmos/pxf')

# Nuke seems to ditch the main root environent where it has been called from so the path needs to be appended again.
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core', 'ui'))
import env__init__
env__init__.appendSysPaths()
# Nuke opens a entire new Nuke process with 'File>New Script' and doesn't simply create and empty script in the current env.
# The Icarus env has to be set temporarily as NUKE_TMP to avoid Icarus detecting an existing Nuke env and opening its UI automatically.
os.environ['ICARUSENVAWARE'] = 'NUKE_TMP'
import icarus__main__, gpsNodes
os.environ['ICARUSENVAWARE'] = 'NUKE'

# Third-party initializations go here


# Shot directories
nuke.addFavoriteDir('Scripts', os.environ['NUKESCRIPTSDIR'])
nuke.addFavoriteDir('Renders', os.environ['NUKERENDERSDIR'])
nuke.addFavoriteDir('Elements', os.environ['NUKEELEMENTSDIR'])
nuke.addFavoriteDir('Plate', os.path.join('[getenv SHOTPATH]', 'Plate'))
nuke.addFavoriteDir('Elements Library', os.environ['ELEMENTSLIBRARY'])

# Plate format
plateFormat = '%s %s %s' % (int(os.environ['RESOLUTIONX']), int(os.environ['RESOLUTIONY']), os.environ['SHOT'])
proxyFormat = '%s %s %s' % (int(os.environ['PROXY_RESOLUTIONX']), int(os.environ['PROXY_RESOLUTIONY']), '%s_proxy' % os.environ['SHOT'])
nuke.addFormat(plateFormat)
nuke.addFormat(proxyFormat)
nuke.knobDefault('Root.format', os.environ['SHOT'])
nuke.knobDefault('Root.proxy_type', 'format')
nuke.knobDefault('Root.proxy_format', '%s_proxy' % os.environ['SHOT'])
nuke.knobDefault('Root.fps', os.environ['FPS'])
nuke.knobDefault('Root.first_frame', os.environ['STARTFRAME'])
nuke.knobDefault('Root.last_frame', os.environ['ENDFRAME'])
