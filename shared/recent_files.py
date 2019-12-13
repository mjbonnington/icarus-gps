#!/usr/bin/python

# [Icarus] recent_files.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019
#
# Manage recent file lists for various applications within the pipeline.


import os

# Import custom modules
from . import json_data
from . import os_wrapper
from . import verbose


class RecentFiles(json_data.JSONData):
	""" Class for storing and manipulating recent files data.
		Inherits JSONData class.
	"""

	def put(self, new_entry, app=os.environ['IC_ENV']):
		""" Add an entry to the recent files list and save file to disk.
		"""
		app = app.lower()  # Make app key case-insensitive

		try:
			filelist = self.prefs_dict[os.environ['IC_SHOT']][app]
		except KeyError:
			filelist = []  # Clear recent file list

		# Make path relative to current shot
		new_entry = os_wrapper.relativePath(new_entry, 'IC_SHOTPATH')

		# If entry already exists in list, delete it
		if new_entry in filelist:
			filelist.remove(new_entry)

		# Prepend entry to list
		filelist.insert(0, new_entry)

		# Limit list to specific size
		while len(filelist) > int(os.environ.get('IC_NUMRECENTFILES', 10)):
			filelist.pop()

		# Create data structure
		shotkey = os.environ['IC_SHOT']
		# self.prefs_dict[shotkey] = {app: filelist}
		try:  # Add updated filelist to existing key
			self.prefs_dict[shotkey][app] = filelist
		except KeyError:  # Create new key for updated filelist
			self.prefs_dict[shotkey] = {app: filelist}

		# Write to disk
		if self.save():
			verbose.print_("Added '%s' to recent files list." % new_entry)
		else:
			verbose.warning("Entry '%s' could not be added to recent files list." % new_entry)


	def get(self, app=os.environ['IC_ENV']):
		""" Read recent file list and return list.
		"""
		app = app.lower()  # Make app key case-insensitive

		try:
			filelist = self.prefs_dict[os.environ['IC_SHOT']][app]

			# Slice the list to specific size
			filelist = filelist[:int(os.environ.get('IC_NUMRECENTFILES', 10))]

		except:
			filelist = []

		return filelist


datafile = os_wrapper.absolutePath('$IC_RECENTFILESDIR/$IC_JOB.json')
recents = RecentFiles(datafile)
