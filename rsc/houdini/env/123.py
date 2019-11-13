#!/usr/bin/python

# [GPS] 123.py
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

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
from core.app_session import *

#from rsc.houdini.scripts import houdini_ops
from core import icarus
# from shared import os_wrapper

#removing default user shelf set
#try:
#    os_wrapper.remove(os.path.join(os.environ['HOUDINI_USER_PREF_DIR'], 'toolbar', 'default.shelf'))
#except OSError:
#    pass

# Add HDAs
#houdini_ops.add_hdas()

# Set shot defaults
#houdini_ops.set_defaults()

# Initialise Icarus
#hou.session.icarus = icarus.app(app='nuke')  # Use Houdini session object
session.icarus = icarus.app(app='nuke')  # Use Icarus session object
