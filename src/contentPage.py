from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QScrollArea, QLineEdit, QFrame, QCompleter, QMenu, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QKeyEvent, QAction

import json
import sys

from tools.BACKGROUND import BackgroundCanvas


class WordDefinitionWidget(QFrame):
    def __init__(self, word, definition, parent=None):
        super().__init__(parent)
        self.word = word
        self.definition = definition
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        blurOverlay = QWidget(self)
        blurOverlay.setGeometry(0, 0, 340, 165)
        blurOverlay.setStyleSheet("background-color: rgba(194, 237, 206, 0.5);")

        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(30)
        blurOverlay.setGraphicsEffect(blur_effect)

        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setFixedSize(320, 45)
        wordLabel.setStyleSheet("border: none; color: #253B56; font-size: 25px;")

        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setFixedSize(320, 120)
        definitionLabel.setStyleSheet("font-size: 18px; border: none; color: #253B56;")
        definitionLabel.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(wordLabel)
        layout.addWidget(definitionLabel)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 0, 0, 0)

        self.setLayout(layout)
        self.setFixedSize(340, 165)
        self.setStyleSheet("border-radius: 10px; border: 2px solid #253B56;")


class CustomLineEdit(QLineEdit):
    def __init__(self, checkValidity=None, parent=None):
        super().__init__(parent)
        self.checkValidity = checkValidity

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()
            if self.checkValidity is not None:
                self.checkValidity()
            return
        super().keyPressEvent(event)


class JsonFlatWindow(QWidget):
    def __init__(self, mainWindow=None):
        super().__init__()
        self.mainWindow = mainWindow
        self.wordData = {}
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("Word Definitions")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.loadJson()

        self.wordInput = CustomLineEdit(checkValidity=self.checkValidity, parent=self)
        self.wordInput.setPlaceholderText("Type a Word...")
        self.wordInput.setStyleSheet("font-size: 20px;")
        self.wordInput.setFixedSize(380, 50)
        self.wordInput.textChanged.connect(self.onWordInputChanged)

        self.wordCompleter = QCompleter(self)
        wordListModel = QStringListModel(list(self.wordData.keys()))
        self.wordCompleter.setModel(wordListModel)
        self.wordInput.setCompleter(self.wordCompleter)
        self.wordCompleter.activated.connect(self.onWordSelected)

        wordContainerWidget = QWidget()
        self.wordContainerLayout = QVBoxLayout()
        wordContainerWidget.setLayout(self.wordContainerLayout)

        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(wordContainerWidget)

        layout = QGridLayout()
        layout.addWidget(scrollArea, 0, 0, 4, 4)
        layout.addWidget(self.wordInput, 4, 0, 1, 4)

        self.setLayout(layout)
        self.refreshWordWidgets()


    def loadJson(self):
        with open("tools/wordDefinition.json", 'r', encoding="utf-8") as file:
            self.wordData = json.load(file)


    def refreshWordWidgets(self, filterText=""):
        for i in reversed(range(self.wordContainerLayout.count())):
            widget = self.wordContainerLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        filtered = {word: defn for word, defn in self.wordData.items() if filterText.lower() in word.lower()}

        for word, definition in filtered.items():
            self.wordContainerLayout.addWidget(WordDefinitionWidget(word, definition))


    def onWordSelected(self, word):
        self.wordInput.setText(word)
        self.refreshWordWidgets(word)


    def onWordInputChanged(self):
        self.refreshWordWidgets(self.wordInput.text())


    def checkValidity(self):
        self.refreshWordWidgets(self.wordInput.text())


    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JsonFlatWindow()
    window.show()
    sys.exit(app.exec())

