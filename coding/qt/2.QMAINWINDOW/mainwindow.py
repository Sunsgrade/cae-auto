from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Main Window Example")
        # 菜单栏
        menu_bar = self.menuBar()
        # 苹果和win不一样，菜单栏默认在最上方显示，为了了演示效果，强制显示在窗口内
        menu_bar.setNativeMenuBar(False)  # 👈 强制菜单栏显示在窗口内
        file_menu = menu_bar.addMenu("TEST-MENU")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
    def quit_app(self):
        self.app.quit()