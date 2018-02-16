#!/usr/bin/python

# [Icarus] settings_units.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Units settings handler.


# Import custom modules
import units


class helper():

	def __init__(self, parent, frame):
		""" Setup units properties panel.
		"""
		self.frame = frame

		# Populate combo boxes with presets
		for item in units.linear:
			self.frame.linear_comboBox.addItem(item[0])  # Find a way to display nice names but store short names internally

		for item in units.angular:
			self.frame.angle_comboBox.addItem(item[0])  # Find a way to display nice names but store short names internally

		for item in units.time:
			self.frame.time_comboBox.addItem(item[0])  # Find a way to display nice names but store short names internally

		# Set default values - this must happen before values are read from XML data
		self.frame.linear_comboBox.setCurrentIndex(1)  # cm
		self.frame.angle_comboBox.setCurrentIndex(0)  # deg
		self.frame.time_comboBox.setCurrentIndex(1)  # pal

		# Set FPS spin box to correct value based on time combo box selection
		self.setFPS(self.frame.time_comboBox.currentIndex())

		# Connect signals & slots
		self.frame.time_comboBox.currentIndexChanged.connect(lambda current: self.setFPS(current))
		# self.frame.fps_doubleSpinBox.valueChanged.connect(lambda value: self.setTimeUnit(value))


	def setFPS(self, current=None):
		""" Set FPS spin box value based on time unit combo box.
		"""
		self.frame.fps_doubleSpinBox.setValue(units.time[current][2])

