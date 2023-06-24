#need to fix: toggle/active key press system, be aware
#when the different streams are starting/stopping

import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QMutex
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCheckBox,
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
        self.activeFreqs = []
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
        self.naturalLabels = ["C", "D", "E", "F", "G", "A", "B"]
        self.naturalFreqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
        self.sharpLabels = ["C#", "D#", "F#", "G#", "A#"]
        self.sharpFreqs = [277.18, 311.13, 369.99, 415.30, 466.16]

        #generate key (buttons) and assign values
        keyboardLayout = QHBoxLayout()
        sharpCount = 0
        for i in range(7):

            #natural keys (white)
            whiteKey = QPushButton(self.naturalLabels[i])
            whiteKey.setProperty("freq", self.naturalFreqs[i])
            whiteKey.setStyleSheet("background-color: white")
            whiteKey.setFixedSize(100, 200)
            whiteKey.clicked.connect(self.keyToggle)
            #whiteKey.clicked.connect(self.keyPress)
            #whiteKey.clicked.connect(self.keyRelease)
            whiteKey.setCheckable(True)
            keyboardLayout.addWidget(whiteKey)      
            
            #sharp key (black)
            if (i != 2 and i != 6):
                blackKey = QPushButton(self.sharpLabels[sharpCount])
                blackKey.setProperty("freq", self.sharpFreqs[sharpCount])
                blackKey.setStyleSheet("background-color: grey")
                blackKey.setFixedSize(40, 190)
                blackKey.clicked.connect(self.keyToggle)
                #blackKey.clicked.connect(self.keyPress)
                #blackKey.clicked.connect(self.keyRelease)
                blackKey.setCheckable(True)
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

        #mode setup
        self.modeSelect = QPushButton("Enable Chords")
        self.modeSelect.setMaximumSize(dim, dim)
        self.modeSelect.clicked.connect(self.modeClick)
        self.modeSelect.setCheckable(True)

        #volume setup
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximumSize(dim, dim)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(50)
        self.volumeSlider.setValue(25)

        #sine wave button setup
        sineSelect = QPushButton()
        sineSelect.setFixedSize(dim, dim)
        sinePixmap = QPixmap("sine.jpg")
        sineSelect.setIcon(QIcon(sinePixmap))
        sineSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        sineSelect.clicked.connect(self.sineClick)

        #square wave button setup
        squareSelect = QPushButton()
        squareSelect.setFixedSize(dim, dim)
        squarePixmap = QPixmap("square.jpg")
        squareSelect.setIcon(QIcon(squarePixmap))
        squareSelect.setIconSize(QSize(dim-reduction, dim-reduction))
        squareSelect.clicked.connect(self.squareClick)

        #menu setup
        menuLayout = QHBoxLayout()
        menuLayout.addWidget(titleLabel)
        menuLayout.addWidget(self.volumeSlider)
        menuLayout.addWidget(self.modeSelect)
        menuLayout.addWidget(sineSelect)
        menuLayout.addWidget(squareSelect)
        menuLayout.setSpacing(5)
        return menuLayout
    
    #select sine waveform
    def sineClick(self):
        self.audioController.waveform = "sine"

    #select square waveform
    def squareClick(self):
        self.audioController.waveform = "square"

    #select operating mode
    def modeClick(self):
        pass
    
    #click key on keyboard
    def keyToggle(self):
        if (self.modeSelect.isChecked()):
            print("chord mode")
            btn = self.sender()
            if (btn.isChecked()):
                if (self.audioController.stream):
                    self.audioController.pauseStream()

                self.audioController.volume = self.volumeSlider.value()
                self.activeFreqs.append(btn.property("freq"))
                self.audioController.freqs = self.activeFreqs
                self.audioController.startStream()
            else:
                self.activeFreqs.remove(btn.property("freq"))
                self.audioController.pauseStream()
                self.audioController.startStream()

    '''
    def keyPress(self):
        if (not self.modeSelect.isChecked()):
            print("single mode")
            btn = self.sender()
            self.audioController.volume = self.volumeSlider.value()
            self.audioController.freqs = [btn.property("freq")]
            self.audioController.startStream()

    #release clicked key on keyboard
    def keyRelease(self):
        if (not self.modeSelect.isChecked()):
            self.audioController.pauseStream()
    '''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()