# 版本1
from PySide6.QtWidgets import QApplication, QPushButton

# The slot:responds when something happens
def button_clicked():
    print("Button was clicked!")
app = QApplication()
button = QPushButton("Click Me")
# 检查按钮是否被选中，进一步按钮可以作为开关使用，会改变颜色
button.setCheckable(True)
# 变量名button,clicked点击信号,connect函数(参数是槽函数)
button.clicked.connect(button_clicked)
button.show()
app.exec()

