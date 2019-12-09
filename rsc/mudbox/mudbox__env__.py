#!/usr/bin/python

# mudbox__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Mudbox-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['MUDBOX_PLUG_IN_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mudbox/plugins')
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = "60"
