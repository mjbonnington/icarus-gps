# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_time_ui.ui'
#
# Created: Fri May 15 18:46:59 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 160)
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(Frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.range_label = QtGui.QLabel(Frame)
        self.range_label.setObjectName("range_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.range_label)
        self.range_horizontalLayout = QtGui.QHBoxLayout()
        self.range_horizontalLayout.setObjectName("range_horizontalLayout")
        self.rangeStart_spinBox = QtGui.QSpinBox(Frame)
        self.rangeStart_spinBox.setMinimum(1)
        self.rangeStart_spinBox.setMaximum(9999)
        self.rangeStart_spinBox.setProperty("value", 1)
        self.rangeStart_spinBox.setObjectName("rangeStart_spinBox")
        self.range_horizontalLayout.addWidget(self.rangeStart_spinBox)
        self.rangeSep_label = QtGui.QLabel(Frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeSep_label.sizePolicy().hasHeightForWidth())
        self.rangeSep_label.setSizePolicy(sizePolicy)
        self.rangeSep_label.setObjectName("rangeSep_label")
        self.range_horizontalLayout.addWidget(self.rangeSep_label)
        self.rangeEnd_spinBox = QtGui.QSpinBox(Frame)
        self.rangeEnd_spinBox.setMinimum(1)
        self.rangeEnd_spinBox.setMaximum(9999)
        self.rangeEnd_spinBox.setProperty("value", 1)
        self.rangeEnd_spinBox.setObjectName("rangeEnd_spinBox")
        self.range_horizontalLayout.addWidget(self.rangeEnd_spinBox)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.range_horizontalLayout)
        self.fps_label = QtGui.QLabel(Frame)
        self.fps_label.setObjectName("fps_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fps_label)
        self.fps_spinBox = QtGui.QSpinBox(Frame)
        self.fps_spinBox.setMinimum(1)
        self.fps_spinBox.setMaximum(9999)
        self.fps_spinBox.setProperty("value", 25)
        self.fps_spinBox.setObjectName("fps_spinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fps_spinBox)
        self.handles_label = QtGui.QLabel(Frame)
        self.handles_label.setObjectName("handles_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.handles_label)
        self.handles_spinBox = QtGui.QSpinBox(Frame)
        self.handles_spinBox.setMaximum(9999)
        self.handles_spinBox.setProperty("value", 0)
        self.handles_spinBox.setObjectName("handles_spinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.handles_spinBox)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)
        Frame.setTabOrder(self.rangeStart_spinBox, self.rangeEnd_spinBox)
        Frame.setTabOrder(self.rangeEnd_spinBox, self.fps_spinBox)
        Frame.setTabOrder(self.fps_spinBox, self.handles_spinBox)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.range_label.setText(QtGui.QApplication.translate("Frame", "Frame range:", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeSep_label.setText(QtGui.QApplication.translate("Frame", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_label.setText(QtGui.QApplication.translate("Frame", "Frames per second:", None, QtGui.QApplication.UnicodeUTF8))
        self.handles_label.setText(QtGui.QApplication.translate("Frame", "Handles:", None, QtGui.QApplication.UnicodeUTF8))

