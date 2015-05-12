# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'job_settings_ui.ui'
#
# Created: Tue May 12 13:20:08 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(576, 384)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.jobProperties_scrollArea = QtGui.QScrollArea(Dialog)
        self.jobProperties_scrollArea.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobProperties_scrollArea.sizePolicy().hasHeightForWidth())
        self.jobProperties_scrollArea.setSizePolicy(sizePolicy)
        self.jobProperties_scrollArea.setStyleSheet("")
        self.jobProperties_scrollArea.setWidgetResizable(True)
        self.jobProperties_scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.jobProperties_scrollArea.setProperty("noBackground", True)
        self.jobProperties_scrollArea.setObjectName("jobProperties_scrollArea")
        self.jobProperties_scrollAreaWidgetContents = QtGui.QWidget()
        self.jobProperties_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 535, 799))
        self.jobProperties_scrollAreaWidgetContents.setObjectName("jobProperties_scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.jobProperties_scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.job_groupBox = QtGui.QGroupBox(self.jobProperties_scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.job_groupBox.sizePolicy().hasHeightForWidth())
        self.job_groupBox.setSizePolicy(sizePolicy)
        self.job_groupBox.setObjectName("job_groupBox")
        self.formLayout = QtGui.QFormLayout(self.job_groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.projNum_label = QtGui.QLabel(self.job_groupBox)
        self.projNum_label.setObjectName("projNum_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.projNum_label)
        self.projNum_spinBox = QtGui.QSpinBox(self.job_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projNum_spinBox.sizePolicy().hasHeightForWidth())
        self.projNum_spinBox.setSizePolicy(sizePolicy)
        self.projNum_spinBox.setMinimum(0)
        self.projNum_spinBox.setMaximum(999999)
        self.projNum_spinBox.setProperty("value", 123456)
        self.projNum_spinBox.setObjectName("projNum_spinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.projNum_spinBox)
        self.jobNum_label = QtGui.QLabel(self.job_groupBox)
        self.jobNum_label.setObjectName("jobNum_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.jobNum_label)
        self.jobNum_spinBox = QtGui.QSpinBox(self.job_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobNum_spinBox.sizePolicy().hasHeightForWidth())
        self.jobNum_spinBox.setSizePolicy(sizePolicy)
        self.jobNum_spinBox.setMinimum(0)
        self.jobNum_spinBox.setMaximum(9999999)
        self.jobNum_spinBox.setProperty("value", 1234567)
        self.jobNum_spinBox.setObjectName("jobNum_spinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.jobNum_spinBox)
        self.client_lineEdit = QtGui.QLineEdit(self.job_groupBox)
        self.client_lineEdit.setObjectName("client_lineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.client_lineEdit)
        self.brand_label = QtGui.QLabel(self.job_groupBox)
        self.brand_label.setObjectName("brand_label")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.brand_label)
        self.brand_lineEdit = QtGui.QLineEdit(self.job_groupBox)
        self.brand_lineEdit.setObjectName("brand_lineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.brand_lineEdit)
        self.title_label = QtGui.QLabel(self.job_groupBox)
        self.title_label.setObjectName("title_label")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.title_label)
        self.deliverable_label = QtGui.QLabel(self.job_groupBox)
        self.deliverable_label.setObjectName("deliverable_label")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.deliverable_label)
        self.client_label = QtGui.QLabel(self.job_groupBox)
        self.client_label.setObjectName("client_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.client_label)
        self.title_lineEdit = QtGui.QLineEdit(self.job_groupBox)
        self.title_lineEdit.setObjectName("title_lineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.title_lineEdit)
        self.deliverable_lineEdit = QtGui.QLineEdit(self.job_groupBox)
        self.deliverable_lineEdit.setObjectName("deliverable_lineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.deliverable_lineEdit)
        self.verticalLayout_2.addWidget(self.job_groupBox)
        self.time_groupBox = QtGui.QGroupBox(self.jobProperties_scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_groupBox.sizePolicy().hasHeightForWidth())
        self.time_groupBox.setSizePolicy(sizePolicy)
        self.time_groupBox.setObjectName("time_groupBox")
        self.formLayout_4 = QtGui.QFormLayout(self.time_groupBox)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.fps_label = QtGui.QLabel(self.time_groupBox)
        self.fps_label.setObjectName("fps_label")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.fps_label)
        self.fps_spinBox = QtGui.QSpinBox(self.time_groupBox)
        self.fps_spinBox.setMinimum(1)
        self.fps_spinBox.setMaximum(5000)
        self.fps_spinBox.setProperty("value", 25)
        self.fps_spinBox.setObjectName("fps_spinBox")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.fps_spinBox)
        self.range_label = QtGui.QLabel(self.time_groupBox)
        self.range_label.setEnabled(False)
        self.range_label.setObjectName("range_label")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.range_label)
        self.range_horizontalLayout = QtGui.QHBoxLayout()
        self.range_horizontalLayout.setObjectName("range_horizontalLayout")
        self.in_spinBox = QtGui.QSpinBox(self.time_groupBox)
        self.in_spinBox.setEnabled(False)
        self.in_spinBox.setMinimum(1)
        self.in_spinBox.setMaximum(9999)
        self.in_spinBox.setProperty("value", 1001)
        self.in_spinBox.setObjectName("in_spinBox")
        self.range_horizontalLayout.addWidget(self.in_spinBox)
        self.rangeSep_label = QtGui.QLabel(self.time_groupBox)
        self.rangeSep_label.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rangeSep_label.sizePolicy().hasHeightForWidth())
        self.rangeSep_label.setSizePolicy(sizePolicy)
        self.rangeSep_label.setObjectName("rangeSep_label")
        self.range_horizontalLayout.addWidget(self.rangeSep_label)
        self.out_spinBox = QtGui.QSpinBox(self.time_groupBox)
        self.out_spinBox.setEnabled(False)
        self.out_spinBox.setMinimum(1)
        self.out_spinBox.setMaximum(9999)
        self.out_spinBox.setProperty("value", 1100)
        self.out_spinBox.setObjectName("out_spinBox")
        self.range_horizontalLayout.addWidget(self.out_spinBox)
        self.formLayout_4.setLayout(1, QtGui.QFormLayout.FieldRole, self.range_horizontalLayout)
        self.handles_label = QtGui.QLabel(self.time_groupBox)
        self.handles_label.setObjectName("handles_label")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.handles_label)
        self.handles_spinBox = QtGui.QSpinBox(self.time_groupBox)
        self.handles_spinBox.setMaximum(9999)
        self.handles_spinBox.setProperty("value", 10)
        self.handles_spinBox.setObjectName("handles_spinBox")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.handles_spinBox)
        self.verticalLayout_2.addWidget(self.time_groupBox)
        self.res_groupBox = QtGui.QGroupBox(self.jobProperties_scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.res_groupBox.sizePolicy().hasHeightForWidth())
        self.res_groupBox.setSizePolicy(sizePolicy)
        self.res_groupBox.setObjectName("res_groupBox")
        self.formLayout_6 = QtGui.QFormLayout(self.res_groupBox)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_6.setObjectName("formLayout_6")
        self.resPreset_label = QtGui.QLabel(self.res_groupBox)
        self.resPreset_label.setObjectName("resPreset_label")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.resPreset_label)
        self.resPreset_comboBox = QtGui.QComboBox(self.res_groupBox)
        self.resPreset_comboBox.setObjectName("resPreset_comboBox")
        self.resPreset_comboBox.addItem("")
        self.resPreset_comboBox.addItem("")
        self.resPreset_comboBox.addItem("")
        self.resPreset_comboBox.addItem("")
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.resPreset_comboBox)
        self.res_label = QtGui.QLabel(self.res_groupBox)
        self.res_label.setObjectName("res_label")
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.res_label)
        self.res_horizontalLayout = QtGui.QHBoxLayout()
        self.res_horizontalLayout.setObjectName("res_horizontalLayout")
        self.resX_spinBox = QtGui.QSpinBox(self.res_groupBox)
        self.resX_spinBox.setMinimum(1)
        self.resX_spinBox.setMaximum(99999)
        self.resX_spinBox.setProperty("value", 1920)
        self.resX_spinBox.setObjectName("resX_spinBox")
        self.res_horizontalLayout.addWidget(self.resX_spinBox)
        self.resSep_label = QtGui.QLabel(self.res_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resSep_label.sizePolicy().hasHeightForWidth())
        self.resSep_label.setSizePolicy(sizePolicy)
        self.resSep_label.setObjectName("resSep_label")
        self.res_horizontalLayout.addWidget(self.resSep_label)
        self.resY_spinBox = QtGui.QSpinBox(self.res_groupBox)
        self.resY_spinBox.setMinimum(1)
        self.resY_spinBox.setMaximum(99999)
        self.resY_spinBox.setProperty("value", 1080)
        self.resY_spinBox.setObjectName("resY_spinBox")
        self.res_horizontalLayout.addWidget(self.resY_spinBox)
        self.formLayout_6.setLayout(2, QtGui.QFormLayout.FieldRole, self.res_horizontalLayout)
        self.proxyMode_label = QtGui.QLabel(self.res_groupBox)
        self.proxyMode_label.setObjectName("proxyMode_label")
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.LabelRole, self.proxyMode_label)
        self.proxyMode_horizontalLayout = QtGui.QHBoxLayout()
        self.proxyMode_horizontalLayout.setObjectName("proxyMode_horizontalLayout")
        self.scale_radioButton = QtGui.QRadioButton(self.res_groupBox)
        self.scale_radioButton.setChecked(True)
        self.scale_radioButton.setObjectName("scale_radioButton")
        self.proxyMode_horizontalLayout.addWidget(self.scale_radioButton)
        self.res_radioButton = QtGui.QRadioButton(self.res_groupBox)
        self.res_radioButton.setObjectName("res_radioButton")
        self.proxyMode_horizontalLayout.addWidget(self.res_radioButton)
        self.formLayout_6.setLayout(3, QtGui.QFormLayout.FieldRole, self.proxyMode_horizontalLayout)
        self.proxyScale_label = QtGui.QLabel(self.res_groupBox)
        self.proxyScale_label.setObjectName("proxyScale_label")
        self.formLayout_6.setWidget(4, QtGui.QFormLayout.LabelRole, self.proxyScale_label)
        self.proxyScale_horizontalLayout = QtGui.QHBoxLayout()
        self.proxyScale_horizontalLayout.setObjectName("proxyScale_horizontalLayout")
        self.proxyScale_doubleSpinBox = QtGui.QDoubleSpinBox(self.res_groupBox)
        self.proxyScale_doubleSpinBox.setMaximum(1.0)
        self.proxyScale_doubleSpinBox.setSingleStep(0.01)
        self.proxyScale_doubleSpinBox.setProperty("value", 0.5)
        self.proxyScale_doubleSpinBox.setObjectName("proxyScale_doubleSpinBox")
        self.proxyScale_horizontalLayout.addWidget(self.proxyScale_doubleSpinBox)
        self.formLayout_6.setLayout(4, QtGui.QFormLayout.FieldRole, self.proxyScale_horizontalLayout)
        self.proxyRes_label = QtGui.QLabel(self.res_groupBox)
        self.proxyRes_label.setObjectName("proxyRes_label")
        self.formLayout_6.setWidget(5, QtGui.QFormLayout.LabelRole, self.proxyRes_label)
        self.proxyRes_horizontalLayout = QtGui.QHBoxLayout()
        self.proxyRes_horizontalLayout.setObjectName("proxyRes_horizontalLayout")
        self.proxyResX_spinBox = QtGui.QSpinBox(self.res_groupBox)
        self.proxyResX_spinBox.setMinimum(1)
        self.proxyResX_spinBox.setMaximum(99999)
        self.proxyResX_spinBox.setProperty("value", 960)
        self.proxyResX_spinBox.setObjectName("proxyResX_spinBox")
        self.proxyRes_horizontalLayout.addWidget(self.proxyResX_spinBox)
        self.proxyResSep_label = QtGui.QLabel(self.res_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxyResSep_label.sizePolicy().hasHeightForWidth())
        self.proxyResSep_label.setSizePolicy(sizePolicy)
        self.proxyResSep_label.setObjectName("proxyResSep_label")
        self.proxyRes_horizontalLayout.addWidget(self.proxyResSep_label)
        self.proxyResY_spinBox = QtGui.QSpinBox(self.res_groupBox)
        self.proxyResY_spinBox.setMinimum(1)
        self.proxyResY_spinBox.setMaximum(99999)
        self.proxyResY_spinBox.setProperty("value", 540)
        self.proxyResY_spinBox.setObjectName("proxyResY_spinBox")
        self.proxyRes_horizontalLayout.addWidget(self.proxyResY_spinBox)
        self.formLayout_6.setLayout(5, QtGui.QFormLayout.FieldRole, self.proxyRes_horizontalLayout)
        self.preserveAR_checkBox = QtGui.QCheckBox(self.res_groupBox)
        self.preserveAR_checkBox.setChecked(True)
        self.preserveAR_checkBox.setObjectName("preserveAR_checkBox")
        self.formLayout_6.setWidget(6, QtGui.QFormLayout.FieldRole, self.preserveAR_checkBox)
        self.verticalLayout_2.addWidget(self.res_groupBox)
        self.apps_groupBox = QtGui.QGroupBox(self.jobProperties_scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apps_groupBox.sizePolicy().hasHeightForWidth())
        self.apps_groupBox.setSizePolicy(sizePolicy)
        self.apps_groupBox.setObjectName("apps_groupBox")
        self.formLayout_3 = QtGui.QFormLayout(self.apps_groupBox)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.maya_label = QtGui.QLabel(self.apps_groupBox)
        self.maya_label.setObjectName("maya_label")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.maya_label)
        self.maya_comboBox = QtGui.QComboBox(self.apps_groupBox)
        self.maya_comboBox.setObjectName("maya_comboBox")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.maya_comboBox)
        self.mudbox_label = QtGui.QLabel(self.apps_groupBox)
        self.mudbox_label.setObjectName("mudbox_label")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.mudbox_label)
        self.mudbox_comboBox = QtGui.QComboBox(self.apps_groupBox)
        self.mudbox_comboBox.setObjectName("mudbox_comboBox")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.mudbox_comboBox)
        self.verticalLayout_2.addWidget(self.apps_groupBox)
        self.other_groupBox = QtGui.QGroupBox(self.jobProperties_scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.other_groupBox.sizePolicy().hasHeightForWidth())
        self.other_groupBox.setSizePolicy(sizePolicy)
        self.other_groupBox.setObjectName("other_groupBox")
        self.formLayout_7 = QtGui.QFormLayout(self.other_groupBox)
        self.formLayout_7.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_7.setObjectName("formLayout_7")
        self.board_label = QtGui.QLabel(self.other_groupBox)
        self.board_label.setObjectName("board_label")
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.board_label)
        self.board_lineEdit = QtGui.QLineEdit(self.other_groupBox)
        self.board_lineEdit.setObjectName("board_lineEdit")
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.FieldRole, self.board_lineEdit)
        self.verticalLayout_2.addWidget(self.other_groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.jobProperties_scrollArea.setWidget(self.jobProperties_scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.jobProperties_scrollArea)
        self.jobSettings_buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.jobSettings_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset|QtGui.QDialogButtonBox.Save)
        self.jobSettings_buttonBox.setObjectName("jobSettings_buttonBox")
        self.verticalLayout.addWidget(self.jobSettings_buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Job Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.job_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Job settings", None, QtGui.QApplication.UnicodeUTF8))
        self.projNum_label.setText(QtGui.QApplication.translate("Dialog", "Project number:", None, QtGui.QApplication.UnicodeUTF8))
        self.jobNum_label.setText(QtGui.QApplication.translate("Dialog", "Job number:", None, QtGui.QApplication.UnicodeUTF8))
        self.brand_label.setText(QtGui.QApplication.translate("Dialog", "Brand:", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("Dialog", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.deliverable_label.setText(QtGui.QApplication.translate("Dialog", "Deliverable:", None, QtGui.QApplication.UnicodeUTF8))
        self.client_label.setText(QtGui.QApplication.translate("Dialog", "Client:", None, QtGui.QApplication.UnicodeUTF8))
        self.time_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.fps_label.setText(QtGui.QApplication.translate("Dialog", "Frames per second:", None, QtGui.QApplication.UnicodeUTF8))
        self.range_label.setText(QtGui.QApplication.translate("Dialog", "Frame range:", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeSep_label.setText(QtGui.QApplication.translate("Dialog", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.handles_label.setText(QtGui.QApplication.translate("Dialog", "Handles:", None, QtGui.QApplication.UnicodeUTF8))
        self.res_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_label.setText(QtGui.QApplication.translate("Dialog", "Preset:", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "HD 1080p", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "HD 720p", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "PAL 576p 16:9", None, QtGui.QApplication.UnicodeUTF8))
        self.resPreset_comboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "PAL 576p 4:3", None, QtGui.QApplication.UnicodeUTF8))
        self.res_label.setText(QtGui.QApplication.translate("Dialog", "Full size resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.resSep_label.setText(QtGui.QApplication.translate("Dialog", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyMode_label.setText(QtGui.QApplication.translate("Dialog", "Proxy mode:", None, QtGui.QApplication.UnicodeUTF8))
        self.scale_radioButton.setText(QtGui.QApplication.translate("Dialog", "Scale", None, QtGui.QApplication.UnicodeUTF8))
        self.res_radioButton.setText(QtGui.QApplication.translate("Dialog", "Resolution", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyScale_label.setText(QtGui.QApplication.translate("Dialog", "Proxy scale:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyRes_label.setText(QtGui.QApplication.translate("Dialog", "Proxy resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxyResSep_label.setText(QtGui.QApplication.translate("Dialog", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.preserveAR_checkBox.setText(QtGui.QApplication.translate("Dialog", "Preserve aspect ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.apps_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Preferred application versions", None, QtGui.QApplication.UnicodeUTF8))
        self.maya_label.setText(QtGui.QApplication.translate("Dialog", "Maya:", None, QtGui.QApplication.UnicodeUTF8))
        self.mudbox_label.setText(QtGui.QApplication.translate("Dialog", "Mudbox:", None, QtGui.QApplication.UnicodeUTF8))
        self.other_groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Other settings", None, QtGui.QApplication.UnicodeUTF8))
        self.board_label.setText(QtGui.QApplication.translate("Dialog", "Production board URL:", None, QtGui.QApplication.UnicodeUTF8))

