# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_job_ui.ui'
#
# Created: Tue Aug 16 15:53:07 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 192)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.jobSettings_groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobSettings_groupBox.sizePolicy().hasHeightForWidth())
        self.jobSettings_groupBox.setSizePolicy(sizePolicy)
        self.jobSettings_groupBox.setObjectName("jobSettings_groupBox")
        self.formLayout_15 = QtGui.QFormLayout(self.jobSettings_groupBox)
        self.formLayout_15.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_15.setObjectName("formLayout_15")
        self.jobName_label = QtGui.QLabel(self.jobSettings_groupBox)
        self.jobName_label.setObjectName("jobName_label")
        self.formLayout_15.setWidget(0, QtGui.QFormLayout.LabelRole, self.jobName_label)
        self.jobName_horizontalLayout = QtGui.QHBoxLayout()
        self.jobName_horizontalLayout.setObjectName("jobName_horizontalLayout")
        self.jobName_lineEdit = QtGui.QLineEdit(self.jobSettings_groupBox)
        self.jobName_lineEdit.setText("")
        self.jobName_lineEdit.setObjectName("jobName_lineEdit")
        self.jobName_horizontalLayout.addWidget(self.jobName_lineEdit)
        self.formLayout_15.setLayout(0, QtGui.QFormLayout.FieldRole, self.jobName_horizontalLayout)
        self.jobPath_label = QtGui.QLabel(self.jobSettings_groupBox)
        self.jobPath_label.setObjectName("jobPath_label")
        self.formLayout_15.setWidget(1, QtGui.QFormLayout.LabelRole, self.jobPath_label)
        self.jobPath_horizontalLayout = QtGui.QHBoxLayout()
        self.jobPath_horizontalLayout.setObjectName("jobPath_horizontalLayout")
        self.jobPath_lineEdit = QtGui.QLineEdit(self.jobSettings_groupBox)
        self.jobPath_lineEdit.setText("")
        self.jobPath_lineEdit.setObjectName("jobPath_lineEdit")
        self.jobPath_horizontalLayout.addWidget(self.jobPath_lineEdit)
        self.jobPathBrowse_toolButton = QtGui.QToolButton(self.jobSettings_groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/rsc/rsc/icon_folder_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.jobPathBrowse_toolButton.setIcon(icon)
        self.jobPathBrowse_toolButton.setIconSize(QtCore.QSize(15, 15))
        self.jobPathBrowse_toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.jobPathBrowse_toolButton.setObjectName("jobPathBrowse_toolButton")
        self.jobPath_horizontalLayout.addWidget(self.jobPathBrowse_toolButton)
        self.formLayout_15.setLayout(1, QtGui.QFormLayout.FieldRole, self.jobPath_horizontalLayout)
        self.jobEnabled_checkBox = QtGui.QCheckBox(self.jobSettings_groupBox)
        self.jobEnabled_checkBox.setChecked(True)
        self.jobEnabled_checkBox.setObjectName("jobEnabled_checkBox")
        self.formLayout_15.setWidget(2, QtGui.QFormLayout.FieldRole, self.jobEnabled_checkBox)
        self.verticalLayout.addWidget(self.jobSettings_groupBox)
        spacerItem = QtGui.QSpacerItem(20, 156, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edit Job", None, QtGui.QApplication.UnicodeUTF8))
        self.jobSettings_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Job settings", None, QtGui.QApplication.UnicodeUTF8))
        self.jobName_label.setText(QtGui.QApplication.translate("Dialog", "Job name:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobPath_label.setText(QtGui.QApplication.translate("Dialog", "Job path:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobPathBrowse_toolButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.jobEnabled_checkBox.setText(QtGui.QApplication.translate("Dialog", "Enabled", None, QtGui.QApplication.UnicodeUTF8))

import rsc_rc
