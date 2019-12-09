#!/usr/bin/python

# nuke__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Nuke-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['NUKE_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/nuke') + os.pathsep \
	                        + os_wrapper.absolutePath('$IC_BASEDIR/rsc/nuke/env')
