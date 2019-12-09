#!/usr/bin/python

# hiero__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Hiero / HieroPlayer-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['IC_HIERO_EDITORIAL_DIR'] = os_wrapper.absolutePath('$IC_JOBPATH/../Editorial/Hiero')  # Shouldn't hardcode this

	os.environ['HIERO_PLUGIN_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/hiero')
