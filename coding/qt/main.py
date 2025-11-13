"""
版本一
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Qt Demo")
button  = QPushButton("Click Me")
window.setCentralWidget(button)
window.show()
app.exec()
"""

"""
版本二，使用子类封装窗口
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Demo with Holder")
        button = QPushButton("Click Me")
        self.setCentralWidget(button)
app = QApplication(sys.argv)
window = ButtonHolder()
window.show()
app.exec()
"""

# 版本三 按类分拆版本二
from PySide6.QtWidgets import QApplication
from button_holder import ButtonHolder
import sys

app = QApplication(sys.argv)
window = ButtonHolder()
window.show()
app.exec()