import sys
from PyQt6.QtGui import QPalette, QColor, QLinearGradient, QBrush, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # When you subclass a Qt class you must always call the super __init__ function to allow Qt to set up the object.

        # super(MainWindow, self).__init__()
        # This is the same as the previous line. It's just a different way to call the super function.

        self.setWindowTitle("Country Information")
        self.setGeometry(0, 0, 800, 600)  # Set an initial size

        # # Set background gradient
        # gradient = QLinearGradient(0, 0, 0, self.height())
        # gradient.setColorAt(0, QColor(0, 128, 0))
        # gradient.setColorAt(1, QColor(200, 200, 200))
        # palette = self.palette()
        # palette.setBrush(QPalette.ColorGroup.Normal,
        #                  QPalette.ColorRole.Window, QBrush(gradient))
        # self.setPalette(palette)

        # Set background
        palette = self.palette()
        palette.setBrush(QPalette.ColorGroup.Normal,
                         QPalette.ColorRole.Window, QBrush(QColor(116, 194, 194)))
        self.setPalette(palette)

        # Retrieve screen dimensions
        screen_rect = QGuiApplication.primaryScreen().availableGeometry()
        window_rect = self.frameGeometry()
        center_point = screen_rect.center()
        window_rect.moveCenter(center_point)
        self.move(window_rect.topLeft())  # Move window to the center

        layout = QVBoxLayout()
        widget = QWidget()

        widget.setLayout(layout)
        self.setCentralWidget(widget)


window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
# Your application won't reach here until you exit and the event
# loop has stopped.
