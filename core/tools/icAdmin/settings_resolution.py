#!/usr/bin/python

# [Icarus] settings_resolution.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Resolution settings handler.


from fractions import Fraction
import math
import os

# Import custom modules
import resPresets
import verbose


class helper():

	def __init__(self, parent, frame):
		""" Setup resolution properties panel.
		"""
		self.frame = frame
		self.rp = resPresets.resPresets()
		rp_load = self.rp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'resPresets.xml'))

		# Populate combo box with presets
		presets = self.rp.getPresets()
		comboBox = self.frame.resPreset_comboBox

		for item in presets:
			comboBox.addItem(item)

		width = self.frame.fullWidth_spinBox.value()
		height = self.frame.fullHeight_spinBox.value()
		comboBox.setCurrentIndex(comboBox.findText(self.rp.getPresetFromRes(width, height)))

		self.calcAspectRatio()
		self.checkProxyRes()

		# Connect signals & slots
		self.urfp = lambda: self.updateResFromPreset()
		self.car = lambda: self.calcAspectRatio()
		self.urfw = lambda value: self.updateResFullWidth(value)
		self.urfh = lambda value: self.updateResFullHeight(value)
		self.cpr = lambda: self.calcProxyRes()
		self.urpw = lambda value: self.updateResProxyWidth(value)
		self.urph = lambda value: self.updateResProxyHeight(value)

		self.frame.resPreset_comboBox.currentIndexChanged.connect(self.urfp)
		self.frame.preserveAR_checkBox.stateChanged.connect(self.car)
		self.frame.fullWidth_spinBox.valueChanged.connect(self.urfw)
		self.frame.fullHeight_spinBox.valueChanged.connect(self.urfh)
		self.frame.proxyModeScale_radioButton.toggled.connect(self.cpr)
		self.frame.proxyScale_doubleSpinBox.valueChanged.connect(self.cpr)
		self.frame.proxyWidth_spinBox.valueChanged.connect(self.urpw)
		self.frame.proxyHeight_spinBox.valueChanged.connect(self.urph)

		self.frame.proxyScale_doubleSpinBox.valueChanged.connect(lambda value: self.frame.proxyScale_slider.setValue(value*100))
		self.frame.proxyScale_slider.valueChanged.connect(lambda value: self.frame.proxyScale_doubleSpinBox.setValue(value/100))


	def calcAspectRatio(self):
		""" Calculate aspect ratio.
		"""
		fullWidth = self.frame.fullWidth_spinBox.value()
		fullHeight = self.frame.fullHeight_spinBox.value()
		ar = Fraction(fullWidth, fullHeight)
		self.aspectRatio = float(fullWidth) / float(fullHeight)

		# verbose.print_("Aspect ratio: %f" %self.aspectRatio, 4)
		self.frame.preserveAR_checkBox.setText("Lock aspect ratio to %d:%d (%.3f)" %(ar.numerator, ar.denominator, self.aspectRatio))


	def updateResFromPreset(self, index=-1):
		""" Update resolution settings when a preset is chosen.
		"""
		preset = self.frame.resPreset_comboBox.currentText()
		if preset != 'Custom':
			width = int(self.rp.getValue(preset, 'width'))
			height = int(self.rp.getValue(preset, 'height'))

			# Stop the other widgets from emitting signals
			self.frame.fullWidth_spinBox.valueChanged.disconnect(self.urfw)
			self.frame.fullHeight_spinBox.valueChanged.disconnect(self.urfh)
			self.frame.proxyWidth_spinBox.valueChanged.disconnect(self.urpw)
			self.frame.proxyHeight_spinBox.valueChanged.disconnect(self.urph)

			# Update widgets
			self.frame.fullWidth_spinBox.setValue(width)
			self.frame.fullHeight_spinBox.setValue(height)

			self.calcAspectRatio()
			self.calcProxyRes(fullWidth=width, fullHeight=height)

			# Re-enable signals
			self.frame.fullWidth_spinBox.valueChanged.connect(self.urfw)
			self.frame.fullHeight_spinBox.valueChanged.connect(self.urfh)
			self.frame.proxyWidth_spinBox.valueChanged.connect(self.urpw)
			self.frame.proxyHeight_spinBox.valueChanged.connect(self.urph)


	def updateResFullWidth(self, width=-1):
		""" Update resolution when width is changed.
		"""
		# Stop the other widgets from emitting signals
		self.frame.resPreset_comboBox.currentIndexChanged.disconnect(self.urfp)
		self.frame.fullHeight_spinBox.valueChanged.disconnect(self.urfh)
		self.frame.proxyWidth_spinBox.valueChanged.disconnect(self.urpw)
		self.frame.proxyHeight_spinBox.valueChanged.disconnect(self.urph)

		preserveAR = self.frame.preserveAR_checkBox.isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = self.frame.fullHeight_spinBox.value()
			self.calcAspectRatio()

		# print("full res w: [%d]x%d (ar: %f)" %(width, height, self.aspectRatio))

		# Set the preset to 'Custom'
		comboBox = self.frame.resPreset_comboBox
		comboBox.setCurrentIndex(comboBox.findText(self.rp.getPresetFromRes(width, height)))
		#comboBox.setCurrentIndex(comboBox.findText('Custom'))

		# Update height widget
		self.frame.fullHeight_spinBox.setValue(height)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		self.frame.resPreset_comboBox.currentIndexChanged.connect(self.urfp)
		self.frame.fullHeight_spinBox.valueChanged.connect(self.urfh)
		self.frame.proxyWidth_spinBox.valueChanged.connect(self.urpw)
		self.frame.proxyHeight_spinBox.valueChanged.connect(self.urph)


	def updateResFullHeight(self, height=-1):
		""" Update resolution when height is changed.
		"""
		# Stop the other widgets from emitting signals
		self.frame.resPreset_comboBox.currentIndexChanged.disconnect(self.urfp)
		self.frame.fullWidth_spinBox.valueChanged.disconnect(self.urfw)
		self.frame.proxyWidth_spinBox.valueChanged.disconnect(self.urpw)
		self.frame.proxyHeight_spinBox.valueChanged.disconnect(self.urph)

		preserveAR = self.frame.preserveAR_checkBox.isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = self.frame.fullWidth_spinBox.value()
			self.calcAspectRatio()

		# print("full res h: %dx[%d] (ar: %f)" %(width, height, self.aspectRatio))

		# Set the preset to 'Custom'
		comboBox = self.frame.resPreset_comboBox
		comboBox.setCurrentIndex(comboBox.findText(self.rp.getPresetFromRes(width, height)))
		#comboBox.setCurrentIndex(comboBox.findText('Custom'))

		# Update width widget
		self.frame.fullWidth_spinBox.setValue(width)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		self.frame.resPreset_comboBox.currentIndexChanged.connect(self.urfp)
		self.frame.fullWidth_spinBox.valueChanged.connect(self.urfw)
		self.frame.proxyWidth_spinBox.valueChanged.connect(self.urpw)
		self.frame.proxyHeight_spinBox.valueChanged.connect(self.urph)


	def updateResProxyWidth(self, width=-1):
		""" Update proxy resolution when width is changed.
		"""
		# Stop the other widgets from emitting signals
		self.frame.proxyHeight_spinBox.valueChanged.disconnect(self.urph)

		preserveAR = self.frame.preserveAR_checkBox.isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = self.frame.proxyHeight_spinBox.value()

		# print("proxy res w: [%d]x%d (ar: %f)" %(width, height, self.aspectRatio))

		# Update height widget
		self.frame.proxyHeight_spinBox.setValue(height)

		# Re-enable signals
		self.frame.proxyHeight_spinBox.valueChanged.connect(self.urph)


	def updateResProxyHeight(self, height=-1):
		""" Update proxy resolution when height is changed.
		"""
		# Stop the other widgets from emitting signals
		self.frame.proxyWidth_spinBox.valueChanged.disconnect(self.urpw)

		preserveAR = self.frame.preserveAR_checkBox.isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = self.frame.proxyWidth_spinBox.value()

		# print("proxy res h: %dx[%d] (ar: %f)" %(width, height, self.aspectRatio))

		# Update width widget
		self.frame.proxyWidth_spinBox.setValue(width)

		# Re-enable signals
		self.frame.proxyWidth_spinBox.valueChanged.connect(self.urpw)


	def calcProxyRes(self, proxyScale=-1, fullWidth=-1, fullHeight=-1):
		""" Calculate proxy resolution.
		"""
		# If fullWidth or fullHeight not specified, get values from widgets
		if fullWidth < 0:
			fullWidth = self.frame.fullWidth_spinBox.value()
		if fullHeight < 0:
			fullHeight = self.frame.fullHeight_spinBox.value()

		if self.frame.proxyModeScale_radioButton.isChecked():
			proxyMode = 'scale'
			proxyScale = self.frame.proxyScale_doubleSpinBox.value()
			proxyRes = int(fullWidth * proxyScale), int(fullHeight * proxyScale)
		else:
			proxyMode = 'res'
			proxyScale = -1
			proxyRes = self.frame.proxyWidth_spinBox.value(), self.frame.proxyHeight_spinBox.value()

		#print("proxy res: %dx%d (%s: %f)" %(proxyRes[0], proxyRes[1], proxyMode, proxyScale))

		# Update widgets
		self.frame.proxyWidth_spinBox.setValue(proxyRes[0])
		self.frame.proxyHeight_spinBox.setValue(proxyRes[1])


	def checkProxyRes(self):
		""" Check proxy resolution matches full resolution x scale and set
			appropriate proxy mode.
		"""
		fullWidth = self.frame.fullWidth_spinBox.value()
		fullHeight = self.frame.fullHeight_spinBox.value()
		proxyWidth = self.frame.proxyWidth_spinBox.value()
		proxyHeight = self.frame.proxyHeight_spinBox.value()
		proxyScale = self.frame.proxyScale_doubleSpinBox.value()

		if (proxyWidth == fullWidth*proxyScale) and (proxyHeight == fullHeight*proxyScale):
			self.frame.proxyModeScale_radioButton.setChecked(True)
			self.frame.proxyModeRes_radioButton.setChecked(False)
		else:
			self.frame.proxyModeScale_radioButton.setChecked(False)
			self.frame.proxyModeRes_radioButton.setChecked(True)

