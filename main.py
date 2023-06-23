import sys
import requests
import urllib.parse
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor, QBrush, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from googlesearch import search

# Unsplash API access key
ACCESS_KEY = "5FjXzbxyfmQYy75LDh8kNHL9oW_pmam4MznoaIlgLZ8"
ALL_COUNTRIES_URL = "https://restcountries.com/v3.1/all"
NAME_URL = "https://restcountries.com/v3.1/name/"
label_style = "QLabel { background-color: rgba(0, 0, 0, 100); color: white; padding: 0 10px 0 10px; }"
ask_for_input = "Please enter a country name and press 'Search'/'Enter'"

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    # gradient = QLinearGradient(0, 0, 0, 800)
    # gradient.setColorAt(0, QColor(255, 255, 255))  # Start color
    # gradient.setColorAt(1, QColor(200, 200, 200))  # End color

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
        self.line_edit.returnPressed.connect(self.check_country)

        line_edit_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: lightgrey;")
        self.search_button.clicked.connect(self.check_country)

        line_edit_layout.addWidget(self.line_edit, 8)
        line_edit_layout.addWidget(self.search_button, 1)

        self.flag_label = QLabel(f"National flag: {ask_for_input}")
        self.flag_label.setFont(QFont("Tahoma", 14))
        # Center-align the flag image
        self.flag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.population_label = QLabel(f"Population: {ask_for_input}")
        self.population_label.setFont(QFont("Tahoma", 14))
        self.population_label.setStyleSheet(f"{label_style}")

        self.capital_label = QLabel(f"Capital: {ask_for_input}")
        self.capital_label.setFont(QFont("Tahoma", 14))
        self.capital_label.setStyleSheet(f"{label_style}")

        self.languages_label = QLabel(f"Languages: {ask_for_input}")
        self.languages_label.setFont(QFont("Tahoma", 14))
        self.languages_label.setStyleSheet(f"{label_style}")

        self.currency_label = QLabel(f"Currency: {ask_for_input}")
        self.currency_label.setFont(QFont("Tahoma", 14))
        self.currency_label.setStyleSheet(f"{label_style}")

        self.fun_fact_label = QLabel(f"Fun fact: {ask_for_input}")
        self.fun_fact_label.setFont(QFont("Tahoma", 14))
        self.fun_fact_label.setStyleSheet(f"{label_style}")
        # Enable opening links in a web browser
        self.fun_fact_label.setOpenExternalLinks(True)
        self.fun_fact_label.setWordWrap(True)

        layout.addWidget(self.country_label)
        layout.addLayout(line_edit_layout)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.flag_label)
        layout.addWidget(self.population_label)
        layout.addWidget(self.capital_label)
        layout.addWidget(self.languages_label)
        layout.addWidget(self.currency_label)
        layout.addWidget(self.fun_fact_label)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def retrieve_countries_data(self):
        response = requests.get(ALL_COUNTRIES_URL)
        if response.status_code == 200:
            countries_data = response.json()
            return countries_data
        else:
            self.show_error_message("Failed to retrieve country data.")

    def get_country_names(self, countries_data):
        # Extract the list of country names from the data
        # country_names = [country['name']['common'] for country in countries_data]
        country_names = []
        for country in countries_data:
            country_names.append(country['name']['common'])
        # Return the list
        return country_names

    def check_country(self):
        input_value = self.line_edit.text().title()
        countries_data = self.retrieve_countries_data()

        if countries_data:
            country_names = self.get_country_names(countries_data)
            if input_value in country_names:
                self.country_label.setText(f"Country: {input_value}")
                self.display_country_picture(input_value)
                self.display_country_info(input_value, countries_data)
                self.display_flag(input_value)
                self.display_fun_fact(input_value)
            else:
                self.show_error_message(
                    f"{input_value} is not found in the list of countries.")
                # If image not found, clear the country picture label
                self.clear_country_picture()
                self.clear_flag()
                self.clear_country_info()
                self.clear_fun_fact()
        else:
            self.show_error_message("Failed to retrieve country data.")

        self.line_edit.clear()

    def display_country_info(self, country_name, countries_data):
        for country in countries_data:
            if country['name']['common'] == country_name:
                population = country['population']
                capital = country['capital'][0]
                languages = ', '.join(country['languages'].values())
                currency = ', '.join(country['currencies'].keys())

                # Add comma to the population number
                self.population_label.setText(f"Population: {population:,}")
                self.capital_label.setText(f"Capital: {capital}")
                self.languages_label.setText(f"Languages: {languages}")
                self.currency_label.setText(f"Currency: {currency}")

    def display_flag(self, country_name):
        response = requests.get(NAME_URL + country_name).json()
        for country in response:
            if country['name']['common'] == country_name:
                flag_url = country['flags']['png']
                response = requests.get(flag_url)
                if response.ok:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    # Adjust the width of the flag image
                    self.flag_label.setPixmap(pixmap.scaledToWidth(300))
                    self.flag_label.setText("")
                else:
                    self.flag_label.setText("Failed to retrieve flag image.")

    def display_fun_fact(self, country_name):
        query = f"{country_name} fun fact"
        results = list(search(query, num_results=1))
        if results:
            fun_fact = f"Fun Facts about {country_name}: <a href='{results[0]}' style='color: white;'>{results[0]}</a>"
            self.fun_fact_label.setText(fun_fact)
        else:
            self.fun_fact_label.setText("No fun fact found.")

    def display_country_picture(self, country_name):
        # Search for country image on Unsplash
        encoded_country_name = urllib.parse.quote(country_name)
        url = f"https://api.unsplash.com/photos/random?query={encoded_country_name}&client_id={ACCESS_KEY}"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if 'urls' in data and 'regular' in data['urls']:
                image_url = data['urls']['regular']
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    with open('country_picture.jpg', 'wb') as file:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, file)

                    palette = self.palette()
                    background_image = QPixmap('country_picture.jpg')
                    palette.setBrush(
                        QPalette.ColorGroup.Normal, QPalette.ColorRole.Window, QBrush(background_image))
                    self.setPalette(palette)
                else:
                    print('Failed to retrieve country picture')
            else:
                print('No country picture found')
        else:
            print('Failed to retrieve country picture')

    def clear_country_picture(self):
        palette = self.palette()
        palette.setBrush(QPalette.ColorGroup.Normal,
                         QPalette.ColorRole.Window, QBrush(MainWindow.gradient))
        self.setPalette(palette)

    def clear_flag(self):
        self.flag_label.clear()

    def clear_country_info(self):
        self.population_label.clear()
        self.capital_label.clear()
        self.languages_label.clear()
        self.currency_label.clear()

    def clear_fun_fact(self):
        self.fun_fact_label.clear()

    def show_error_message(self, message):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Icon.Critical)
        error_message.setWindowTitle("Error")
        error_message.setText(message)
        error_message.exec()


window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
# Your application won't reach here until you exit and the event
# loop has stopped.
