# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pDialogUI.ui'
#
# Created: Mon Dec 15 16:56:46 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(384, 256)
        Dialog.setStyleSheet("")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_frame = QtGui.QFrame(Dialog)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.message_textEdit = QtGui.QTextEdit(self.main_frame)
        self.message_textEdit.setReadOnly(True)
        self.message_textEdit.setObjectName("message_textEdit")
        self.verticalLayout.addWidget(self.message_textEdit)
        self.frame = QtGui.QFrame(self.main_frame)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_pushButton = QtGui.QPushButton(self.frame)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.horizontalLayout.addWidget(self.cancel_pushButton)
        self.ok_pushButton = QtGui.QPushButton(self.frame)
        self.ok_pushButton.setDefault(True)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.horizontalLayout.addWidget(self.ok_pushButton)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2.addWidget(self.main_frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.message_textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Helvetica\'; font-size:12pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_pushButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

