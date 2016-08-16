# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_global_ui.ui'
#
# Created: Tue Aug 16 10:58:39 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
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
        self.elementslib_label = QtGui.QLabel(settings_frame)
        self.elementslib_label.setObjectName("elementslib_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.elementslib_label)
        self.elementslib_lineEdit = QtGui.QLineEdit(settings_frame)
        self.elementslib_lineEdit.setObjectName("elementslib_lineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.elementslib_lineEdit)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.userPrefsServer_radioButton, self.userPrefsHome_radioButton)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefs_label.setText(QtGui.QApplication.translate("settings_frame", "User preferences location:", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsServer_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsServer_radioButton.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "userPrefsRemote", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsHome_radioButton.setText(QtGui.QApplication.translate("settings_frame", "Home folder", None, QtGui.QApplication.UnicodeUTF8))
        self.userPrefsHome_radioButton.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "userPrefsLocal", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_label.setText(QtGui.QApplication.translate("settings_frame", "Global asset library:", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_lineEdit.setText(QtGui.QApplication.translate("settings_frame", "$FILESYSTEMROOT/_Library", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_lineEdit.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "globalAssetLib", None, QtGui.QApplication.UnicodeUTF8))

