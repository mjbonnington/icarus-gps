# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'versionManagerUI.ui'
#
# Created: Tue Jul 12 17:26:33 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(432, 352)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.asset_label = QtGui.QLabel(Dialog)
        self.asset_label.setObjectName("asset_label")
        self.verticalLayout_3.addWidget(self.asset_label)
        self.main_frame = QtGui.QFrame(Dialog)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.main_frame.setObjectName("main_frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.main_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.assetVersion_listWidget = QtGui.QListWidget(self.main_frame)
        self.assetVersion_listWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.assetVersion_listWidget.setAlternatingRowColors(True)
        self.assetVersion_listWidget.setObjectName("assetVersion_listWidget")
        self.horizontalLayout.addWidget(self.assetVersion_listWidget)
        self.previewInfo_frame = QtGui.QFrame(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewInfo_frame.sizePolicy().hasHeightForWidth())
        self.previewInfo_frame.setSizePolicy(sizePolicy)
        self.previewInfo_frame.setObjectName("previewInfo_frame")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.previewInfo_frame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gatherImgPreview_label = QtGui.QLabel(self.previewInfo_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gatherImgPreview_label.sizePolicy().hasHeightForWidth())
        self.gatherImgPreview_label.setSizePolicy(sizePolicy)
        self.gatherImgPreview_label.setMinimumSize(QtCore.QSize(256, 144))
        self.gatherImgPreview_label.setMaximumSize(QtCore.QSize(256, 144))
        self.gatherImgPreview_label.setFrameShape(QtGui.QFrame.NoFrame)
        self.gatherImgPreview_label.setText("")
        self.gatherImgPreview_label.setObjectName("gatherImgPreview_label")
        self.verticalLayout_6.addWidget(self.gatherImgPreview_label)
        self.gatherInfo_textEdit = QtGui.QTextEdit(self.previewInfo_frame)
        self.gatherInfo_textEdit.setMaximumSize(QtCore.QSize(256, 16777215))
        self.gatherInfo_textEdit.setStyleSheet("QTextEdit, QPlainTextEdit, QListView {\n"
"    background: transparent;\n"
"    border-color: transparent;\n"
"}\n"
"")
        self.gatherInfo_textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.gatherInfo_textEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.gatherInfo_textEdit.setReadOnly(True)
        self.gatherInfo_textEdit.setObjectName("gatherInfo_textEdit")
        self.verticalLayout_6.addWidget(self.gatherInfo_textEdit)
        self.horizontalLayout.addWidget(self.previewInfo_frame)
        self.verticalLayout_3.addWidget(self.main_frame)
        self.buttonBox_horizontalLayout = QtGui.QHBoxLayout()
        self.buttonBox_horizontalLayout.setObjectName("buttonBox_horizontalLayout")
        self.update_pushButton = QtGui.QPushButton(Dialog)
        self.update_pushButton.setObjectName("update_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.update_pushButton)
        self.cancel_pushButton = QtGui.QPushButton(Dialog)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.cancel_pushButton)
        self.verticalLayout_3.addLayout(self.buttonBox_horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Icarus Version Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_label.setText(QtGui.QApplication.translate("Dialog", "<AssetName>", None, QtGui.QApplication.UnicodeUTF8))
        self.gatherInfo_textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Helvetica\'; font-size:11pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.update_pushButton.setText(QtGui.QApplication.translate("Dialog", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

