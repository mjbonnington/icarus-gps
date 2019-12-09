#!/usr/bin/python

# djv__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set djv-view-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['DJV_PLAY'] = os.environ['IC_DJV_EXECUTABLE']
	os.environ['DJV_LIB']  = os_wrapper.absolutePath('%s/../lib' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))
	if os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert.exe' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))
	else:  # Mac OS X and Linux
		os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))
