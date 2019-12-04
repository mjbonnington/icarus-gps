#!/usr/bin/python

# [Icarus] settings_data_json.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Manipulates settings data stored in a JSON file.


import json


class SettingsData(object):
	""" Settings data class for JSON prefs data.
	"""
	def __init__(self, prefs_file):
		self.prefs_file = prefs_file
		self.prefs_dict = {}
		self.read()

	def read_new(self, prefs_file):
		self.prefs_file = prefs_file
		self.read()

	def read(self):
		try:
			with open(self.prefs_file, 'r') as f:
				self.prefs_dict = json.load(f)
		except:
			pass

	def write(self):
		try:
			with open(self.prefs_file, 'w') as f:
				json.dump(self.prefs_dict, f, indent=4, sort_keys=True)
			return True
		except:
			return False

	def getValue(self, category, attr, default=None):
		try:
			key = "%s.%s" % (category, attr)
			return self.prefs_dict[key]
		except KeyError:
			if default is not None:
				self.prefs_dict[key] = default  # Store default value
				return default
			else:
				return None

	def setValue(self, category, attr, value):
		key = "%s.%s" % (category, attr)
		self.prefs_dict[key] = value
