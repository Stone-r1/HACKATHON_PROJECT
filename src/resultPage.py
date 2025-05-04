from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption

import sys
import random

from tools.BACKGROUND import BackgroundCanvas
from tools.StyleSheet import STYLE_SHEET


class ResultWindow(QWidget):
    def __init__(self, score, total, mainWindow):
        super().__init__()
 
        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.setWindowTitle("Quiz Results")
        self.setMinimumSize(400, 300)
        self.mainWindow = mainWindow

        layout = QVBoxLayout()

        resultLabel = QTextEdit()
        resultLabel.setReadOnly(True)
        resultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resultLabel.setText(f"You answered {score} out of {total} correctly!")
        resultLabel.setStyleSheet("font-size: 30px;")
        layout.addWidget(resultLabel)

        returnButton = QPushButton("Return to Main Page")
        returnButton.setStyleSheet("font-size: 20px; padding: 10px;")
        returnButton.clicked.connect(self.returnToMain)
        layout.addWidget(returnButton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def returnToMain(self):
        self.close()
        self.mainWindow.show()

