# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_job_metadata.ui'
#
# Created: Fri May 15 17:25:54 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 240)
        Frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.formLayout = QtGui.QFormLayout(Frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.projNum_label = QtGui.QLabel(Frame)
        self.projNum_label.setObjectName("projNum_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.projNum_label)
        self.projNum_spinBox = QtGui.QSpinBox(Frame)
        self.projNum_spinBox.setMinimum(0)
        self.projNum_spinBox.setMaximum(999999)
        self.projNum_spinBox.setProperty("value", 0)
        self.projNum_spinBox.setObjectName("projNum_spinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.projNum_spinBox)
        self.jobNum_label = QtGui.QLabel(Frame)
        self.jobNum_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.jobNum_label.setObjectName("jobNum_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.jobNum_label)
        self.jobNum_spinBox = QtGui.QSpinBox(Frame)
        self.jobNum_spinBox.setMinimum(0)
        self.jobNum_spinBox.setMaximum(9999999)
        self.jobNum_spinBox.setProperty("value", 0)
        self.jobNum_spinBox.setObjectName("jobNum_spinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.jobNum_spinBox)
        self.client_label = QtGui.QLabel(Frame)
        self.client_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.client_label.setObjectName("client_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.client_label)
        self.client_lineEdit = QtGui.QLineEdit(Frame)
        self.client_lineEdit.setObjectName("client_lineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.client_lineEdit)
        self.brand_label = QtGui.QLabel(Frame)
        self.brand_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.brand_label.setObjectName("brand_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.brand_label)
        self.brand_lineEdit = QtGui.QLineEdit(Frame)
        self.brand_lineEdit.setObjectName("brand_lineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.brand_lineEdit)
        self.title_label = QtGui.QLabel(Frame)
        self.title_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.title_label.setObjectName("title_label")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.title_label)
        self.title_lineEdit = QtGui.QLineEdit(Frame)
        self.title_lineEdit.setObjectName("title_lineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.title_lineEdit)
        self.deliverable_label = QtGui.QLabel(Frame)
        self.deliverable_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.deliverable_label.setObjectName("deliverable_label")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.deliverable_label)
        self.deliverable_lineEdit = QtGui.QLineEdit(Frame)
        self.deliverable_lineEdit.setObjectName("deliverable_lineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.deliverable_lineEdit)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.projNum_label.setText(QtGui.QApplication.translate("Frame", "Project number:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobNum_label.setText(QtGui.QApplication.translate("Frame", "Job number:", None, QtGui.QApplication.UnicodeUTF8))
        self.client_label.setText(QtGui.QApplication.translate("Frame", "Client:", None, QtGui.QApplication.UnicodeUTF8))
        self.brand_label.setText(QtGui.QApplication.translate("Frame", "Brand:", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("Frame", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.deliverable_label.setText(QtGui.QApplication.translate("Frame", "Deliverable:", None, QtGui.QApplication.UnicodeUTF8))

