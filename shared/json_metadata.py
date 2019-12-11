#!/usr/bin/python

# [Icarus] json_metadata.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Manipulates JSON-based settings metadata for jobs, shots, assets, etc.


# Import custom modules
from . import json_data


class Metadata(json_data.JSONData):
	""" Class for settings metadata.
		Inherits JSONData class.
	"""

	def get_attr(self, category, attr, default=None):
		""" Get a value from prefs dictionary. If the given value cannot be
			retrieved, and a default value is given, return default value.
		"""
		key = "%s.%s" % (category, attr)
		# return self.prefs_dict.get(key, default)  # Works but doesn't store the default in the dict

		try:
			return self.prefs_dict[key]

		except KeyError:
			if default is not None:
				self.prefs_dict[key] = default  # Store default value
				return default
			else:
				return None


	def set_attr(self, category, attr, value):
		""" Set a value and store it in the prefs dictionary.
		"""
		key = "%s.%s" % (category, attr)
		self.prefs_dict[key] = value


	def remove_attr(self, category, attr):
		""" Remove the given attribute from the prefs dictionary.
		"""
		key = "%s.%s" % (category, attr)
		return self.prefs_dict.pop(key, None)


	# def getCategories(self):
	# 	""" Return a list of settings categories.
	# 	"""
	# 	pass


	# def getSettings(self, category):
	# 	""" Return a list of settings for a given category.
	# 	"""
	# 	pass


	# def getApps(self):
	# 	""" Return list of apps that have been specified in the job settings.
	# 	"""
	# 	pass


	def getAppVersion(self, app):
		""" Return version for specified app.
		"""
		key = "apps.%s" % app
		return self.prefs_dict.get(key, None)
