# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'submit_ui.ui'
#
# Created: Thu May  7 14:07:45 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 256)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_frame = QtGui.QFrame(Dialog)
        self.main_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.main_frame.setLineWidth(0)
        self.main_frame.setObjectName("main_frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.main_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scene_horizontalLayout = QtGui.QHBoxLayout()
        self.scene_horizontalLayout.setObjectName("scene_horizontalLayout")
        self.scene_label = QtGui.QLabel(self.main_frame)
        self.scene_label.setObjectName("scene_label")
        self.scene_horizontalLayout.addWidget(self.scene_label)
        self.scene_comboBox = QtGui.QComboBox(self.main_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_comboBox.sizePolicy().hasHeightForWidth())
        self.scene_comboBox.setSizePolicy(sizePolicy)
        self.scene_comboBox.setEditable(False)
        self.scene_comboBox.setMaxCount(10)
        self.scene_comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.scene_comboBox.setObjectName("scene_comboBox")
        self.scene_horizontalLayout.addWidget(self.scene_comboBox)
        self.sceneBrowse_toolButton = QtGui.QToolButton(self.main_frame)
        self.sceneBrowse_toolButton.setObjectName("sceneBrowse_toolButton")
        self.scene_horizontalLayout.addWidget(self.sceneBrowse_toolButton)
        self.verticalLayout.addLayout(self.scene_horizontalLayout)
        self.line = QtGui.QFrame(self.main_frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.overrideFrameRange_groupBox = QtGui.QGroupBox(self.main_frame)
        self.overrideFrameRange_groupBox.setCheckable(True)
        self.overrideFrameRange_groupBox.setObjectName("overrideFrameRange_groupBox")
        self.formLayout = QtGui.QFormLayout(self.overrideFrameRange_groupBox)
        self.formLayout.setObjectName("formLayout")
        self.taskSize_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.taskSize_label.setObjectName("taskSize_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.taskSize_label)
        self.taskSize_spinBox = QtGui.QSpinBox(self.overrideFrameRange_groupBox)
        self.taskSize_spinBox.setMinimum(1)
        self.taskSize_spinBox.setObjectName("taskSize_spinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.taskSize_spinBox)
        self.frameRange_label = QtGui.QLabel(self.overrideFrameRange_groupBox)
        self.frameRange_label.setObjectName("frameRange_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.frameRange_label)
        self.frameRange_lineEdit = QtGui.QLineEdit(self.overrideFrameRange_groupBox)
        self.frameRange_lineEdit.setText("")
        self.frameRange_lineEdit.setObjectName("frameRange_lineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.frameRange_lineEdit)
        self.verticalLayout.addWidget(self.overrideFrameRange_groupBox)
        self.verticalLayout_2.addWidget(self.main_frame)
        spacerItem = QtGui.QSpacerItem(20, 12, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox_horizontalLayout = QtGui.QHBoxLayout()
        self.buttonBox_horizontalLayout.setObjectName("buttonBox_horizontalLayout")
        self.submit_pushButton = QtGui.QPushButton(Dialog)
        self.submit_pushButton.setAutoDefault(False)
        self.submit_pushButton.setObjectName("submit_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.submit_pushButton)
        self.killComplete_pushButton = QtGui.QPushButton(Dialog)
        self.killComplete_pushButton.setAutoDefault(False)
        self.killComplete_pushButton.setObjectName("killComplete_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.killComplete_pushButton)
        self.close_pushButton = QtGui.QPushButton(Dialog)
        self.close_pushButton.setAutoDefault(False)
        self.close_pushButton.setObjectName("close_pushButton")
        self.buttonBox_horizontalLayout.addWidget(self.close_pushButton)
        self.verticalLayout_2.addLayout(self.buttonBox_horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.submit_pushButton, self.killComplete_pushButton)
        Dialog.setTabOrder(self.killComplete_pushButton, self.close_pushButton)
        Dialog.setTabOrder(self.close_pushButton, self.scene_comboBox)
        Dialog.setTabOrder(self.scene_comboBox, self.sceneBrowse_toolButton)
        Dialog.setTabOrder(self.sceneBrowse_toolButton, self.overrideFrameRange_groupBox)
        Dialog.setTabOrder(self.overrideFrameRange_groupBox, self.frameRange_lineEdit)
        Dialog.setTabOrder(self.frameRange_lineEdit, self.taskSize_spinBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Submit Command-Line Render", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_label.setText(QtGui.QApplication.translate("Dialog", "Scene:", None, QtGui.QApplication.UnicodeUTF8))
        self.sceneBrowse_toolButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setToolTip(QtGui.QApplication.translate("Dialog", "Allows the frame range(s) to be explicitly stated. If unchecked, the start and end frames will be read from the scene", None, QtGui.QApplication.UnicodeUTF8))
        self.overrideFrameRange_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Override frame range", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_label.setText(QtGui.QApplication.translate("Dialog", "Task size:", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setToolTip(QtGui.QApplication.translate("Dialog", "How many frames to submit for each task", None, QtGui.QApplication.UnicodeUTF8))
        self.taskSize_spinBox.setSuffix(QtGui.QApplication.translate("Dialog", " frame(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_label.setText(QtGui.QApplication.translate("Dialog", "Frame range:", None, QtGui.QApplication.UnicodeUTF8))
        self.frameRange_lineEdit.setToolTip(QtGui.QApplication.translate("Dialog", "List of frames to be rendered. Individual frames should be separated with commas, and sequences can be specified using a hyphen, e.g. 1, 5-10", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_pushButton.setText(QtGui.QApplication.translate("Dialog", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.killComplete_pushButton.setText(QtGui.QApplication.translate("Dialog", "Kill/Complete", None, QtGui.QApplication.UnicodeUTF8))
        self.close_pushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
