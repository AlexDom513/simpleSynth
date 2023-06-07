import sys
import time
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QSlider,
    QLabel,
)
from AudioController import AudioController

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("simpleSynth v1")
        self.setGeometry(0, 0, 720, 360)
        primaryLayout = QVBoxLayout()
        primaryLayout.addLayout(self.buildMenu())
        primaryLayout.addLayout(self.buildKeyboard())
        self.setLayout(primaryLayout)
        self.show()

    def buildKeyboard(self):
        keyboardLayout = QHBoxLayout()
        noteNames1 = ["C", "D", "E", "F", "G", "A", "B"]
        noteNames2 = ["C#", "D#", "F#", "G#", "A#"]
        count = 0
        for i in range(7):
            whiteKey = QPushButton(noteNames1[i])
            whiteKey.setFixedSize(100, 200)
            keyboardLayout.addWidget(whiteKey)   
            if (i != 2 and i != 6):
                blackKey = QPushButton(noteNames2[count])
                count += 1
                blackKey.setFixedSize(40, 190)
                blackKey.setStyleSheet('background-color: grey')
                keyboardLayout.addWidget(blackKey)
        return keyboardLayout
    
    def buildMenu(self):
        titleLabel = QLabel("simpleSynth")
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        titleLabel.setFont(font)
        dim = 100
        reduction = 10
        menuLayout = QHBoxLayout()
        volumeSlider = QSlider(Qt.Horizontal)
        volumeSlider.setMaximumSize(dim, dim)
        sineSelect = QPushButton()
        sineSelect.setFixedSize(dim, dim)
        sinePixmap = QPixmap("sine.jpg")
        sineSelect.setIcon(QIcon(sinePixmap))
        sineSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        squareSelect = QPushButton()
        squareSelect.setFixedSize(dim, dim)
        squarePixmap = QPixmap("square.jpg")
        squareSelect.setIcon(QIcon(squarePixmap))
        squareSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        menuLayout.addWidget(titleLabel)
        menuLayout.addWidget(volumeSlider)
        menuLayout.addWidget(sineSelect)
        menuLayout.addWidget(squareSelect)
        menuLayout.setSpacing(5)
        return menuLayout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
    test = AudioController()
    while test.stream.is_active():
        time.sleep(0.1)
    test.close()