import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QSlider,
    QLabel,
)

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
        menuLayout = QHBoxLayout()
        volumeSlider = QSlider(Qt.Horizontal)
        volumeSlider.setMaximumSize(dim, dim)
        sineSelect = QPushButton()
        sineSelect.setFixedSize(dim, dim)
        squareSelect = QPushButton()
        squareSelect.setFixedSize(dim, dim)
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