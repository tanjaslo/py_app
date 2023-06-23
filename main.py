import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor, QBrush, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # When you subclass a Qt class you must always call the super __init__ function to allow Qt to set up the object.

        # super(MainWindow, self).__init__()
        # This is the same as the previous line. It's just a different way to call the super function.

        self.setWindowTitle("Country Information")
        self.setGeometry(0, 0, 800, 600)  # Set an initial size

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

        self.country_label = QLabel("Enter a country name: ")
        self.country_label.setFont(QFont("Tahoma", 30))
        self.country_label.setStyleSheet("QLabel { padding: 0 10px 0 10px; }")

        # Set background color for country label
        label_palette = self.country_label.palette()
        label_palette.setColor(QPalette.ColorGroup.Normal,
                               QPalette.ColorRole.WindowText, QColor(Qt.GlobalColor.white))
        label_palette.setColor(QPalette.ColorGroup.Normal,
                               QPalette.ColorRole.Window, QColor(0, 0, 0, 100))
        self.country_label.setAutoFillBackground(True)
        self.country_label.setPalette(label_palette)

        self.line_edit = QLineEdit()

        line_edit_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: lightgrey;")

        line_edit_layout.addWidget(self.line_edit, 8)
        line_edit_layout.addWidget(self.search_button, 1)

        layout.addWidget(self.country_label)
        layout.addLayout(line_edit_layout)
        layout.addWidget(self.line_edit)


window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
# Your application won't reach here until you exit and the event
# loop has stopped.
