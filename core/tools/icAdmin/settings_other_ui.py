# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_other_ui.ui'
#
# Created: Fri May 15 18:46:45 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 128)
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(Frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.board_label = QtGui.QLabel(Frame)
        self.board_label.setObjectName("board_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.board_label)
        self.board_lineEdit = QtGui.QLineEdit(Frame)
        self.board_lineEdit.setObjectName("board_lineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.board_lineEdit)
        self.label = QtGui.QLabel(Frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtGui.QLineEdit(Frame)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(Frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_2)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.board_label.setText(QtGui.QApplication.translate("Frame", "Production board:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Frame", "Project tools:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Frame", "Elements library:", None, QtGui.QApplication.UnicodeUTF8))

