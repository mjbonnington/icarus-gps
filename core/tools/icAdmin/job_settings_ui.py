# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'job_settings_ui.ui'
#
# Created: Tue May 19 18:21:05 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 384)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.categories_listWidget = QtGui.QListWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categories_listWidget.sizePolicy().hasHeightForWidth())
        self.categories_listWidget.setSizePolicy(sizePolicy)
        self.categories_listWidget.setObjectName("categories_listWidget")
        self.horizontalLayout.addWidget(self.categories_listWidget)
        self.settings_scrollArea = QtGui.QScrollArea(Dialog)
        self.settings_scrollArea.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_scrollArea.sizePolicy().hasHeightForWidth())
        self.settings_scrollArea.setSizePolicy(sizePolicy)
        self.settings_scrollArea.setStyleSheet("")
        self.settings_scrollArea.setWidgetResizable(True)
        self.settings_scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.settings_scrollArea.setProperty("noBackground", True)
        self.settings_scrollArea.setObjectName("settings_scrollArea")
        self.settings_scrollAreaWidgetContents = QtGui.QWidget()
        self.settings_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 218, 316))
        self.settings_scrollAreaWidgetContents.setObjectName("settings_scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.settings_scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.settings_frame = QtGui.QFrame(self.settings_scrollAreaWidgetContents)
        self.settings_frame.setFrameShape(QtGui.QFrame.Box)
        self.settings_frame.setObjectName("settings_frame")
        self.formLayout = QtGui.QFormLayout(self.settings_frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.settings_frame)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.verticalLayout_2.addWidget(self.settings_frame)
        self.settings_scrollArea.setWidget(self.settings_scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.settings_scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.jobSettings_buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.jobSettings_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.Save)
        self.jobSettings_buttonBox.setObjectName("jobSettings_buttonBox")
        self.verticalLayout.addWidget(self.jobSettings_buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.jobSettings_buttonBox, self.categories_listWidget)
        Dialog.setTabOrder(self.categories_listWidget, self.settings_scrollArea)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Job Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "No settings loaded", None, QtGui.QApplication.UnicodeUTF8))

