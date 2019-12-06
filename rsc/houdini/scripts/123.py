#!/usr/bin/python

# [Icarus] 123.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Houdini initialisation.


import os
import sys

# Set environment (should be done first)
os.environ['IC_ENV'] = 'HOUDINI'

import hou
import hdefereval
# from shared import os_wrapper

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
from core.app_session import *

#from rsc.houdini.scripts import houdini_ops

# Remove default user shelf set
#try:
#	os_wrapper.remove(os.path.join(os.environ['HOUDINI_USER_PREF_DIR'], 'toolbar', 'default.shelf'))
#except OSError:
#	pass

# Add HDAs
#houdini_ops.add_hdas()

def init_uis():
	""" Initialise PySide UI objects. This should be deferred until after
		Houdini has initialised its own UI so that the PySide UIs can be
		properly parented to the Houdini main window.
	"""
	# Initialise Icarus
	from core import icarus
	session.icarus = icarus.app(app='houdini')

	# Initialise Scene Manager
	from tools.scenemanager import scenemanager
	session.scnmgr = scenemanager.create(app='houdini')

	# Set shot defaults
	session.scnmgr.set_defaults()

hdefereval.executeDeferred(init_uis)
