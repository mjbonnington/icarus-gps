# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_resolution_ui.ui'
#
# Created: Fri May 29 16:21:22 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 320)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.resPreset_label = QtGui.QLabel(settings_frame)
        self.resPreset_label.setObjectName("resPreset_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.resPreset_label)
        self.resPreset_comboBox = QtGui.QComboBox(settings_frame)
        self.resPreset_comboBox.setObjectName("resPreset_comboBox")
        self.resPreset_comboBox.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.resPreset_comboBox)
        self.preserveAR_checkBox = QtGui.QCheckBox(settings_frame)
        self.preserveAR_checkBox.setChecked(True)
        self.preserveAR_checkBox.setObjectName("preserveAR_checkBox")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.preserveAR_checkBox)
        self.full_label = QtGui.QLabel(settings_frame)
        self.full_label.setObjectName("full_label")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.full_label)
        self.full_horizontalLayout = QtGui.QHBoxLayout()
        self.full_horizontalLayout.setObjectName("full_horizontalLayout")
        self.fullWidth_spinBox = QtGui.QSpinBox(settings_frame)
        self.fullWidth_spinBox.setMinimum(1)
        self.fullWidth_spinBox.setMaximum(99999)
        self.fullWidth_spinBox.setProperty("value", 1920)
        self.fullWidth_spinBox.setObjectName("fullWidth_spinBox")
        self.full_horizontalLayout.addWidget(self.fullWidth_spinBox)
        self.fullSep_label = QtGui.QLabel(settings_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fullSep_label.sizePolicy().hasHeightForWidth())
        self.fullSep_label.setSizePolicy(sizePolicy)
        self.fullSep_label.setObjectName("fullSep_label")
        self.full_horizontalLayout.addWidget(self.fullSep_label)
        self.fullHeight_spinBox = QtGui.QSpinBox(settings_frame)
        self.fullHeight_spinBox.setMinimum(1)
        self.fullHeight_spinBox.setMaximum(99999)
        self.fullHeight_spinBox.setProperty("value", 1080)
        self.fullHeight_spinBox.setObjectName("fullHeight_spinBox")
        self.full_horizontalLayout.addWidget(self.fullHeight_spinBox)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.full_horizontalLayout)
        self.proxyMode_label = QtGui.QLabel(settings_frame)
        self.proxyMode_label.setObjectName("proxyMode_label")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.proxyMode_label)
        self.proxyMode_horizontalLayout = QtGui.QHBoxLayout()
        self.proxyMode_horizontalLayout.setObjectName("proxyMode_horizontalLayout")
        self.proxyModeScale_radioButton = QtGui.QRadioButton(settings_frame)
        self.proxyModeScale_radioButton.setChecked(True)
        self.proxyModeScale_radioButton.setObjectName("proxyModeScale_radioButton")
        self.proxyMode_horizontalLayout.addWidget(self.proxyModeScale_radioButton)
        self.proxyModeRes_radioButton = QtGui.QRadioButton(settings_frame)
        self.proxyModeRes_radioButton.setObjectName("proxyModeRes_radioButton")
        self.proxyMode_horizontalLayout.addWidget(self.proxyModeRes_radioButton)
        self.formLayout.setLayout(7, QtGui.QFormLayout.FieldRole, self.proxyMode_horizontalLayout)
        self.proxyScale_label = QtGui.QLabel(settings_frame)
        self.proxyScale_label.setObjectName("proxyScale_label")
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.proxyScale_label)
        self.proxyScale_horizontalLayout = QtGui.QHBoxLayout()
        self.proxyScale_horizontalLayout.setObjectName("proxyScale_horizontalLayout")
        self.proxyScale_doubleSpinBox = QtGui.QDoubleSpinBox(settings_frame)
        self.proxyScale_doubleSpinBox.setEnabled(True)
        self.proxyScale_doubleSpinBox.setMaximum(1.0)
        self.proxyScale_doubleSpinBox.setSingleStep(0.01)
        self.proxyScale_doubleSpinBox.setProperty("value", 0.5)
        self.proxyScale_doubleSpinBox.setObjectName("proxyScale_doubleSpinBox")
        self.proxyScale_horizontalLayout.addWidget(self.proxyScale_doubleSpinBox)
        self.formLayout.setLayout(8, QtGui.QFormLayout.FieldRole, self.proxyScale_horizontalLayout)
        self.proxy_label = QtGui.QLabel(settings_frame)
        self.proxy_label.setObjectName("proxy_label")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.proxy_label)
        self.proxy_horizontalLayout = QtGui.QHBoxLayout()
        self.proxy_horizontalLayout.setObjectName("proxy_horizontalLayout")
        self.proxyWidth_spinBox = QtGui.QSpinBox(settings_frame)
        self.proxyWidth_spinBox.setEnabled(False)
        self.proxyWidth_spinBox.setMinimum(1)
        self.proxyWidth_spinBox.setMaximum(99999)
        self.proxyWidth_spinBox.setProperty("value", 960)
        self.proxyWidth_spinBox.setObjectName("proxyWidth_spinBox")
        self.proxy_horizontalLayout.addWidget(self.proxyWidth_spinBox)
        self.proxySep_label = QtGui.QLabel(settings_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxySep_label.sizePolicy().hasHeightForWidth())
        self.proxySep_label.setSizePolicy(sizePolicy)
        self.proxySep_label.setObjectName("proxySep_label")
        self.proxy_horizontalLayout.addWidget(self.proxySep_label)
        self.proxyHeight_spinBox = QtGui.QSpinBox(settings_frame)
        self.proxyHeight_spinBox.setEnabled(False)
        self.proxyHeight_spinBox.setMinimum(1)
        self.proxyHeight_spinBox.setMaximum(99999)
        self.proxyHeight_spinBox.setProperty("value", 540)
        self.proxyHeight_spinBox.setObjectName("proxyHeight_spinBox")
        self.proxy_horizontalLayout.addWidget(self.proxyHeight_spinBox)
        self.formLayout.setLayout(9, QtGui.QFormLayout.FieldRole, self.proxy_horizontalLayout)
        self.resPrest_pushButton = QtGui.QPushButton(settings_frame)
        self.resPrest_pushButton.setEnabled(False)
        self.resPrest_pushButton.setObjectName("resPrest_pushButton")
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.resPrest_pushButton)

        self.retranslateUi(settings_frame)
        QtCore.QObject.connect(self.proxyModeScale_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyScale_doubleSpinBox.setEnabled)
        QtCore.QObject.connect(self.proxyModeScale_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyWidth_spinBox.setDisabled)
        QtCore.QObject.connect(self.proxyModeScale_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyHeight_spinBox.setDisabled)
        QtCore.QObject.connect(self.proxyModeRes_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyScale_doubleSpinBox.setDisabled)
        QtCore.QObject.connect(self.proxyModeRes_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyWidth_spinBox.setEnabled)
        QtCore.QObject.connect(self.proxyModeRes_radioButton, QtCore.SIGNAL("toggled(bool)"), self.proxyHeight_spinBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.preserveAR_checkBox, self.fullWidth_spinBox)
        settings_frame.setTabOrder(self.fullWidth_spinBox, self.fullHeight_spinBox)
        settings_frame.setTabOrder(self.fullHeight_spinBox, self.proxyModeScale_radioButton)
        settings_frame.setTabOrder(self.proxyModeScale_radioButton, self.proxyModeRes_radioButton)
        settings_frame.setTabOrder(self.proxyModeRes_radioButton, self.proxyScale_doubleSpinBox)
        settings_frame.setTabOrder(self.proxyScale_doubleSpinBox, self.proxyWidth_spinBox)
        settings_frame.setTabOrder(self.proxyWidth_spinBox, self.proxyHeight_spinBox)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_label.setText(QtGui.QApplication.translate("settings_frame", "Preset:", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_comboBox.setItemText(0, QtGui.QApplication.translate("settings_frame", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.preserveAR_checkBox.setText(QtGui.QApplication.translate("settings_frame", "Preserve aspect ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.full_label.setText(QtGui.QApplication.translate("settings_frame", "Full size resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.fullWidth_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "fullWidth", None, QtGui.QApplication.UnicodeUTF8))
        self.fullSep_label.setText(QtGui.QApplication.translate("settings_frame", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.fullHeight_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "fullHeight", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyMode_label.setText(QtGui.QApplication.translate("settings_frame", "Proxy mode:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyModeScale_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyModeRes_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyScale_label.setText(QtGui.QApplication.translate("settings_frame", "Proxy scale:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_label.setText(QtGui.QApplication.translate("settings_frame", "Proxy resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyWidth_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "proxyWidth", None, QtGui.QApplication.UnicodeUTF8))
        self.proxySep_label.setText(QtGui.QApplication.translate("settings_frame", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyHeight_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "proxyHeight", None, QtGui.QApplication.UnicodeUTF8))
        self.resPrest_pushButton.setText(QtGui.QApplication.translate("settings_frame", "Edit Presets...", None, QtGui.QApplication.UnicodeUTF8))
