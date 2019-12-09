#!/usr/bin/python

# c4d__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Cinema 4D-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['C4D_PLUGINS_DIR'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/C4D/$IC_C4D_VERSION/plugins')
	os.environ['C4D_SCRIPTS_DIR'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/C4D/$IC_C4D_VERSION/scripts')
