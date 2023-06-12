import sys
import time
import threading
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
        self.audioController = AudioController()
        self.show()

    def buildKeyboard(self):
        keyboardLayout = QHBoxLayout()
        noteNames1 = ["C", "D", "E", "F", "G", "A", "B"]
        noteFreqs1 = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
        noteNames2 = ["C#", "D#", "F#", "G#", "A#"]
        noteFreqs2 = [277.18, 311.13, 369.99, 415.30, 466.16]
        count = 0
        for i in range(7):
            whiteKey = QPushButton(noteNames1[i])
            whiteKey.setFixedSize(100, 200)
            whiteKey.setProperty("freq", noteFreqs1[i])
            whiteKey.pressed.connect(self.keyPress)
            whiteKey.released.connect(self.keyRelease)
            keyboardLayout.addWidget(whiteKey)   
            if (i != 2 and i != 6):
                blackKey = QPushButton(noteNames2[count])
                blackKey.setProperty("freq", noteFreqs2[count])
                blackKey.setFixedSize(40, 190)
                blackKey.setStyleSheet('background-color: grey')
                blackKey.pressed.connect(self.keyPress)
                blackKey.released.connect(self.keyRelease)
                keyboardLayout.addWidget(blackKey)
                count += 1
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
    
    def keyPress(self):
        print("key pressed!")
        btn = self.sender()
        self.audioController.startStream(btn.property("freq"))

    def keyRelease(self):
        print("key released!")
        self.audioController.pauseStream()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()