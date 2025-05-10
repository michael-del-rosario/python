import sys
import re
import mysql.connector
from bcrypt import hashpw, gensalt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="expense_tracker"
    )
    cursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Database connection failed: {e}")
    db = None

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Expense Tracker Registration")
        self.resize(500, 400)

        # **Background Image**
        palette = QPalette()
        bg_image = QPixmap("bg2.jpg")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # **Navbar**
        navbar_layout = QHBoxLayout()
        button_style = "padding: 8px; font-size: 16px; border-radius: 5px; background-color: white; color: black;"

        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(button_style)
        self.register_nav_button = QPushButton("Register")
        self.register_nav_button.setStyleSheet(button_style)
        self.login_nav_button = QPushButton("Login")
        self.login_nav_button.setStyleSheet(button_style)

        self.home_button.clicked.connect(lambda: self.switch_page("LandingPage"))
        self.register_nav_button.clicked.connect(lambda: self.switch_page("RegistrationWindow"))
        self.login_nav_button.clicked.connect(lambda: self.switch_page("LoginWindow"))

        navbar_layout.addWidget(self.home_button)
        navbar_layout.addWidget(self.register_nav_button)
        navbar_layout.addWidget(self.login_nav_button)
        main_layout.addLayout(navbar_layout)

        # **Content Container**
        content_container = QFrame()
        content_container.setStyleSheet(
            "border: 2px solid white; padding: 20px; border-radius: 10px; "
            "background-color: rgba(255, 255, 255, 0.95);"
        )
        content_layout = QVBoxLayout(content_container)

        # **Header**
        self.page_header = QLabel("Personal Expense Tracker Registration")
        self.page_header.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.page_header)

        # **System Description**
        self.system_description_label = QLabel(
            "Create an account to start tracking and managing your expenses.\n"
            "Securely store and analyze your financial data.\n"
            "Register now to take control of your finances!"
        )
        self.system_description_label.setStyleSheet("font-size: 14px; color: black; font-weight: bold")
        self.system_description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.system_description_label)

        # **Registration Form**
        input_style = "padding: 6px; font-size: 14px; border-radius: 5px; background-color: white; color: black; width: 250px;"

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet(input_style)
        content_layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setStyleSheet(input_style)
        content_layout.addWidget(self.email_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        content_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # **Register Button**
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet(
            "padding: 12px; font-size: 18px; font-weight: bold; border-radius: 5px; "
            "background-color: #007BFF; color: white; width: 200px;"
        )
        self.register_button.clicked.connect(self.validate_form)
        content_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()
        main_layout.addWidget(content_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

    def validate_form(self):
        """Ensures fields are filled before submission and validates email format."""
        if not db:
            QMessageBox.critical(self, "Database Error", "Database connection failed!")
            return

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(self, "Validation Error", "All fields must be filled!")
            return

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Validation Error", "Enter a valid email address!")
            return

        # **Hash password before storing**
        hashed_password = hashpw(password.encode(), gensalt()).decode()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            db.commit()
            QMessageBox.information(self, "Success", "Registration successful!")
            self.switch_page("LoginWindow")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")

    def switch_page(self, page_name):
        """Closes current window and opens a new one while maintaining window size."""
        current_size = self.size()
        self.close()

        if page_name == "LoginWindow":
            from login import LoginWindow
            new_page = LoginWindow()
        elif page_name == "LandingPage":
            from landing import LandingPage
            new_page = LandingPage()
        elif page_name == "RegistrationWindow":
            new_page = RegistrationWindow()

        new_page.resize(current_size)
        new_page.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec())