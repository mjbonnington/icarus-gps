#!/usr/bin/python

# realflow__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set RealFlow-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['RF_RSC'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow')
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow/scripts/startup.rfs')
	os.environ['RFOBJECTSPATH'] = os_wrapper.absolutePath('$IC_SHOTPUBLISHDIR/ma_geoCache/realflow')
