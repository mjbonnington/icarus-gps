# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutUI.ui'
#
# Created: Mon May 11 16:44:41 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(640, 320)
        Dialog.setMinimumSize(QtCore.QSize(640, 320))
        Dialog.setMaximumSize(QtCore.QSize(640, 320))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.icBG_label = QtGui.QLabel(Dialog)
        self.icBG_label.setGeometry(QtCore.QRect(0, 0, 640, 320))
        self.icBG_label.setText("")
        self.icBG_label.setPixmap(QtGui.QPixmap(":/bg/rsc/icarus_about_bg.jpg"))
        self.icBG_label.setObjectName("icBG_label")
        self.aboutMessage_label = QtGui.QLabel(Dialog)
        self.aboutMessage_label.setGeometry(QtCore.QRect(16, 16, 608, 288))
        self.aboutMessage_label.setStyleSheet("background: transparent;\n"
"color: #FFF;\n"
"")
        self.aboutMessage_label.setObjectName("aboutMessage_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutMessage_label.setText(QtGui.QApplication.translate("Dialog", "I   C   A   R   U   S", None, QtGui.QApplication.UnicodeUTF8))

import about_rc
