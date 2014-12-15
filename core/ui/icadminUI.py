# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icadminUI.ui'
#
# Created: Wed Dec  3 16:46:00 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtGui.QWidget(MainWindow)
        font = QtGui.QFont()
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabJobList = QtGui.QWidget()
        self.tabJobList.setEnabled(True)
        self.tabJobList.setObjectName("tabJobList")
        self.verticalLayout = QtGui.QVBoxLayout(self.tabJobList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_jobs = QtGui.QListWidget(self.tabJobList)
        self.listWidget_jobs.setAcceptDrops(True)
        self.listWidget_jobs.setDragEnabled(True)
        self.listWidget_jobs.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.listWidget_jobs.setAlternatingRowColors(True)
        self.listWidget_jobs.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget_jobs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listWidget_jobs.setModelColumn(0)
        self.listWidget_jobs.setObjectName("listWidget_jobs")
        self.verticalLayout.addWidget(self.listWidget_jobs)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(self.tabJobList)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.tabJobList)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.tabJobList)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtGui.QPushButton(self.tabJobList)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_remove = QtGui.QPushButton(self.tabJobList)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.horizontalLayout.addWidget(self.pushButton_remove)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tabJobList, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.grpLowerButtons = QtGui.QHBoxLayout()
        self.grpLowerButtons.setObjectName("grpLowerButtons")
        self.btnApply = QtGui.QPushButton(self.centralwidget)
        self.btnApply.setObjectName("btnApply")
        self.grpLowerButtons.addWidget(self.btnApply)
        self.btnCancel = QtGui.QPushButton(self.centralwidget)
        self.btnCancel.setObjectName("btnCancel")
        self.grpLowerButtons.addWidget(self.btnCancel)
        self.verticalLayout_2.addLayout(self.grpLowerButtons)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Edit Jobs", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_add.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_remove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabJobList), QtGui.QApplication.translate("MainWindow", "Jobs", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApply.setText(QtGui.QApplication.translate("MainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

