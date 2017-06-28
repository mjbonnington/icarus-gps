# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'versionManagerUI.ui'
#
# Created: Wed Jan  7 11:12:01 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(432, 432)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_frame = QtGui.QFrame(Dialog)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.asset_label = QtGui.QLabel(self.main_frame)
        self.asset_label.setText("")
        self.asset_label.setAlignment(QtCore.Qt.AlignCenter)
        self.asset_label.setObjectName("asset_label")
        self.verticalLayout_5.addWidget(self.asset_label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left_verticalLayout = QtGui.QVBoxLayout()
        self.left_verticalLayout.setObjectName("left_verticalLayout")
        self.version_label = QtGui.QLabel(self.main_frame)
        self.version_label.setObjectName("version_label")
        self.left_verticalLayout.addWidget(self.version_label)
        self.assetVersion_listWidget = QtGui.QListWidget(self.main_frame)
        self.assetVersion_listWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.assetVersion_listWidget.setAlternatingRowColors(True)
        self.assetVersion_listWidget.setObjectName("assetVersion_listWidget")
        self.left_verticalLayout.addWidget(self.assetVersion_listWidget)
        self.horizontalLayout_2.addLayout(self.left_verticalLayout)
        spacerItem = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.right_verticalLayout = QtGui.QVBoxLayout()
        self.right_verticalLayout.setObjectName("right_verticalLayout")
        self.preview_groupBox = QtGui.QGroupBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_groupBox.sizePolicy().hasHeightForWidth())
        self.preview_groupBox.setSizePolicy(sizePolicy)
        self.preview_groupBox.setObjectName("preview_groupBox")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.preview_groupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gatherImgPreview_label = QtGui.QLabel(self.preview_groupBox)
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
        self.right_verticalLayout.addWidget(self.preview_groupBox)
        self.info_groupBox = QtGui.QGroupBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_groupBox.sizePolicy().hasHeightForWidth())
        self.info_groupBox.setSizePolicy(sizePolicy)
        self.info_groupBox.setObjectName("info_groupBox")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.info_groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gatherInfo_textEdit = QtGui.QTextEdit(self.info_groupBox)
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
        self.verticalLayout_7.addWidget(self.gatherInfo_textEdit)
        self.right_verticalLayout.addWidget(self.info_groupBox)
        self.horizontalLayout_2.addLayout(self.right_verticalLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cancel_pushButton = QtGui.QPushButton(self.main_frame)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.horizontalLayout_3.addWidget(self.cancel_pushButton)
        self.update_pushButton = QtGui.QPushButton(self.main_frame)
        self.update_pushButton.setObjectName("update_pushButton")
        self.horizontalLayout_3.addWidget(self.update_pushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.main_frame)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Icarus Version Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.version_label.setText(QtGui.QApplication.translate("Dialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.preview_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.info_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.gatherInfo_textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Helvetica\'; font-size:11pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_pushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.update_pushButton.setText(QtGui.QApplication.translate("Dialog", "Update", None, QtGui.QApplication.UnicodeUTF8))

