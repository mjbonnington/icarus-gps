#!/usr/bin/python

# [Icarus] settings_resolution.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Camera settings handler.


import os

from Qt import QtWidgets

# Import custom modules
import camPresets


class helper():

	def __init__(self, parent, frame):
		""" Setup camera properties panel.
		"""
		self.frame = frame
		self.cp = camPresets.camPresets()
		cp_load = self.cp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'camPresets.xml'))

		# Populate combo box with presets
		presets = self.cp.getPresets()
		camera_comboBox = self.frame.camera_comboBox

		for item in presets:
			camera_comboBox.addItem(item)

		width = self.frame.filmbackWidth_doubleSpinBox.value()
		height = self.frame.filmbackHeight_doubleSpinBox.value()
		# camera_comboBox.setCurrentIndex(camera_comboBox.findText(self.rp.getPresetFromRes(width, height)))

		# Connect signals & slots
		self.uffp = lambda: self.updateFilmbackFromPreset()
		self.rptc = lambda: self.resetPresetToCustom(camera_comboBox)

		camera_comboBox.currentIndexChanged.connect(self.uffp)
		self.frame.filmbackWidth_doubleSpinBox.valueChanged.connect(self.rptc)
		self.frame.filmbackHeight_doubleSpinBox.valueChanged.connect(self.rptc)


	def updateFilmbackFromPreset(self, index=-1):
		""" Update filmback settings when a preset is chosen.
		"""
		camera = self.frame.camera_comboBox.currentText()
		if camera != 'Custom':
			sensorWidth, sensorHeight = self.cp.getFilmback(camera)

			# Stop the other widgets from emitting signals
			self.frame.filmbackWidth_doubleSpinBox.valueChanged.disconnect(self.rptc)
			self.frame.filmbackHeight_doubleSpinBox.valueChanged.disconnect(self.rptc)

			# Update widgets
			self.frame.filmbackWidth_doubleSpinBox.setValue(sensorWidth)
			self.frame.filmbackHeight_doubleSpinBox.setValue(sensorHeight)

			# Re-enable signals
			self.frame.filmbackWidth_doubleSpinBox.valueChanged.connect(self.rptc)
			self.frame.filmbackHeight_doubleSpinBox.valueChanged.connect(self.rptc)


	def resetPresetToCustom(self, comboBox):
		""" Reset filmback settings preset combo box to 'Custom' when values
			are changed manually.
		"""
		comboBox.setCurrentIndex(comboBox.findText('Custom'))

