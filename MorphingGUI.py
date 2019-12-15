# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(872, 625)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PBTstart = QtWidgets.QPushButton(self.centralwidget)
        self.PBTstart.setGeometry(QtCore.QRect(10, 10, 151, 27))
        self.PBTstart.setObjectName("PBTstart")
        self.PBTend = QtWidgets.QPushButton(self.centralwidget)
        self.PBTend.setGeometry(QtCore.QRect(440, 10, 151, 27))
        self.PBTend.setObjectName("PBTend")
        self.LBLstart = QtWidgets.QLabel(self.centralwidget)
        self.LBLstart.setGeometry(QtCore.QRect(100, 260, 111, 17))
        self.LBLstart.setObjectName("LBLstart")
        self.LBLend = QtWidgets.QLabel(self.centralwidget)
        self.LBLend.setGeometry(QtCore.QRect(540, 260, 101, 17))
        self.LBLend.setObjectName("LBLend")
        self.CKBtriangle = QtWidgets.QCheckBox(self.centralwidget)
        self.CKBtriangle.setGeometry(QtCore.QRect(310, 270, 121, 22))
        self.CKBtriangle.setObjectName("CKBtriangle")
        self.HSLalpha = QtWidgets.QSlider(self.centralwidget)
        self.HSLalpha.setGeometry(QtCore.QRect(70, 290, 591, 20))
        self.HSLalpha.setOrientation(QtCore.Qt.Horizontal)
        self.HSLalpha.setObjectName("HSLalpha")
        self.LBLalpha = QtWidgets.QLabel(self.centralwidget)
        self.LBLalpha.setGeometry(QtCore.QRect(20, 290, 41, 17))
        self.LBLalpha.setObjectName("LBLalpha")
        self.LBL0 = QtWidgets.QLabel(self.centralwidget)
        self.LBL0.setGeometry(QtCore.QRect(70, 310, 41, 17))
        self.LBL0.setObjectName("LBL0")
        self.LBL1 = QtWidgets.QLabel(self.centralwidget)
        self.LBL1.setGeometry(QtCore.QRect(650, 310, 41, 17))
        self.LBL1.setObjectName("LBL1")
        self.LBLresult = QtWidgets.QLabel(self.centralwidget)
        self.LBLresult.setGeometry(QtCore.QRect(320, 550, 121, 17))
        self.LBLresult.setObjectName("LBLresult")
        self.PBTblend = QtWidgets.QPushButton(self.centralwidget)
        self.PBTblend.setGeometry(QtCore.QRect(330, 570, 92, 27))
        self.PBTblend.setObjectName("PBTblend")
        self.LBLalphaShow = QtWidgets.QLabel(self.centralwidget)
        self.LBLalphaShow.setGeometry(QtCore.QRect(670, 290, 41, 17))
        self.LBLalphaShow.setStyleSheet("background-color:white")
        self.LBLalphaShow.setText("")
        self.LBLalphaShow.setObjectName("LBLalphaShow")
        self.GVstart = QtWidgets.QGraphicsView(self.centralwidget)
        self.GVstart.setGeometry(QtCore.QRect(10, 40, 288, 216))
        self.GVstart.setObjectName("GVstart")
        self.GVend = QtWidgets.QGraphicsView(self.centralwidget)
        self.GVend.setGeometry(QtCore.QRect(440, 40, 288, 216))
        self.GVend.setObjectName("GVend")
        self.GVresult = QtWidgets.QGraphicsView(self.centralwidget)
        self.GVresult.setGeometry(QtCore.QRect(230, 330, 288, 216))
        self.GVresult.setObjectName("GVresult")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PBTstart.setText(_translate("MainWindow", "Load Starting Image..."))
        self.PBTend.setText(_translate("MainWindow", "Load Ending Image..."))
        self.LBLstart.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Starting Image</span></p></body></html>"))
        self.LBLend.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Ending Image</span></p></body></html>"))
        self.CKBtriangle.setText(_translate("MainWindow", "Show Triangles"))
        self.LBLalpha.setText(_translate("MainWindow", "Alpha"))
        self.LBL0.setText(_translate("MainWindow", "0.0"))
        self.LBL1.setText(_translate("MainWindow", "1.0"))
        self.LBLresult.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Blending Result</span></p></body></html>"))
        self.PBTblend.setText(_translate("MainWindow", "Blend"))

