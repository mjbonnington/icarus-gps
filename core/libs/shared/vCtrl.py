#!/usr/bin/python

# [Icarus] vCtrl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Manage version control for assets.


import os
import string


def version(vCtrlFolder, current=False):
	""" Determine current version based on vc or directory contents.
	"""
	# Check if directory exists
	if os.path.isdir(vCtrlFolder):
		# Try to figure out versioning based on existing contents
		try:
			vCtrlFileLs = os.listdir(vCtrlFolder)
			vrsLs = []
			# Check all items in vCtrlFolder for 'v###' pattern
			for vCtrlItem in vCtrlFileLs:
				# Get first item of split list if _ found to strip out 'approved' from version
				contentVrs = vCtrlItem.split("_")[0]
				# If found strip 'v'
				if contentVrs.startswith("v"):
					contentVrs = contentVrs.replace("v", "")
				elif contentVrs.startswith(".v"):
					contentVrs = contentVrs.replace(".v", "")
				# Check for numeral(s) and add to vrsLs
				if contentVrs.isdigit():
					vrsLs.append(contentVrs)
			# Sort vrsLs and retrieve last item (highest digit)
			vrsLs.sort()
			# print(vrsLs)
			currentVersion = int(vrsLs[-1])

		# If no versioning detected in contents start new versioning
		except IndexError:
			currentVersion = 0
	else:
		print("vCtrl: directory doesn't exist.")
		currentVersion = 0

	# Padding control and versioning increment
	if current:
		newVersion = currentVersion
	else:
		newVersion = currentVersion + 1

	# Prepend 'v' and padding to version
	newVersion = "v%03d" %newVersion

	return newVersion

