#######################################################
#    Author:      Shu Hwai Teoh
#    email:       teoh0@purdue.edu
#    ID:          ee364e13
#    Date:        Apr. 19, 2019
#######################################################
"""
Creating a PyQt Application:

1- Create a UI file using the QtDesigner.

2- Convert the UI file to a Python file using the conversion tool:
    /package/eda/anaconda3/bin/pyuic5 MorphingGUI.ui -o MorphingGUI.py
   The generated file must NOT be modified, as indicated in the header warning!

3- Use the given file <blank.py> to create a consumer Python file, and write the code that drives the UI.

"""

# Import PyQt5 classes
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QEvent
import re
import imageio
import numpy as np
from Morphing import loadTriangles, Morpher
from MorphingGUI import *


# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
# DataPath = os.path.expanduser("~ee364/DataFolder/Lab12")

class MorphingApp(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)

        self.HSLalpha.setRange(0, 20)
        self.HSLalpha.setSingleStep(1)
        self.LBLalphaShow.setText("   0.0")
        self.HSLalpha.setDisabled(True)
        self.LBLalphaShow.setDisabled(True)
        self.PBTblend.setDisabled(True)
        self.CKBtriangle.setDisabled(True)

        self._saveFileStart = ""
        self._saveFileEnd = ""
        self._flag = 0

        self._startPointFile = ""
        self._endPointFile = ""

        self._leftTri = []
        self._rightTri = []
        self._startPoint = []
        self._endPoint = []
        self._slineList = []
        self._elineList = []
        self._lIm = []
        self._rIm = []

        self.sImage = None
        self.eImage = None

        self._RPen = QPen(Qt.red, 5, Qt.SolidLine)
        self._RBrush = QBrush(Qt.red)
        self._GPen = QPen(Qt.green, 5, Qt.SolidLine)
        self._GBrush = QBrush(Qt.green)
        self._BPen = QPen(Qt.blue, 5, Qt.SolidLine)
        self._BBrush = QBrush(Qt.blue)
        self._YPen = QPen(Qt.yellow, 5, Qt.SolidLine)
        self._YBrush = QBrush(Qt.yellow)
        self.PBTstart.clicked.connect(self._loadStartImg)
        self.PBTend.clicked.connect(self._loadEndImg)
        self.HSLalpha.valueChanged.connect(self._showAlpha)
        self.CKBtriangle.stateChanged.connect(self._delaunay)
        self.PBTblend.clicked.connect(self._blend)

        self._sScene = scene(self)
        self._eScene = scene(self)
        self._sScene.installEventFilter(self)
        self._eScene.installEventFilter(self)
        self._rScene = QGraphicsScene(self)
        # self._data=None

    def _loadStartImg(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open png or jpg file ...', filter="(*.png *.jpg)")
        if not filePath:
            return

        self.sImage = QtGui.QPixmap(filePath)
        self._lIm = np.array(imageio.imread(filePath))

        if self.eImage != None:
            self._EinitialState()
            self._endPoint.clear()
            self._elineList.clear()
            self._eScene._savePoint.clear()
            self._eScene._item.clear()
            self._startPoint.clear()
            self._slineList.clear()
            self._sScene._savePoint.clear()
            self._sScene._item.clear()

        self._sScene.clear()
        self._sScene.addPixmap(self.sImage)
        self.GVstart.setScene(self._sScene)
        self.GVstart.fitInView(self._sScene.sceneRect())

        startFile = filePath + ".txt"
        self._saveFileStart = startFile
        if os.path.isfile(startFile):
            self._startPointFile = startFile
        else:
            self._startPointFile = ""
        if self._startPointFile != "" and self._endPointFile != "" and self.GVend and self.GVstart:
            self._loadPoints()

    def _loadEndImg(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open png or jpg file ...', filter="(*.png *.jpg)")
        if not filePath:
            return

        self.eImage = QtGui.QPixmap(filePath)
        self._rIm = np.array(imageio.imread(filePath))

        if self.sImage != None:
            self._SinitialState()
            self._endPoint.clear()
            self._elineList.clear()
            self._eScene._savePoint.clear()
            self._eScene._item.clear()
            self._startPoint.clear()
            self._slineList.clear()
            self._sScene._savePoint.clear()
            self._sScene._item.clear()

        self._eScene.clear()
        self._eScene.addPixmap(self.eImage)
        self.GVend.setScene(self._eScene)
        self.GVend.fitInView(self._eScene.sceneRect())

        endFile = filePath + ".txt"
        self._saveFileEnd = endFile
        if os.path.isfile(endFile):
            self._endPointFile = endFile
        else:
            self._endPointFile = ""
        if self._startPointFile != "" and self._endPointFile != "" and self.GVend and self.GVstart:
            self._loadPoints()

    def _SinitialState(self):
        if self._sScene._tPoint != []:
            self._sScene._tPoint.clear()
        if self._startPoint != []:
            for i in self._startPoint:
                self._sScene.removeItem(i)
            self._startPoint.clear()
        if self._slineList != []:
            for i in self._slineList:
                self._sScene.removeItem(i)
            self._slineList.clear()
        if self._sScene._savePoint != []:
            for i in self._sScene._savePoint:
                self._sScene.removeItem(i)
            self._sScene._savePoint.clear()
        if self._sScene._item != []:
            for i in self._sScene._savePoint:
                self._sScene.removeItem(i)
            self._sScene._item.claer()
        self.CKBtriangle.setChecked(False)
        self.HSLalpha.setDisabled(True)
        self.LBLalphaShow.setDisabled(True)
        self.PBTblend.setDisabled(True)
        self.CKBtriangle.setDisabled(True)
        self._rScene.clear()

    def _EinitialState(self):
        if self._eScene._tPoint != []:
            self._eScene._tPoint.clear()
        if self._endPoint != []:
            for i in self._endPoint:
                self._eScene.removeItem(i)
            self._endPoint.clear()
        if self._elineList != []:
            for i in self._elineList:
                self._eScene.removeItem(i)
            self._elineList.clear()
        if self._eScene._savePoint != []:
            for i in self._eScene._savePoint:
                self._eScene.removeItem(i)
            self._eScene._savePoint.clear()
        if self._eScene._item != []:
            for i in self._eScene._savePoint:
                self._eScene.removeItem(i)
            self._eScene._item.clear()
        # self.HSLalpha.setTickPosition()
        self.CKBtriangle.setChecked(False)
        # self.LBLalphaShow.setText("   0.0")
        self.HSLalpha.setDisabled(True)
        self.LBLalphaShow.setDisabled(True)
        self.PBTblend.setDisabled(True)
        self.CKBtriangle.setDisabled(True)
        self._rScene.clear()

    def _loadPoints(self):
        with open(self._startPointFile, "r") as f:
            leftSource = f.read().split()
        leftPoints = [[float(leftSource[i]), float(leftSource[i + 1])] for i in range(0, len(leftSource) - 1, 2)]
        with open(self._endPointFile, "r") as f:
            rightSource = f.read().split()
        rightPoints = [[float(rightSource[i]), float(rightSource[i + 1])] for i in range(0, len(rightSource) - 1, 2)]
        if len(leftPoints) < 3 and len(leftPoints) == len(rightPoints):
            for i in range(len(leftPoints)):
                self._startPoint.append(
                    self._sScene.addEllipse(leftPoints[i][0], leftPoints[i][1], 15, 15, self._RPen, self._RBrush))
                self._endPoint.append(
                    self._eScene.addEllipse(rightPoints[i][0], rightPoints[i][1], 15, 15, self._RPen, self._RBrush))
        if len(leftPoints) >= 3 and len(leftPoints) == len(rightPoints):
            self._startPoint = []
            self._endPoint = []
            self._leftTri, self._rightTri = loadTriangles(self._startPointFile, self._endPointFile)
            for i in range(len(self._leftTri)):
                self._startPoint.append(
                    self._sScene.addEllipse(self._leftTri[i]._0[0], self._leftTri[i]._0[1], 15, 15, self._RPen,
                                            self._RBrush))
                self._startPoint.append(
                    self._sScene.addEllipse(self._leftTri[i]._1[0], self._leftTri[i]._1[1], 15, 15, self._RPen,
                                            self._RBrush))
                self._startPoint.append(
                    self._sScene.addEllipse(self._leftTri[i]._2[0], self._leftTri[i]._2[1], 15, 15, self._RPen,
                                            self._RBrush))
                self._endPoint.append(
                    self._eScene.addEllipse(self._rightTri[i]._0[0], self._rightTri[i]._0[1], 15, 15, self._RPen,
                                            self._RBrush))
                self._endPoint.append(
                    self._eScene.addEllipse(self._rightTri[i]._1[0], self._rightTri[i]._1[1], 15, 15, self._RPen,
                                            self._RBrush))
                self._endPoint.append(
                    self._eScene.addEllipse(self._rightTri[i]._2[0], self._rightTri[i]._2[1], 15, 15, self._RPen,
                                            self._RBrush))
            self.loadedState()
        else:
            return

    def loadedState(self):
        self.HSLalpha.setDisabled(False)
        self.LBLalphaShow.setDisabled(False)
        self.PBTblend.setDisabled(False)
        self.CKBtriangle.setDisabled(False)

    def _showAlpha(self):
        self.LBLalphaShow.setText("   {0:.2f}".format(self.HSLalpha.value() / 100 * 5))

    def _delaunay(self):
        if self.CKBtriangle.isChecked():
            self._lineList = []
            self._elineList = []
            if self._startPointFile != "" and self._endPointFile != "" and len(self._sScene._savePoint) == 0:
                self._leftTri, self._rightTri = loadTriangles(self._startPointFile, self._endPointFile)
                for i in range(len(self._leftTri)):
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._0[0], self._leftTri[i]._0[1], self._leftTri[i]._1[0],
                                             self._leftTri[i]._1[1], self._RPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._1[0], self._leftTri[i]._1[1], self._leftTri[i]._2[0],
                                             self._leftTri[i]._2[1], self._RPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._2[0], self._leftTri[i]._2[1], self._leftTri[i]._0[0],
                                             self._leftTri[i]._0[1], self._RPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._0[0], self._rightTri[i]._0[1], self._rightTri[i]._1[0],
                                             self._rightTri[i]._1[1], self._RPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._1[0], self._rightTri[i]._1[1], self._rightTri[i]._2[0],
                                             self._rightTri[i]._2[1], self._RPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._2[0], self._rightTri[i]._2[1], self._rightTri[i]._0[0],
                                             self._rightTri[i]._0[1], self._RPen))
            elif self._startPointFile != "" and self._endPointFile != "" and len(self._sScene._savePoint) != 0:
                self._leftTri, self._rightTri = loadTriangles(self._startPointFile, self._endPointFile)
                for i in range(len(self._leftTri)):
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._0[0], self._leftTri[i]._0[1], self._leftTri[i]._1[0],
                                             self._leftTri[i]._1[1], self._YPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._1[0], self._leftTri[i]._1[1], self._leftTri[i]._2[0],
                                             self._leftTri[i]._2[1], self._YPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._2[0], self._leftTri[i]._2[1], self._leftTri[i]._0[0],
                                             self._leftTri[i]._0[1], self._YPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._0[0], self._rightTri[i]._0[1], self._rightTri[i]._1[0],
                                             self._rightTri[i]._1[1], self._YPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._1[0], self._rightTri[i]._1[1], self._rightTri[i]._2[0],
                                             self._rightTri[i]._2[1], self._YPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._2[0], self._rightTri[i]._2[1], self._rightTri[i]._0[0],
                                             self._rightTri[i]._0[1], self._YPen))
            else:
                self._leftTri, self._rightTri = loadTriangles(self._saveFileStart, self._saveFileEnd)
                for i in range(len(self._leftTri)):
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._0[0], self._leftTri[i]._0[1], self._leftTri[i]._1[0],
                                             self._leftTri[i]._1[1], self._BPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._1[0], self._leftTri[i]._1[1], self._leftTri[i]._2[0],
                                             self._leftTri[i]._2[1], self._BPen))
                    self._slineList.append(
                        self._sScene.addLine(self._leftTri[i]._2[0], self._leftTri[i]._2[1], self._leftTri[i]._0[0],
                                             self._leftTri[i]._0[1], self._BPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._0[0], self._rightTri[i]._0[1], self._rightTri[i]._1[0],
                                             self._rightTri[i]._1[1], self._BPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._1[0], self._rightTri[i]._1[1], self._rightTri[i]._2[0],
                                             self._rightTri[i]._2[1], self._BPen))
                    self._elineList.append(
                        self._eScene.addLine(self._rightTri[i]._2[0], self._rightTri[i]._2[1], self._rightTri[i]._0[0],
                                             self._rightTri[i]._0[1], self._BPen))
        else:
            for i in self._slineList:
                self._sScene.removeItem(i)
            for i in self._elineList:
                self._eScene.removeItem(i)

    def _blend(self):
        m = Morpher(self._lIm, self._leftTri, self._rIm, self._rightTri)
        self._data = m.getImageAtAlpha(float(self.LBLalphaShow.text()))
        image = QImage(self._data, self._data.shape[1], self._data.shape[0], QImage.Format_Grayscale8)
        self._rScene.addPixmap(QPixmap(image))
        self.GVresult.setScene(self._rScene)
        self.GVresult.fitInView(self._rScene.sceneRect())

    def eventFilter(self, source, event):
        if event.type() == QEvent.GraphicsSceneMousePress:
            self._flag = 1
            if source is self._sScene:
                if len(self._sScene._tPoint) == 1 and len(self._eScene._tPoint) == 1:
                    self._eScene.mousePressEvent(event)
                    self._sScene.mousePressEvent(event)
                    self._saveFile()
                    self._sScene.mousePressEvent(event)
                elif len(self._sScene._tPoint) == 0:
                    self._sScene.mousePressEvent(event)
                return True
            elif source is self._eScene:
                if len(self._sScene._tPoint) != 0 and len(self._eScene._tPoint) == 0:
                    self._eScene.mousePressEvent(event)
                return True
        elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Backspace:
            if len(self._eScene._tPoint) != 0:
                self._eScene.keyPressEvent(event)
            elif len(self._sScene._tPoint) != 0:
                self._sScene.keyPressEvent(event)
            return True
        self._flag = 0
        return super(MorphingApp, self).eventFilter(source, event)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if self._flag == 0 and len(self._sScene._tPoint) == 1 and len(self._eScene._tPoint) == 1 and a0.type() != 4:
            self._sScene.removeItem(self._sScene._item[-1])
            self._sScene._item.pop()
            self._sScene._savePoint.append(self._sScene._item.append(
                self._sScene.addEllipse(self._sScene._tPoint[0][0], self._sScene._tPoint[0][1], 15, 15, self._BPen,
                                        self._BBrush)))
            self._eScene.removeItem(self._eScene._item[-1])
            self._eScene._item.pop()
            self._eScene._savePoint.append(self._eScene._item.append(
                self._eScene.addEllipse(self._eScene._tPoint[0][0], self._eScene._tPoint[0][1], 15, 15, self._BPen,
                                        self._BBrush)))
            self._saveFile()
    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if len(self._eScene._tPoint) != 0 and a0.type()==6:
            if len(self._eScene._item) != 0:
                self._eScene.removeItem(self._eScene._item[-1])
                self._eScene._item.pop()
                self._eScene._tPoint.pop()
        elif len(self._sScene._tPoint) != 0 and a0.type()==6:
            if len(self._sScene._item) != 0:
                self._sScene.removeItem(self._sScene._item[-1])
                self._sScene._item.pop()
                self._sScene._tPoint.pop()

    def _saveFile(self):
        if os.path.isfile(self._endPointFile) and os.path.isfile(self._startPointFile):
            with open(self._startPointFile, 'a') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._sScene._tPoint[0][0], self._sScene._tPoint[0][1]))
            self._sScene._tPoint.pop()
            with open(self._endPointFile, 'a') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._eScene._tPoint[0][0], self._eScene._tPoint[0][1]))
            self._eScene._tPoint.pop()
        elif os.path.isfile(self._saveFileStart) and os.path.isfile(self._saveFileEnd):
            with open(self._saveFileStart, 'a') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._sScene._tPoint[0][0], self._sScene._tPoint[0][1]))
            self._sScene._tPoint.pop()
            with open(self._saveFileEnd, 'a') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._eScene._tPoint[0][0], self._eScene._tPoint[0][1]))
            self._eScene._tPoint.pop()
        else:
            match = re.search('([-\w]+\.(?:jpg|png))', self._saveFileStart)
            with open(match[0] + ".txt", 'w') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._sScene._tPoint[0][0], self._sScene._tPoint[0][1]))
            self._sScene._tPoint.pop()
            match = re.search('([-\w]+\.(?:jpg|png))', self._saveFileEnd)
            with open(match[0] + ".txt", 'w') as f:
                f.write("  {0:6.1f}  {1:6.1f}\n".format(self._eScene._tPoint[0][0], self._eScene._tPoint[0][1]))
            self._eScene._tPoint.pop()
        if len(self._sScene._savePoint) >= 3 and len(self._sScene._savePoint) == len(self._eScene._savePoint):
            self.loadedState()


class scene(QGraphicsScene):
    def __init__(self, main, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.original = self

        self._GPen = QPen(Qt.green, 4, Qt.SolidLine)
        self._GBrush = QBrush(Qt.green)
        self._BPen = QPen(Qt.blue, 4, Qt.SolidLine)
        self._BBrush = QBrush(Qt.blue)
        self._item = []
        self._tPoint = []
        self._savePoint = []

    def mousePressEvent(self, event):
        if len(self._tPoint) == 0:
            self._item.append(
                self.addEllipse(event.scenePos().x(), event.scenePos().y(), 15, 15, self._GPen, self._GBrush))
            self._tPoint.append([event.scenePos().x(), event.scenePos().y()])
        elif len(self._tPoint) == 1:
            self.removeItem(self._item[-1])
            self._item.pop()
            self._savePoint.append(
                self.addEllipse(self._tPoint[0][0], self._tPoint[0][1], 15, 15, self._BPen, self._BBrush))

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if len(self._item) != 0:
            self.removeItem(self._item[-1])
            self._item.pop()
            self._tPoint.pop()


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()


