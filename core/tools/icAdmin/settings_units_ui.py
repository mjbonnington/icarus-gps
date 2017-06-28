# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_units_ui.ui'
#
# Created: Thu Jun  4 10:43:22 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 145)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.linear_label = QtGui.QLabel(settings_frame)
        self.linear_label.setObjectName("linear_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.linear_label)
        self.linear_comboBox = QtGui.QComboBox(settings_frame)
        self.linear_comboBox.setObjectName("linear_comboBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.linear_comboBox)
        self.angle_label = QtGui.QLabel(settings_frame)
        self.angle_label.setObjectName("angle_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.angle_label)
        self.angle_comboBox = QtGui.QComboBox(settings_frame)
        self.angle_comboBox.setObjectName("angle_comboBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.angle_comboBox)
        self.time_label = QtGui.QLabel(settings_frame)
        self.time_label.setObjectName("time_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.time_label)
        self.time_horizontalLayout = QtGui.QHBoxLayout()
        self.time_horizontalLayout.setObjectName("time_horizontalLayout")
        self.time_comboBox = QtGui.QComboBox(settings_frame)
        self.time_comboBox.setObjectName("time_comboBox")
        self.time_horizontalLayout.addWidget(self.time_comboBox)
        spacerItem = QtGui.QSpacerItem(12, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.time_horizontalLayout.addItem(spacerItem)
        self.fps_label = QtGui.QLabel(settings_frame)
        self.fps_label.setObjectName("fps_label")
        self.time_horizontalLayout.addWidget(self.fps_label)
        self.fps_spinBox = QtGui.QSpinBox(settings_frame)
        self.fps_spinBox.setReadOnly(True)
        self.fps_spinBox.setMinimum(1)
        self.fps_spinBox.setMaximum(6000)
        self.fps_spinBox.setProperty("value", 25)
        self.fps_spinBox.setObjectName("fps_spinBox")
        self.time_horizontalLayout.addWidget(self.fps_spinBox)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.time_horizontalLayout)

        self.retranslateUi(settings_frame)
        self.linear_comboBox.setCurrentIndex(-1)
        self.time_comboBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_label.setText(QtGui.QApplication.translate("settings_frame", "Linear:", None, QtGui.QApplication.UnicodeUTF8))
        self.linear_comboBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "linear", None, QtGui.QApplication.UnicodeUTF8))
        self.angle_label.setText(QtGui.QApplication.translate("settings_frame", "Angle:", None, QtGui.QApplication.UnicodeUTF8))
        self.angle_comboBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "angle", None, QtGui.QApplication.UnicodeUTF8))
        self.time_label.setText(QtGui.QApplication.translate("settings_frame", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_comboBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "time", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_label.setText(QtGui.QApplication.translate("settings_frame", "FPS:", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_label.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "fps", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "fps", None, QtGui.QApplication.UnicodeUTF8))

