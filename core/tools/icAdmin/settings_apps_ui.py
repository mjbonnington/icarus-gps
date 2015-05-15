# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_apps_ui.ui'
#
# Created: Fri May 15 18:46:27 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 80)
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(Frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.appPaths_pushButton = QtGui.QPushButton(Frame)
        self.appPaths_pushButton.setObjectName("appPaths_pushButton")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.appPaths_pushButton)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.appPaths_pushButton.setText(QtGui.QApplication.translate("Frame", "Edit Versions...", None, QtGui.QApplication.UnicodeUTF8))

