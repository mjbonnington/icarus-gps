#!/usr/bin/python

# [Icarus] settings_shot.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Shot settings handler.


import os


class helper():

	def __init__(self, parent, frame):
		""" Setup shot properties panel.
		"""
		self.frame = frame

		# Populate line edit with shot name
		self.frame.shot_lineEdit.setText(parent.self_name)
