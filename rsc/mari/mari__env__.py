#!/usr/bin/python

# mari__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Mari-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	if os.environ['IC_NUKE_EXECUTABLE'] != "":
		os.environ['MARI_NUKEWORKFLOW_PATH'] = os.environ['IC_NUKE_EXECUTABLE']
	os.environ['MARI_DEFAULT_IMAGEPATH'] = os.environ['IC_MARI_SOURCEIMAGES_DIR']
	os.environ['MARI_SCRIPT_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mari/scripts')
	os.environ['MARI_CACHE'] = os.environ['IC_MARI_SCENES_DIR']
	os.environ['MARI_WORKING_DIR'] = os.environ['IC_MARI_SCENES_DIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['IC_SHOTPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH'] = os.environ['IC_MARI_SCENES_DIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH'] = os.environ['IC_MARI_TEXTURES_DIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH'] = os.environ['IC_MARI_TEXTURES_DIR']
	os.environ['MARI_DEFAULT_RENDER_PATH'] = os.environ['IC_MARI_RENDERS_DIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH'] = os.environ['IC_SHOTPUBLISHDIR']
