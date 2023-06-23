import sys
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
    
        #general setup
        super().__init__()
        self.setWindowTitle("simpleSynth")
        self.setGeometry(0, 0, 720, 360)

        #audio setup
        self.audioController = AudioController()

        #layout setup
        primaryLayout = QVBoxLayout()
        primaryLayout.addLayout(self.buildMenu())
        primaryLayout.addLayout(self.buildKeyboard())
        self.setLayout(primaryLayout)
        self.show()

    #generate synth keyboard and attach freq value to every note
    def buildKeyboard(self):

        #set fixed keyboard values
        naturalLabels = ["C", "D", "E", "F", "G", "A", "B"]
        naturalFreqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
        sharpLabels = ["C#", "D#", "F#", "G#", "A#"]
        sharpFreqs = [277.18, 311.13, 369.99, 415.30, 466.16]

        #generate key (buttons) and assign values
        keyboardLayout = QHBoxLayout()
        sharpCount = 0
        for i in range(7):

            #natural keys (white)
            whiteKey = QPushButton(naturalLabels[i])
            whiteKey.setProperty("freq", naturalFreqs[i])
            whiteKey.setStyleSheet('background-color: white')
            whiteKey.setFixedSize(100, 200)
            whiteKey.pressed.connect(self.keyPress)
            whiteKey.released.connect(self.keyRelease)
            keyboardLayout.addWidget(whiteKey)   
            
            #sharp key (black)
            if (i != 2 and i != 6):
                blackKey = QPushButton(sharpLabels[sharpCount])
                blackKey.setProperty("freq", sharpFreqs[sharpCount])
                blackKey.setStyleSheet('background-color: grey')
                blackKey.setFixedSize(40, 190)
                blackKey.pressed.connect(self.keyPress)
                blackKey.released.connect(self.keyRelease)
                keyboardLayout.addWidget(blackKey)
                sharpCount += 1

        return keyboardLayout
    
    def buildMenu(self):

        #title setup
        titleLabel = QLabel("simpleSynth v1")
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        titleLabel.setFont(font)

        #const
        dim = 100
        reduction = 10

        #volume setup
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximumSize(dim, dim)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(50)

        #sine wave button setup
        sineSelect = QPushButton()
        sineSelect.setFixedSize(dim, dim)
        sinePixmap = QPixmap("sine.jpg")
        sineSelect.setIcon(QIcon(sinePixmap))
        sineSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        sineSelect.clicked.connect(self.sinePress)

        #square wave button setup
        squareSelect = QPushButton()
        squareSelect.setFixedSize(dim, dim)
        squarePixmap = QPixmap("square.jpg")
        squareSelect.setIcon(QIcon(squarePixmap))
        squareSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        squareSelect.clicked.connect(self.squarePress)

        #menu setup
        menuLayout = QHBoxLayout()
        menuLayout.addWidget(titleLabel)
        menuLayout.addWidget(self.volumeSlider)
        menuLayout.addWidget(sineSelect)
        menuLayout.addWidget(squareSelect)
        menuLayout.setSpacing(5)
        return menuLayout
    
    def sinePress(self):
        self.audioController.waveform = "sine"

    def squarePress(self):
        self.audioController.waveform = "square"
    
    def keyPress(self):
        btn = self.sender()
        self.audioController.volume = self.volumeSlider.value()
        self.audioController.startStream(btn.property("freq"))

    def keyRelease(self):
        self.audioController.pauseStream()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()