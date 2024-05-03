from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSizePolicy, QLineEdit, QMessageBox, QTextBrowser, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from bs4 import BeautifulSoup
import requests
import sqlite3
import os
import mimetypes

os.environ["QT_LOGGING_RULES"] = "*.warn=false"
from about import AboutDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Scraper Application")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 800, 600)  # Set window position and size
        self.setStyleSheet("background-color: #b9b0b0;")  # Set background color of main window


        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Title label and toggle button layout
        title_layout = QHBoxLayout()
        main_layout.addLayout(title_layout)

        # Title label
        self.title_label = QLabel("Web Scraper Application", self)
        gradient_color = "qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(90, 25, 155, 0.25), stop:1 rgba(0, 32, 240, 0.25));"  
        self.title_label.setStyleSheet("color: black; font-size: 24px; padding: 10px; background-color: " + gradient_color + " font-weight: bold; font-family: Arial, sans-serif;")
        title_layout.addWidget(self.title_label)

        # Button to toggle the task bar
        self.toggle_button = QPushButton("MENU")
        self.toggle_button.setIcon(QIcon("menu.png"))
        self.toggle_button.setStyleSheet("QPushButton {""background-color: #7289da; ""color: #fff; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {""background-color: #4e6eff; ""}")  
        self.toggle_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle_button.clicked.connect(self.toggle_task_bar)
        title_layout.addWidget(self.toggle_button)

        # Initialize task bar
        self.init_task_bar(main_layout)

        # Initialize home page components
        self.init_home_page(main_layout)

        # Initialize scrape page components
        self.init_scrape_page(main_layout)

        # Initialize view page components
        self.init_view_page(main_layout)

        # Initially hide task bar, scrape page, and view page components
        self.task_bar.hide()
        self.scrape_page.hide()
        self.view_page.hide()

    def init_task_bar(self, layout):
        # Sliding task bar
        self.task_bar = QWidget()
        self.task_bar.setStyleSheet("background-color: #23272a;")  # Set background color
        self.task_bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.task_bar_layout = QVBoxLayout(self.task_bar)

        # Additional buttons on the task bar
        button_names = [("HOME", "home.png"), ("SCRAPE", "scrape.png"), ("VIEW", "view.png"), ("ABOUT", "about.png"), ("QUIT","quit.png")]  # Add more button names as needed
        for name, icon_filename in button_names:
            button = QPushButton(name)
            button.setStyleSheet("QPushButton {"
                         "background-color: #7289da; "
                         "color: #fff; "
                         "font-weight: bold; "
                         "font-size: 18px; "
                         "text-align: left; "
                         "}"
                         "QPushButton:hover {"
                         "background-color: #4e6eff; "
                         "}")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if name == "QUIT":
                button.clicked.connect(self.quit_application)
            elif name == "ABOUT":
                button.clicked.connect(self.show_about_dialog)
            else:
                button.clicked.connect(lambda checked, name=name: self.change_page(name))

            # Set icon for the button
            icon = QIcon(icon_filename)
            button.setIcon(icon)
            self.task_bar_layout.addWidget(button)

        layout.addWidget(self.task_bar)

    def toggle_task_bar(self):
        if self.task_bar.isHidden():
            self.task_bar.show()
        else:
            self.task_bar.hide()

    def change_page(self, page_name):
        self.setWindowTitle(page_name)  # Change window title to reflect current page
        
        # Show or hide home, scrape, and view page components based on button click
        if page_name == "HOME":
            self.home_page.show()
            self.scrape_page.hide()
            self.view_page.hide()
        elif page_name == "SCRAPE":
            self.home_page.hide()
            self.scrape_page.show()
            self.view_page.hide()
        elif page_name == "VIEW":
            self.home_page.hide()
            self.scrape_page.hide()
            self.view_page.show()
        else:
            self.home_page.hide()
            self.scrape_page.hide()
            self.view_page.hide()

    def quit_application(self):
        QApplication.quit()

    def init_home_page(self, layout):
        # Initialize home page components
        self.home_page = QWidget()
        home_layout = QVBoxLayout(self.home_page)
        home_layout.setAlignment(Qt.AlignCenter)

        home_image_label = QLabel(self.home_page)
        pixmap = QPixmap("WS.png")  # Replace "your_image.png" with the filename of your PNG image
        home_image_label.setPixmap(pixmap)
        home_layout.addWidget(home_image_label , alignment=Qt.AlignCenter)

        home_text_label = QLabel("\n\t Introducing WebWeaver - your digital arachnid companion in the vast online jungle! \n\t\t      WebWeaver scours the web, capturing valuable data. \n So say goodbye to manual data collection and hello to WebWeaver, your trusty web-scraping sidekick!\n", self.home_page)
        home_text_label.setFont(QFont('New courier',10))
        home_text_label.setStyleSheet("color: black; font-size: 24px; font-weight: bold; background-color: #CBCBCB; border: 1px solid;")
        home_layout.addWidget(home_text_label)

        layout.addWidget(self.home_page)

    def init_scrape_page(self, layout):
        # Initialize scrape page components
        self.scrape_page = QWidget()
        scrape_layout = QVBoxLayout(self.scrape_page)
        scrape_layout.setAlignment(Qt.AlignCenter)

        self.url_line_edit = QLineEdit(self.scrape_page)
        self.url_line_edit.setPlaceholderText("Enter URL to scrape")
        self.url_line_edit.setStyleSheet("color: black; font-weight: bold; font-size: 18px;")
        scrape_layout.addWidget(self.url_line_edit)

        scrape_button = QPushButton("Scrape", self.scrape_page)
        scrape_button.setStyleSheet("QPushButton {""background-color: #7289da; ""color: white; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {""background-color: #4e6eff; ""}")
        scrape_button.clicked.connect(self.scrape_website)
        scrape_layout.addWidget(scrape_button)

        layout.addWidget(self.scrape_page)

    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec_()

    def scrape_website(self):
        url = self.url_line_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL.")
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Display HTML content in the view page
                html_content = str(soup)
                self.view_content_browser.setPlainText(html_content)
                # Switch to view page
                self.change_page("VIEW")
                # Save HTML content to text file
                self.save_html_content(html_content)
            else:
                QMessageBox.warning(self, "Error", "Failed to retrieve webpage. Please check the URL.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def save_html_content(self, content):
        try:
            with open("scraped_content.html", "w", encoding="utf-8") as file:
                file.write(content)
            QMessageBox.information(self, "Success", "HTML content saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save HTML content: {str(e)}")

    def init_view_page(self, layout):
        # Initialize view page components
        self.view_page = QWidget()
        view_layout = QVBoxLayout(self.view_page)
        view_layout.setAlignment(Qt.AlignCenter)

        view_label = QLabel("HTML CONTENT", self.view_page)
        view_label.setStyleSheet("color: black; font-size: 24px; font-weight: bold;")
        view_layout.addWidget(view_label)

        self.view_content_browser = QTextBrowser(self.view_page)
        self.view_content_browser.setStyleSheet("color: white; background-color: black;")
        view_layout.addWidget(self.view_content_browser)

        # Button to select previously scraped websites
        select_button = QPushButton("Select Previous Scrapes", self.view_page)
        select_button.setStyleSheet("QPushButton {""background-color: #7289da; ""color: white; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {""background-color: #4e6eff; ""}")
        select_button.clicked.connect(self.select_previous_scrapes)
        view_layout.addWidget(select_button)


        layout.addWidget(self.view_page)

    def select_previous_scrapes(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()
                self.view_content_browser.setPlainText(content)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
