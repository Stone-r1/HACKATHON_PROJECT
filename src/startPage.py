from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption

import sys
import random

from tools.BACKGROUND import BackgroundCanvas
from tools.StyleSheet import STYLE_SHEET
from tools.generateWordsGemini import WordExplorer

from resultPage import ResultWindow


class StartWindow(QWidget):
    def __init__(self, mainWindow=None):
        super().__init__()
        self.mainWindow = mainWindow
        self.explorer = WordExplorer(10)
        self.currentIndex = 0
        self.resultDict = []
        self.wordButtons = []
        self.correctCount = 0
        self.correctAnswer = None  # Store the correct answer to compare 
        self.phase = "question"  # To track the phase: "question" or "open"
        self.UI()


    def UI(self):
        self.setMinimumSize(500, 500)
        self.setWindowTitle("Word Explorer")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.layout = QVBoxLayout(self)

        self.generateButton = QPushButton("Start Quiz")
        self.generateButton.clicked.connect(self.startQuiz)
        self.layout.addWidget(self.generateButton)

        self.promptLabel = QTextEdit()
        self.promptLabel.setStyleSheet("font-size: 40px;")
        self.promptLabel.setReadOnly(True)
        self.promptLabel.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.promptLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.promptLabel)

        self.buttonsLayout = QVBoxLayout()
        self.topButtonLayout = QHBoxLayout()
        self.bottomButtonLayout = QHBoxLayout()

        self.buttonsLayout.addLayout(self.topButtonLayout)
        self.buttonsLayout.addLayout(self.bottomButtonLayout)
        self.layout.addLayout(self.buttonsLayout)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextQuestion)
        self.nextButton.setVisible(False)
        self.layout.addWidget(self.nextButton)

        self.setLayout(self.layout)


    def startQuiz(self):
        words = self.explorer.chooseRandomWords()
        prompt = self.explorer.buildPrompt(words)
        response = self.explorer.queryModel(prompt)
        self.resultDict = list(self.explorer.parseResponse(response).items())
        self.currentIndex = 0
        self.correctCount = 0
        self.generateButton.setVisible(False)
        self.showQuestion()


    def showQuestion(self):
        self.clearButtons()
        if self.currentIndex >= len(self.resultDict):
            self.showResultPage()
            self.nextButton.setVisible(False)
            return

        key, choices = self.resultDict[self.currentIndex]
        synonym = key[1]
        promptWord = key[0]

        self.promptLabel.setText(f"Find the synonym of {promptWord}")
        words = [synonym] + choices
        random.shuffle(words)

        self.correctAnswer = synonym
        self.phase = "question"

        for i, word in enumerate(words[:2]):
            btn = QPushButton(word)
            btn.setStyleSheet("padding: 8px;")
            btn.clicked.connect(lambda _, b=btn, w=word: self.printWord(b, w))
            self.topButtonLayout.addWidget(btn)
            self.wordButtons.append(btn)

        for i, word in enumerate(words[2:]):
            btn = QPushButton(word)
            btn.setStyleSheet("padding: 8px;")
            btn.clicked.connect(lambda _, b=btn, w=word: self.printWord(b, w))
            self.bottomButtonLayout.addWidget(btn)
            self.wordButtons.append(btn)

        self.nextButton.setVisible(True)


    def printWord(self, button, chosenWord):
        if self.phase == "question":
            if chosenWord == self.correctAnswer:
                button.setStyleSheet("padding: 8px; background-color: green;")
                self.correctCount += 1
            else:
                button.setStyleSheet("padding: 8px; background-color: red;")
                self.showCorrectAnswer()
            self.phase = "open"
            self.promptLabel.setText("Click again to save the word and definition")
        else:
            print(f"Button pressed: {chosenWord}")


    def showCorrectAnswer(self):
        for button in self.wordButtons:
            if button.text() == self.correctAnswer:
                button.setStyleSheet("padding: 8px; background-color: green;")
                break


    def nextQuestion(self):
        self.currentIndex += 1
        self.showQuestion()


    def clearButtons(self):
        while self.topButtonLayout.count():
            item = self.topButtonLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        while self.bottomButtonLayout.count():
            item = self.bottomButtonLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.wordButtons = []


    def showResultPage(self):
        self.resultWindow = ResultWindow(self.correctCount, len(self.resultDict), self.mainWindow)
        self.hide()
        self.resultWindow.show()


    def reset(self):
        self.correctCount = 0
        self.currentIndex = 0
        self.wordButtons = []
        self.correctAnswer = None
        self.phase = "question"
        self.promptLabel.setText("")
        self.clearButtons()
        self.generateButton.setVisible(True)
        self.nextButton.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())

