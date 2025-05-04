from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
import sys

from tools.BACKGROUND import BackgroundCanvas
from tools.StyleSheet import STYLE_SHEET

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()


    def UI(self):
        self.setMinimumSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        verticalLayout = QVBoxLayout()
        verticalLayout2 = QVBoxLayout()
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout2.setContentsMargins(0, 120, 0, 0)

        greeting = QLabel("<h1> Welcome! </h1>");
        greeting.setAlignment(Qt.AlignmentFlag.AlignRight)
        greeting.setStyleSheet("background: transparent;")
        greeting.setContentsMargins(0, 120, 0, 0)
        verticalLayout.addWidget(greeting)

        startButton = QPushButton("Start") 
        startButton.setObjectName("StartButton")
        #startButton.clicked.connect(self.openModeWindow) 

        contentButton = QPushButton("Words") 
        contentButton.setObjectName("AddButton")
        #contentButton.clicked.connect(self.openContentWindow)

        verticalLayout2.addWidget(startButton)
        verticalLayout2.setSpacing(10)
        verticalLayout2.addWidget(contentButton)
        verticalLayout2.setContentsMargins(220, 0, 10, 30)

        verticalLayout.addLayout(verticalLayout2)
        self.setLayout(verticalLayout)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main();
