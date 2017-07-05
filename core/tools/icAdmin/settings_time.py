#!/usr/bin/python

# [Icarus] settings_time.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Time settings handler.


import time


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

		fps = int(self.parent.xd.getValue('units', 'fps'))
		durationFrames = rangeEnd - rangeStart + 1
		durationSecs = durationFrames / fps
		durationStr = ""
		if durationSecs < 60:
			durationStr = "%s seconds" %round(durationSecs, 6)
		elif durationSecs < 3600:
			mins = durationSecs/60
			secs = durationSecs%60
			durationStr = "%dm %ds" %(mins, secs)
		else:
			durationStr = time.strftime("%H:%M:%S", time.gmtime(durationSecs))

		# Stop the other widgets from emitting signals
		self.frame.rangeStart_spinBox.valueChanged.disconnect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.disconnect(self.ctv)
		# self.frame.duration_spinBox.valueChanged.disconnect(self.ctv)

		# Update widgets
		self.frame.rangeEnd_spinBox.setMinimum(rangeStart)
		if rangeStart >= rangeEnd:
			self.frame.rangeEnd_spinBox.setValue(rangeStart)

		# self.frame.rangeStart_spinBox.setMaximum(rangeEnd)
		# self.frame.rangeEnd_spinBox.setMinimum(rangeStart)

		self.frame.posterFrame_spinBox.setMinimum(rangeStart)
		self.frame.posterFrame_spinBox.setMaximum(rangeEnd)
		self.frame.posterFrame_slider.setMinimum(rangeStart)
		self.frame.posterFrame_slider.setMaximum(rangeEnd)

		self.frame.duration_spinBox.setValue(durationFrames)
		self.frame.durationInfo_label.setText("%s @ %d fps" %(durationStr, fps))

		# Re-enable signals
		self.frame.rangeStart_spinBox.valueChanged.connect(self.ctv)
		self.frame.rangeEnd_spinBox.valueChanged.connect(self.ctv)
		# self.frame.duration_spinBox.valueChanged.connect(self.ctv)

