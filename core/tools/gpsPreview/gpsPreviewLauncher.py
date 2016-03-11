#!/usr/bin/python

# [GPS Preview] gpsPreviewLauncher.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Launches GPS Preview UI based on environment.


import os
import gpsPreview__main__


def launch(env=None):
	""" Launches GPS Preview UI based on environment.
	"""
	if not env:
		return
	os.environ['ICARUSENVAWARE'] = env
	reload(gpsPreview__main__)

