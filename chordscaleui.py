# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chord-scale.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1110, 534)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 15, 54, 12))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(40, 10, 69, 22))
        self.comboBox.setStyleSheet("QComboBox { \n"
"background-color: #AAA; \n"
"border: 1px solid #555; \n"
"color: black; \n"
"}")
        self.comboBox.setObjectName("comboBox")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 1091, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(83, 20, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 41, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab)
        self.pushButton_5.setGeometry(QtCore.QRect(83, 41, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab)
        self.pushButton_6.setGeometry(QtCore.QRect(83, 62, 75, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 62, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(83, 83, 75, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 83, 75, 23))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab)
        self.pushButton_10.setGeometry(QtCore.QRect(83, 104, 75, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab)
        self.pushButton_11.setGeometry(QtCore.QRect(10, 104, 75, 23))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab)
        self.pushButton_12.setGeometry(QtCore.QRect(83, 125, 75, 23))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab)
        self.pushButton_13.setGeometry(QtCore.QRect(10, 125, 75, 23))
        self.pushButton_13.setObjectName("pushButton_13")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(162, 10, 69, 22))
        self.comboBox_2.setStyleSheet("QComboBox { \n"
"background-color: #AAA; \n"
"border: 1px solid #555; \n"
"color: black; \n"
"}")
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(132, 15, 54, 12))
        self.label_2.setObjectName("label_2")
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(290, 10, 69, 22))
        self.comboBox_3.setStyleSheet("QComboBox { \n"
"background-color: #AAA; \n"
"border: 1px solid #555; \n"
"color: black; \n"
"}")
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(260, 15, 54, 12))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(510, 10, 75, 23))
        self.pushButton.setStyleSheet("QPushButton { \n"
"background-color: palegoldenrod; \n"
"border-width: 2px; \n"
"border-color: darkkhaki; \n"
"border-style: solid; \n"
"border-radius: 5; \n"
"padding: 3px; \n"
"min-width: 9ex; \n"
"min-height: 2.5ex; \n"
"}\n"
"\n"
"QPushButton:hover { \n"
"background-color: khaki; \n"
"}")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "根音"))
        self.pushButton_2.setText(_translate("Form", "-"))
        self.pushButton_3.setText(_translate("Form", "-"))
        self.pushButton_4.setText(_translate("Form", "-"))
        self.pushButton_5.setText(_translate("Form", "-"))
        self.pushButton_6.setText(_translate("Form", "-"))
        self.pushButton_7.setText(_translate("Form", "-"))
        self.pushButton_8.setText(_translate("Form", "-"))
        self.pushButton_9.setText(_translate("Form", "-"))
        self.pushButton_10.setText(_translate("Form", "-"))
        self.pushButton_11.setText(_translate("Form", "-"))
        self.pushButton_12.setText(_translate("Form", "-"))
        self.pushButton_13.setText(_translate("Form", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "吉他"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "钢琴"))
        self.label_2.setText(_translate("Form", "根音"))
        self.label_3.setText(_translate("Form", "根音"))
        self.pushButton.setText(_translate("Form", "PushButton"))

