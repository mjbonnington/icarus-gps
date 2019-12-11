#!/usr/bin/python

# [Icarus] json_data.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Class for handling generic JSON data files.
# Classes written to handle specific data files should inherit this class.


import os
import json

# Import custom modules
from . import verbose


class JSONData(object):
	""" Class for JSON data.
	"""
	def __init__(self, datafile=None):
		""" Initialise class. If datafile is not specified, create bare
			class. The data should then be loaded with the load() method.
		"""
		verbose.debug("Class: %s" % self)

		self.prefs_dict = {}
		if datafile is not None:
			self.load(datafile)


	def load(self, datafile):
		""" Load data from datafile and store in a dictionary.
		"""
		self.datafile = os.path.normpath(datafile)
		return self.reload()


	def reload(self):
		""" Reload data from current datafile.
		"""
		try:
			with open(self.datafile, 'r') as f:
				self.prefs_dict = json.load(f)
			verbose.print_('JSON load: "%s"' % self.datafile)
			return True

		except IOError:
			verbose.warning('JSON file is invalid or doesn\'t exist: "%s"' % self.datafile)
			return False


	def save(self):
		""" Save prefs dictionary to datafile.
		"""
		try:
			with open(self.datafile, 'w') as f:
				json.dump(self.prefs_dict, f, indent=4, sort_keys=True)
			verbose.print_('JSON save: "%s"' % self.datafile)
			return True

		except IOError:
			verbose.error('JSON file could not be written: "%s"' % self.datafile)
			return False


	def clear(self):
		""" Clear all data from the prefs dictionary.
		"""
		self.prefs_dict.clear()
