# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_root_paths_ui.ui'
#
# Created: Tue Aug 16 19:16:21 2016
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
        self.jobRootPaths_groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobRootPaths_groupBox.sizePolicy().hasHeightForWidth())
        self.jobRootPaths_groupBox.setSizePolicy(sizePolicy)
        self.jobRootPaths_groupBox.setObjectName("jobRootPaths_groupBox")
        self.formLayout_15 = QtGui.QFormLayout(self.jobRootPaths_groupBox)
        self.formLayout_15.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_15.setObjectName("formLayout_15")
        self.jobRootPathOSX_label = QtGui.QLabel(self.jobRootPaths_groupBox)
        self.jobRootPathOSX_label.setObjectName("jobRootPathOSX_label")
        self.formLayout_15.setWidget(1, QtGui.QFormLayout.LabelRole, self.jobRootPathOSX_label)
        self.jobRootPathOSX_horizontalLayout = QtGui.QHBoxLayout()
        self.jobRootPathOSX_horizontalLayout.setObjectName("jobRootPathOSX_horizontalLayout")
        self.jobRootPathOSX_lineEdit = QtGui.QLineEdit(self.jobRootPaths_groupBox)
        self.jobRootPathOSX_lineEdit.setObjectName("jobRootPathOSX_lineEdit")
        self.jobRootPathOSX_horizontalLayout.addWidget(self.jobRootPathOSX_lineEdit)
        self.formLayout_15.setLayout(1, QtGui.QFormLayout.FieldRole, self.jobRootPathOSX_horizontalLayout)
        self.jobRootPathLinux_label = QtGui.QLabel(self.jobRootPaths_groupBox)
        self.jobRootPathLinux_label.setObjectName("jobRootPathLinux_label")
        self.formLayout_15.setWidget(2, QtGui.QFormLayout.LabelRole, self.jobRootPathLinux_label)
        self.jobRootPathLinux_horizontalLayout = QtGui.QHBoxLayout()
        self.jobRootPathLinux_horizontalLayout.setObjectName("jobRootPathLinux_horizontalLayout")
        self.jobRootPathLinux_lineEdit = QtGui.QLineEdit(self.jobRootPaths_groupBox)
        self.jobRootPathLinux_lineEdit.setObjectName("jobRootPathLinux_lineEdit")
        self.jobRootPathLinux_horizontalLayout.addWidget(self.jobRootPathLinux_lineEdit)
        self.formLayout_15.setLayout(2, QtGui.QFormLayout.FieldRole, self.jobRootPathLinux_horizontalLayout)
        self.jobRootPathWin_label = QtGui.QLabel(self.jobRootPaths_groupBox)
        self.jobRootPathWin_label.setObjectName("jobRootPathWin_label")
        self.formLayout_15.setWidget(0, QtGui.QFormLayout.LabelRole, self.jobRootPathWin_label)
        self.jobRootPathWin_horizontalLayout = QtGui.QHBoxLayout()
        self.jobRootPathWin_horizontalLayout.setObjectName("jobRootPathWin_horizontalLayout")
        self.jobRootPathWin_lineEdit = QtGui.QLineEdit(self.jobRootPaths_groupBox)
        self.jobRootPathWin_lineEdit.setObjectName("jobRootPathWin_lineEdit")
        self.jobRootPathWin_horizontalLayout.addWidget(self.jobRootPathWin_lineEdit)
        self.formLayout_15.setLayout(0, QtGui.QFormLayout.FieldRole, self.jobRootPathWin_horizontalLayout)
        self.verticalLayout.addWidget(self.jobRootPaths_groupBox)
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
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edit Root Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPaths_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Jobs root paths", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathOSX_label.setText(QtGui.QApplication.translate("Dialog", "Mac:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathOSX_lineEdit.setText(QtGui.QApplication.translate("Dialog", "/Volumes/hggl_SAN_1", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathLinux_label.setText(QtGui.QApplication.translate("Dialog", "Linux:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathLinux_lineEdit.setText(QtGui.QApplication.translate("Dialog", "/Volumes/hggl_SAN_1", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathWin_label.setText(QtGui.QApplication.translate("Dialog", "Windows:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobRootPathWin_lineEdit.setText(QtGui.QApplication.translate("Dialog", "Z:", None, QtGui.QApplication.UnicodeUTF8))

