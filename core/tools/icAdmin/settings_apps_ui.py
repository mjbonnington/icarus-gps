# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_apps_ui.ui'
#
# Created: Tue May 19 18:03:16 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 80)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.appPaths_pushButton = QtGui.QPushButton(settings_frame)
        self.appPaths_pushButton.setObjectName("appPaths_pushButton")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.appPaths_pushButton)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.appPaths_pushButton.setText(QtGui.QApplication.translate("settings_frame", "Edit Versions...", None, QtGui.QApplication.UnicodeUTF8))

