# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slave_ui.ui'
#
# Created: Wed May 18 17:29:27 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 320)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.info_groupBox = QtGui.QGroupBox(Dialog)
        self.info_groupBox.setCheckable(False)
        self.info_groupBox.setObjectName("info_groupBox")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.info_groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.info_lineEdit = QtGui.QLineEdit(self.info_groupBox)
        self.info_lineEdit.setText("")
        self.info_lineEdit.setReadOnly(True)
        self.info_lineEdit.setObjectName("info_lineEdit")
        self.verticalLayout_3.addWidget(self.info_lineEdit)
        self.output_textEdit = QtGui.QTextEdit(self.info_groupBox)
        self.output_textEdit.setReadOnly(True)
        self.output_textEdit.setObjectName("output_textEdit")
        self.verticalLayout_3.addWidget(self.output_textEdit)
        self.stopAfterTask_checkBox = QtGui.QCheckBox(self.info_groupBox)
        self.stopAfterTask_checkBox.setObjectName("stopAfterTask_checkBox")
        self.verticalLayout_3.addWidget(self.stopAfterTask_checkBox)
        self.verticalLayout_2.addWidget(self.info_groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox_horizontalLayout = QtGui.QHBoxLayout()
        self.buttonBox_horizontalLayout.setObjectName("buttonBox_horizontalLayout")
        self.close_pushButton = QtGui.QPushButton(Dialog)
        self.close_pushButton.setAutoDefault(False)
        self.close_pushButton.setObjectName("close_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.close_pushButton)
        self.verticalLayout_2.addLayout(self.buttonBox_horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Render Slave", None, QtGui.QApplication.UnicodeUTF8))
        self.info_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "Allows the frame range(s) to be explicitly stated. If unchecked, the start and end frames will be read from the scene.", None, QtGui.QApplication.UnicodeUTF8))
        self.info_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Job / Task information", None, QtGui.QApplication.UnicodeUTF8))
        self.info_lineEdit.setToolTip(QtGui.QApplication.translate("Dialog", "List of frames to be rendered. Individual frames should be separated with commas, and sequences can be specified using a hyphen, e.g. 1, 5-10.", None, QtGui.QApplication.UnicodeUTF8))
        self.stopAfterTask_checkBox.setText(QtGui.QApplication.translate("Dialog", "Stop after current task", None, QtGui.QApplication.UnicodeUTF8))
        self.close_pushButton.setText(QtGui.QApplication.translate("Dialog", "Stop Slave", None, QtGui.QApplication.UnicodeUTF8))

