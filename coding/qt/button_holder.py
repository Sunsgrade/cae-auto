from PySide6.QtWidgets import  QMainWindow, QPushButton

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Demo with Holder")
        button = QPushButton("Click Me")
        self.setCentralWidget(button)