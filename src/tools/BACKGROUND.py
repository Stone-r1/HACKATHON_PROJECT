from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsBlurEffect, QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QPixmap
import sys


class BackgroundCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()


    def UI(self):
        self.setFixedSize(1920, 1080)
        self.setWindowTitle("CANVAS")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setPen(Qt.GlobalColor.transparent)

        # background
        gradient = QLinearGradient(QPointF(self.width(), 0), QPointF(0, self.height())) 
        gradient.setColorAt(1, QColor("#90C67C"))
        gradient.setColorAt(0, QColor("#328E6E"))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.drawRect(0, 0, self.width(), self.height())

        # background decorations
        painter.setBrush(QColor("#3F7D58"))
        painter.rotate(45)
        painter.drawRect(30, 30, int(self.width() / 2), int(self.height() / 2))

        painter.setBrush(QColor("#336949"))
        painter.drawRect(90, 90, int(self.width() / 2) - 10, int(self.height() / 2) - 10)

        painter.setBrush(QColor("#26593b"))
        painter.drawRect(150, 150, int(self.width() / 2) - 20, int(self.height() / 2) - 20)

        painter.setBrush(QColor("#3F7D58"))
        painter.rotate(-33)
        painter.drawRect(0, -self.height(), self.width(), self.height())
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = BackgroundCanvas()
    canvas.show()
    sys.exit(app.exec())
