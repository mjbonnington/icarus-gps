# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_user_ui.ui'
#
# Created: Sun Nov 01 19:06:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 160)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.userPrefs_label = QtGui.QLabel(settings_frame)
        self.userPrefs_label.setObjectName("userPrefs_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.userPrefs_label)
        self.userPrefs_horizontalLayout = QtGui.QHBoxLayout()
        self.userPrefs_horizontalLayout.setObjectName("userPrefs_horizontalLayout")
        self.userPrefsServer_radioButton = QtGui.QRadioButton(settings_frame)
        self.userPrefsServer_radioButton.setChecked(True)
        self.userPrefsServer_radioButton.setObjectName("userPrefsServer_radioButton")
        self.userPrefs_horizontalLayout.addWidget(self.userPrefsServer_radioButton)
        self.userPrefsHome_radioButton = QtGui.QRadioButton(settings_frame)
        self.userPrefsHome_radioButton.setObjectName("userPrefsHome_radioButton")
        self.userPrefs_horizontalLayout.addWidget(self.userPrefsHome_radioButton)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.userPrefs_horizontalLayout)
        self.minimiseOnLaunch_checkBox = QtGui.QCheckBox(settings_frame)
        self.minimiseOnLaunch_checkBox.setChecked(True)
        self.minimiseOnLaunch_checkBox.setObjectName("minimiseOnLaunch_checkBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.minimiseOnLaunch_checkBox)
        self.numRecentFiles_label = QtGui.QLabel(settings_frame)
        self.numRecentFiles_label.setObjectName("numRecentFiles_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.numRecentFiles_label)
        self.verbosity_label = QtGui.QLabel(settings_frame)
        self.verbosity_label.setObjectName("verbosity_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.verbosity_label)
        self.numRecentFiles_horizontalLayout = QtGui.QHBoxLayout()
        self.numRecentFiles_horizontalLayout.setObjectName("numRecentFiles_horizontalLayout")
        self.numRecentFiles_spinBox = QtGui.QSpinBox(settings_frame)
        self.numRecentFiles_spinBox.setMinimum(1)
        self.numRecentFiles_spinBox.setMaximum(20)
        self.numRecentFiles_spinBox.setProperty("value", 10)
        self.numRecentFiles_spinBox.setObjectName("numRecentFiles_spinBox")
        self.numRecentFiles_horizontalLayout.addWidget(self.numRecentFiles_spinBox)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.numRecentFiles_horizontalLayout)
        self.verbosity_horizontalLayout = QtGui.QHBoxLayout()
        self.verbosity_horizontalLayout.setObjectName("verbosity_horizontalLayout")
        self.verbosity_spinBox = QtGui.QSpinBox(settings_frame)
        self.verbosity_spinBox.setEnabled(True)
        self.verbosity_spinBox.setMaximum(4)
        self.verbosity_spinBox.setProperty("value", 3)
        self.verbosity_spinBox.setObjectName("verbosity_spinBox")
        self.verbosity_horizontalLayout.addWidget(self.verbosity_spinBox)
        self.vebosityInfo_label = QtGui.QLabel(settings_frame)
        self.vebosityInfo_label.setObjectName("vebosityInfo_label")
        self.verbosity_horizontalLayout.addWidget(self.vebosityInfo_label)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.verbosity_horizontalLayout)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.numRecentFiles_spinBox, self.userPrefsServer_radioButton)
        settings_frame.setTabOrder(self.userPrefsServer_radioButton, self.userPrefsHome_radioButton)
        settings_frame.setTabOrder(self.userPrefsHome_radioButton, self.verbosity_spinBox)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefs_label.setText(QtGui.QApplication.translate("settings_frame", "User preferences location:", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsServer_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsHome_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Home folder", None, QtGui.QApplication.UnicodeUTF8))
        self.minimiseOnLaunch_checkBox.setText(QtGui.QApplication.translate("settings_frame", "Minimise Icarus UI on application launch", None, QtGui.QApplication.UnicodeUTF8))
        self.minimiseOnLaunch_checkBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "minimiseOnLaunch", None, QtGui.QApplication.UnicodeUTF8))
        self.numRecentFiles_label.setText(QtGui.QApplication.translate("settings_frame", "Number of recent files:", None, QtGui.QApplication.UnicodeUTF8))
        self.verbosity_label.setText(QtGui.QApplication.translate("settings_frame", "Output message verbosity:", None, QtGui.QApplication.UnicodeUTF8))
        self.numRecentFiles_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "numRecentFiles", None, QtGui.QApplication.UnicodeUTF8))
        self.verbosity_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "verbosity", None, QtGui.QApplication.UnicodeUTF8))
        self.vebosityInfo_label.setText(QtGui.QApplication.translate("settings_frame", "Errors and warnings", None, QtGui.QApplication.UnicodeUTF8))
