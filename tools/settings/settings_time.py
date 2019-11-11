#!/usr/bin/python

# [Icarus] settings_time.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Time settings handler.


from __future__ import division  # Enables true division for Python2
import time

# Import custom modules
from shared import verbose


class helper():

	def __init__(self, parent, frame):
		""" Setup time properties panel.
		"""
		self.frame = frame
		self.parent = parent

		# Connect signals & slots
		self.ctv = lambda: self.calcTimeValues()

		self.frame.rangeStart_spinBox.valueChanged.connect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.connect(self.ctv)
		# self.frame.duration_spinBox.valueChanged.connect(self.ctv)

		self.calcTimeValues()


	def calcTimeValues(self):
		""" Calculate time values (frame range, duration, in/out, etc.)
		"""
		rangeStart = self.frame.rangeStart_spinBox.value()
		rangeEnd = self.frame.rangeEnd_spinBox.value()

		# Stop the other widgets from emitting signals
		self.frame.rangeStart_spinBox.valueChanged.disconnect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.disconnect(self.ctv)
		# self.frame.duration_spinBox.valueChanged.disconnect(self.ctv)

		# Update widgets
		self.frame.rangeEnd_spinBox.setMinimum(rangeStart)
		if rangeStart >= rangeEnd:
			rangeEnd = rangeStart
			self.frame.rangeEnd_spinBox.setValue(rangeEnd)

		durationFrames, formattedStr = self.calcDuration(rangeStart, rangeEnd)
		self.frame.duration_spinBox.setValue(durationFrames)
		self.frame.durationInfo_label.setText(formattedStr)

		self.frame.posterFrame_spinBox.setMinimum(rangeStart)
		self.frame.posterFrame_spinBox.setMaximum(rangeEnd)
		self.frame.posterFrame_slider.setMinimum(rangeStart)
		self.frame.posterFrame_slider.setMaximum(rangeEnd)

		# Re-enable signals
		self.frame.rangeStart_spinBox.valueChanged.connect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.connect(self.ctv)
		# self.frame.duration_spinBox.valueChanged.connect(self.ctv)


	def calcDuration(self, rangeStart, rangeEnd):
		""" Calculate the duration.
		"""
		durationFrames = rangeEnd - rangeStart + 1

		fps = self.parent.xd.getValue('units', 'fps', type='float')
		if fps == "":
			if self.parent.inherit:
				fps = self.parent.id.getValue('units', 'fps', type='float')
		if fps == "":
			verbose.warning("Undefined FPS.")
			return durationFrames, ""

		durationSecs = float(durationFrames) / float(fps)
		durationStr = ""
		if durationSecs < 60:
			durationStr = "%s seconds" %round(durationSecs, 6)
		elif durationSecs < 3600:
			mins = durationSecs/60
			secs = durationSecs%60
			durationStr = "%dm %ds" %(mins, secs)
		else:
			durationStr = time.strftime("%H:%M:%S", time.gmtime(durationSecs))
		formattedStr = "%s @ %s fps" %(durationStr, round(fps, 3))

		return durationFrames, formattedStr

