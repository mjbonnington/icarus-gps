#!/usr/bin/python

# [Icarus] recent_shots.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019
#
# Manage recent shots list.


import os

# Import custom modules
from . import json_data
from . import os_wrapper
from . import verbose


class RecentShots(json_data.JSONData):
	""" Class for storing and manipulating recent shots data.
		Inherits JSONData class.
	"""

	def put(self, job, shot):
		""" Add an entry to the recent shots list and save file to disk.
		"""
		new_entry = [job, shot]

		try:
			shotlist = self.prefs_dict['shots']
		except KeyError:
			shotlist = []  # Clear recent shot list

		# If entry already exists in list, delete it
		if new_entry in shotlist:
			shotlist.remove(new_entry)

		# Prepend entry to list
		shotlist.insert(0, new_entry)

		# Limit list to specific size
		while len(shotlist) > int(os.environ.get('IC_NUMRECENTFILES', 10)):
			shotlist.pop()

		# Create data structure
		self.prefs_dict['shots'] = shotlist

		# Write to disk
		if self.save():
			verbose.print_("Added %s to recent shots list." % new_entry)
		else:
			verbose.warning("Entry %s could not be added to recent shots list." % new_entry)


	def get(self, last=False):
		""" Read recent shots list and return list.
		"""
		try:
			shotlist = self.prefs_dict['shots']

			# Slice the list to specific size
			shotlist = shotlist[:int(os.environ.get('IC_NUMRECENTFILES', 10))]

		except:
			shotlist = []

		if last:
			return shotlist[0]
		else:
			return shotlist


datafile = os_wrapper.absolutePath('$IC_RECENTFILESDIR/shots.json')
recents = RecentShots(datafile)
