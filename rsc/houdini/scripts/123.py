#!/usr/bin/python

# [Icarus] 123.py
#
# Mike Bonnington <michael.bonnington@hogarthww.com>
# (c) 2019 Gramercy Park Studios
#
# Houdini initialisation.


import os
import sys

# Set environment (should be done first)
os.environ['IC_ENV'] = 'HOUDINI'

import hou
# from shared import os_wrapper

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
# from core.app_session import *

#from rsc.houdini.scripts import houdini_ops

# Remove default user shelf set
#try:
#    os_wrapper.remove(os.path.join(os.environ['HOUDINI_USER_PREF_DIR'], 'toolbar', 'default.shelf'))
#except OSError:
#    pass

# Add HDAs
#houdini_ops.add_hdas()

# Initialise Icarus
from core import icarus
hou.session.icarus = icarus.app(app='houdini')

# Initialise Scene Manager
from tools.scenemanager import scenemanager
hou.session.scnmgr = scenemanager.create(app='houdini')

# Set shot defaults
hou.session.scnmgr.set_defaults()
