#!/usr/bin/python

# [Icarus] settings_resolution.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Time settings handler.


from Qt import QtWidgets


class helper():

	def __init__(self, parent, frame):
		""" Setup time properties panel.
		"""
		self.frame = frame

		# Connect signals & slots
		self.ctv = lambda: self.calcTimeValues()

		self.frame.rangeStart_spinBox.valueChanged.connect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.connect(self.ctv)

		self.calcTimeValues()


	def calcTimeValues(self):
		""" Calculate time values (frame range, duration, in/out, etc.)
		"""
		rangeStart = self.frame.rangeStart_spinBox.value()
		rangeEnd = self.frame.rangeEnd_spinBox.value()

		durationFull = rangeEnd - rangeStart + 1

		# Stop the other widgets from emitting signals
		self.frame.rangeStart_spinBox.valueChanged.disconnect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.disconnect(self.ctv)

		# Update widgets
		self.frame.rangeInfo_label.setText("(duration: %d frames)" %durationFull)

		self.frame.rangeStart_spinBox.setMaximum(rangeEnd)
		self.frame.rangeEnd_spinBox.setMinimum(rangeStart)
		self.frame.posterFrame_spinBox.setMinimum(rangeStart)
		self.frame.posterFrame_spinBox.setMaximum(rangeEnd)

		# Re-enable signals
		self.frame.rangeStart_spinBox.valueChanged.connect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.connect(self.ctv)

