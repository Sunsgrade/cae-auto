from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSlider

def respond_to_slider(data):
    print(f"Slider value changed to: {data}")

app = QApplication()
slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(100)
slider.setValue(50)

# valueChanged 值变化信号
slider.valueChanged.connect(respond_to_slider)
slider.show()
app.exec()