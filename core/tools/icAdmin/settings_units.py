#!/usr/bin/python

# [Icarus] settings_units.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Units settings handler.


# Import custom modules
import units
import verbose


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
			self.frame.timePreset_comboBox.addItem(self.getNiceName(item))
			self.frame.time_comboBox.addItem(item[0])

		self.frame.timePreset_comboBox.addItem("Custom")
		self.frame.time_comboBox.addItem("custom")

		# Set default values - this must happen before values are read from XML data
		self.frame.linear_comboBox.setCurrentIndex(1)  # cm
		self.frame.angle_comboBox.setCurrentIndex(0)  # deg
		self.frame.timePreset_comboBox.setCurrentIndex(1)  # pal

		# Connect signals & slots
		self.sfps = lambda current: self.setFPS(current)
		self.stp = lambda value: self.setTimePreset(value)
		self.cfrc = lambda current: self.checkFrameRateCompatibility(current)

		self.frame.timePreset_comboBox.currentIndexChanged.connect(self.sfps)
		self.frame.fps_doubleSpinBox.valueChanged.connect(self.stp)
		self.frame.time_comboBox.currentIndexChanged.connect(self.cfrc)

		# Set FPS spin box to correct value based on time combo box selection
		self.setFPS(self.frame.timePreset_comboBox.currentIndex())
		self.frame.time_comboBox.hide()
		self.setInfoMessage()


	# @QtCore.Slot(int)
	def setFPS(self, current):
		""" Set FPS spin box value based on time unit combo box.
		"""
		timePreset = self.frame.timePreset_comboBox.currentText()
		if timePreset != "Custom":
			# Stop the other widgets from emitting signals
			self.frame.fps_doubleSpinBox.valueChanged.disconnect(self.stp)

			# Update widgets
			self.frame.fps_doubleSpinBox.setValue(units.time[current][2])

			# Re-enable signals
			self.frame.fps_doubleSpinBox.valueChanged.connect(self.stp)


	# @QtCore.Slot(float)
	def setTimePreset(self, value):
		""" Set time preset based on FPS setting.
		"""
		# Stop the other widgets from emitting signals
		self.frame.timePreset_comboBox.currentIndexChanged.disconnect(self.sfps)

		# Update widgets
		comboBox = self.frame.timePreset_comboBox
		comboBox.setCurrentIndex(comboBox.findText(self.getPresetFromFPS(value)))

		# Re-enable signals
		self.frame.timePreset_comboBox.currentIndexChanged.connect(self.sfps)


	# @QtCore.Slot(int)
	def checkFrameRateCompatibility(self, current):
		""" Check compatibility of frame rate setting.
			TODO: Update to reflect compatibility with apps other than Maya.
		"""
		message = ""

		try:
			fps = units.time[current][2]
			if (type(fps) == float) or (fps > 6000):
				message = "The time units setting (%s) is incompatible with Maya 2016 or earlier." %units.time[current][0]
		except IndexError:
			message = "The frame rate setting is incompatible with Maya."

		self.setInfoMessage(message)


	def setInfoMessage(self, message=""):
		""" Set the information message.
		"""
		if message:
			verbose.warning(message)
		self.frame.timeInfo_label.setText(message)


	def getNiceName(self, item):
		""" Generate a nice name for a time preset.
		"""
		if item[1] is "":
			nice_name = "%s fps" %item[2]
		else:
			nice_name = "%s (%s fps)" %(item[1], item[2])

		return nice_name


	def getPresetFromFPS(self, fps):
		""" Return a time preset given the FPS value.
		"""
		#print(type(fps), fps)
		for item in units.time:
			if item[2]==fps:
				return self.getNiceName(item)

		return "Custom"

