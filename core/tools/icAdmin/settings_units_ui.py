# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_units_ui.ui'
#
# Created: Tue May 19 18:10:08 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
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
        self.time_label = QtGui.QLabel(settings_frame)
        self.time_label.setObjectName("time_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.time_label)
        self.linear_label = QtGui.QLabel(settings_frame)
        self.linear_label.setObjectName("linear_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.linear_label)
        self.angle_label = QtGui.QLabel(settings_frame)
        self.angle_label.setObjectName("angle_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.angle_label)
        self.time_comboBox = QtGui.QComboBox(settings_frame)
        self.time_comboBox.setObjectName("time_comboBox")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.time_comboBox.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.time_comboBox)
        self.linear_comboBox = QtGui.QComboBox(settings_frame)
        self.linear_comboBox.setObjectName("linear_comboBox")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.linear_comboBox.addItem("")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.linear_comboBox)
        self.angle_comboBox = QtGui.QComboBox(settings_frame)
        self.angle_comboBox.setObjectName("angle_comboBox")
        self.angle_comboBox.addItem("")
        self.angle_comboBox.addItem("")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.angle_comboBox)

        self.retranslateUi(settings_frame)
        self.time_comboBox.setCurrentIndex(1)
        self.linear_comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.time_label.setText(QtGui.QApplication.translate("settings_frame", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_label.setText(QtGui.QApplication.translate("settings_frame", "Linear:", None, QtGui.QApplication.UnicodeUTF8))
        self.angle_label.setText(QtGui.QApplication.translate("settings_frame", "Angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(0, QtGui.QApplication.translate("settings_frame", "film", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(1, QtGui.QApplication.translate("settings_frame", "pal", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(2, QtGui.QApplication.translate("settings_frame", "ntsc", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(3, QtGui.QApplication.translate("settings_frame", "millisec", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(4, QtGui.QApplication.translate("settings_frame", "sec", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(5, QtGui.QApplication.translate("settings_frame", "min", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setItemText(6, QtGui.QApplication.translate("settings_frame", "hour", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(0, QtGui.QApplication.translate("settings_frame", "millimeter", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(1, QtGui.QApplication.translate("settings_frame", "centimeter", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(2, QtGui.QApplication.translate("settings_frame", "meter", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(3, QtGui.QApplication.translate("settings_frame", "kilometer", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(4, QtGui.QApplication.translate("settings_frame", "inch", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(5, QtGui.QApplication.translate("settings_frame", "foot", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(6, QtGui.QApplication.translate("settings_frame", "yard", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setItemText(7, QtGui.QApplication.translate("settings_frame", "mile", None, QtGui.QApplication.UnicodeUTF8))
        self.angle_comboBox.setItemText(0, QtGui.QApplication.translate("settings_frame", "degree", None, QtGui.QApplication.UnicodeUTF8))
        self.angle_comboBox.setItemText(1, QtGui.QApplication.translate("settings_frame", "radian", None, QtGui.QApplication.UnicodeUTF8))

