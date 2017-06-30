# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_other_ui.ui'
#
# Created: Thu Jul 14 15:57:06 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 128)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.prodboard_label = QtGui.QLabel(settings_frame)
        self.prodboard_label.setObjectName("prodboard_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.prodboard_label)
        self.prodboard_lineEdit = QtGui.QLineEdit(settings_frame)
        self.prodboard_lineEdit.setObjectName("prodboard_lineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.prodboard_lineEdit)
        self.projtools_label = QtGui.QLabel(settings_frame)
        self.projtools_label.setObjectName("projtools_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.projtools_label)
        self.projtools_lineEdit = QtGui.QLineEdit(settings_frame)
        self.projtools_lineEdit.setObjectName("projtools_lineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.projtools_lineEdit)
        self.elementslib_label = QtGui.QLabel(settings_frame)
        self.elementslib_label.setObjectName("elementslib_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.elementslib_label)
        self.elementslib_lineEdit = QtGui.QLineEdit(settings_frame)
        self.elementslib_lineEdit.setObjectName("elementslib_lineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.elementslib_lineEdit)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.prodboard_lineEdit, self.projtools_lineEdit)
        settings_frame.setTabOrder(self.projtools_lineEdit, self.elementslib_lineEdit)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.prodboard_label.setText(QtGui.QApplication.translate("settings_frame", "Production board:", None, QtGui.QApplication.UnicodeUTF8))
        self.prodboard_lineEdit.setText(QtGui.QApplication.translate("settings_frame", "https://gramercypark.tpondemand.com", None, QtGui.QApplication.UnicodeUTF8))
        self.prodboard_lineEdit.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "prodboard", None, QtGui.QApplication.UnicodeUTF8))
        self.projtools_label.setText(QtGui.QApplication.translate("settings_frame", "Project tools:", None, QtGui.QApplication.UnicodeUTF8))
        self.projtools_lineEdit.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "projtools", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_label.setText(QtGui.QApplication.translate("settings_frame", "Elements library:", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_lineEdit.setText(QtGui.QApplication.translate("settings_frame", "$FILESYSTEMROOT/_Library/Asset_Library", None, QtGui.QApplication.UnicodeUTF8))
        self.elementslib_lineEdit.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "elementslib", None, QtGui.QApplication.UnicodeUTF8))

