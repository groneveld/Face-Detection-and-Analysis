import os
import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QStyleFactory, QFileDialog
from mtcnn import MTCNN
from mxnet.numpy import ndarray
from fixed_image import analyze_image
from view import interface
from webcam_video_stream import VideoStream


class STGWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.path = ''
        self.source_idx = 0
        self.ui.comboBox.currentIndexChanged.connect(self.source)
        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_3.clicked.connect(self.browse)
        self.source(self.source_idx)

    @pyqtSlot(ndarray)
    def set_image(self, image):
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                   QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.ui.image_label.setPixmap(QPixmap.fromImage(p))

    def source(self, value):
        self.source_idx = value
        if value == 0:
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)

    def start(self):
        detector = MTCNN()
        if self.source_idx == 0:
            image = analyze_image(self.path, detector)
            rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                       QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.ui.image_label.setPixmap(QPixmap.fromImage(p))
        else:

            self.stream = VideoStream(detector)
            self.stream.changePixmap.connect(self.set_image)
            self.stream.start()
            self.moveToThread(self.stream)

    def browse(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "(*.jpg)")[0]
        self.ui.lineEdit.setText(self.path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = STGWindow()
    window.show()
    sys.exit(app.exec_())
