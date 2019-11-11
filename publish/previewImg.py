#!/usr/bin/python

# [Icarus] previewImg.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Loads asset preview image.


import os


def getImg(gatherPath, forceExt=None):
	gatherPathLs = os.listdir(gatherPath)
	img = ''
	for item_ in gatherPathLs:
		if item_.startswith('preview.'):
			if forceExt:
				if item_.endswith(forceExt):
					img = item_
					break
			else:
				img = item_
				break
	if img:
		return os.path.join(gatherPath, img)
	else:
		return

