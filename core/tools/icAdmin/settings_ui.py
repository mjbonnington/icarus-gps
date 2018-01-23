# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created: Mon Jan 22 15:31:02 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 384)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.categories_listWidget = QtGui.QListWidget(self.splitter)
        self.categories_listWidget.setObjectName("categories_listWidget")
        self.settings_scrollArea = QtGui.QScrollArea(self.splitter)
        self.settings_scrollArea.setStyleSheet("")
        self.settings_scrollArea.setWidgetResizable(True)
        self.settings_scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.settings_scrollArea.setProperty("noBackground", True)
        self.settings_scrollArea.setObjectName("settings_scrollArea")
        self.settings_scrollAreaWidgetContents = QtGui.QWidget()
        self.settings_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 150, 337))
        self.settings_scrollAreaWidgetContents.setProperty("noBackground", True)
        self.settings_scrollAreaWidgetContents.setObjectName("settings_scrollAreaWidgetContents")
        self.settings_verticalLayout = QtGui.QVBoxLayout(self.settings_scrollAreaWidgetContents)
        self.settings_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.settings_verticalLayout.setObjectName("settings_verticalLayout")
        self.settings_frame = QtGui.QFrame(self.settings_scrollAreaWidgetContents)
        self.settings_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.settings_frame.setObjectName("settings_frame")
        self.formLayout = QtGui.QFormLayout(self.settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.placeholder_label = QtGui.QLabel(self.settings_frame)
        self.placeholder_label.setObjectName("placeholder_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.placeholder_label)
        self.settings_verticalLayout.addWidget(self.settings_frame)
        self.settings_scrollArea.setWidget(self.settings_scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.splitter)
        self.settings_buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.settings_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.Save)
        self.settings_buttonBox.setObjectName("settings_buttonBox")
        self.verticalLayout.addWidget(self.settings_buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.placeholder_label.setText(QtGui.QApplication.translate("Dialog", "No settings loaded", None, QtGui.QApplication.UnicodeUTF8))

