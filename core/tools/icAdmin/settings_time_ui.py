# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_time_ui.ui'
#
# Created: Wed Mar 16 09:53:07 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_settings_frame(object):
    def setupUi(self, settings_frame):
        settings_frame.setObjectName("settings_frame")
        settings_frame.resize(400, 144)
        settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.range_label = QtGui.QLabel(settings_frame)
        self.range_label.setObjectName("range_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.range_label)
        self.range_horizontalLayout = QtGui.QHBoxLayout()
        self.range_horizontalLayout.setObjectName("range_horizontalLayout")
        self.rangeStart_spinBox = QtGui.QSpinBox(settings_frame)
        self.rangeStart_spinBox.setMinimum(0)
        self.rangeStart_spinBox.setMaximum(9999)
        self.rangeStart_spinBox.setProperty("value", 1001)
        self.rangeStart_spinBox.setObjectName("rangeStart_spinBox")
        self.range_horizontalLayout.addWidget(self.rangeStart_spinBox)
        self.rangeSep_label = QtGui.QLabel(settings_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeSep_label.sizePolicy().hasHeightForWidth())
        self.rangeSep_label.setSizePolicy(sizePolicy)
        self.rangeSep_label.setObjectName("rangeSep_label")
        self.range_horizontalLayout.addWidget(self.rangeSep_label)
        self.rangeEnd_spinBox = QtGui.QSpinBox(settings_frame)
        self.rangeEnd_spinBox.setMinimum(0)
        self.rangeEnd_spinBox.setMaximum(9999)
        self.rangeEnd_spinBox.setProperty("value", 1100)
        self.rangeEnd_spinBox.setObjectName("rangeEnd_spinBox")
        self.range_horizontalLayout.addWidget(self.rangeEnd_spinBox)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.range_horizontalLayout)
        self.handles_label = QtGui.QLabel(settings_frame)
        self.handles_label.setObjectName("handles_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.handles_label)
        self.handles_spinBox = QtGui.QSpinBox(settings_frame)
        self.handles_spinBox.setMaximum(9999)
        self.handles_spinBox.setProperty("value", 10)
        self.handles_spinBox.setObjectName("handles_spinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.handles_spinBox)
        self.posterFrame_label = QtGui.QLabel(settings_frame)
        self.posterFrame_label.setObjectName("posterFrame_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.posterFrame_label)
        self.posterFrame_spinBox = QtGui.QSpinBox(settings_frame)
        self.posterFrame_spinBox.setMaximum(9999)
        self.posterFrame_spinBox.setProperty("value", 1001)
        self.posterFrame_spinBox.setObjectName("posterFrame_spinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.posterFrame_spinBox)

        self.retranslateUi(settings_frame)
        QtCore.QMetaObject.connectSlotsByName(settings_frame)
        settings_frame.setTabOrder(self.rangeStart_spinBox, self.rangeEnd_spinBox)
        settings_frame.setTabOrder(self.rangeEnd_spinBox, self.handles_spinBox)

    def retranslateUi(self, settings_frame):
        settings_frame.setWindowTitle(QtGui.QApplication.translate("settings_frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.range_label.setText(QtGui.QApplication.translate("settings_frame", "Frame range:", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeStart_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "rangeStart", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeSep_label.setText(QtGui.QApplication.translate("settings_frame", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeEnd_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "rangeEnd", None, QtGui.QApplication.UnicodeUTF8))
        self.handles_label.setText(QtGui.QApplication.translate("settings_frame", "Handles:", None, QtGui.QApplication.UnicodeUTF8))
        self.handles_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "handles", None, QtGui.QApplication.UnicodeUTF8))
        self.posterFrame_label.setText(QtGui.QApplication.translate("settings_frame", "Poster frame:", None, QtGui.QApplication.UnicodeUTF8))
        self.posterFrame_spinBox.setProperty("xmlTag", QtGui.QApplication.translate("settings_frame", "posterFrame", None, QtGui.QApplication.UnicodeUTF8))

