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
        self.chordMode = False
        self.keys = []

        #audio setup
        self.activeFreqs = []
        self.audioController = AudioController()
        self.audioController.startStream()
        self.audioController.pauseStream()

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
            whiteKey.pressed.connect(self.keyPress)
            whiteKey.released.connect(self.keyRelease)
            whiteKey.clicked.connect(self.keyToggle)
            keyboardLayout.addWidget(whiteKey)
            self.keys.append(whiteKey)
            
            #sharp key (black)
            if (i != 2 and i != 6):
                blackKey = QPushButton(self.sharpLabels[sharpCount])
                blackKey.setProperty("freq", self.sharpFreqs[sharpCount])
                blackKey.setStyleSheet("background-color: grey")
                blackKey.setFixedSize(40, 190)
                blackKey.pressed.connect(self.keyPress)
                blackKey.released.connect(self.keyRelease)
                blackKey.clicked.connect(self.keyToggle)
                self.keys.append(blackKey)
                keyboardLayout.addWidget(blackKey)
                self.keys.append(blackKey)
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
        self.chordMode = not self.chordMode
        if (self.chordMode):
            for key in self.keys:
                key.setCheckable(True)
        else:
            for key in self.keys:
                key.setCheckable(False)
                key.repaint()
            self.activeFreqs.clear()
            self.audioController.pauseStream()
    
    #click key on keyboard
    def keyToggle(self):
        if (self.chordMode):
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

    #hold key on keyboard
    def keyPress(self):
        if (not self.chordMode):
            btn = self.sender()
            self.audioController.volume = self.volumeSlider.value()
            self.audioController.freqs = [btn.property("freq")]
            self.audioController.startStream()

    #release key on keyboard
    def keyRelease(self):
        if (not self.chordMode):
            self.audioController.pauseStream()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()