import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About - Personal Expense Tracker")
        self.resize(500, 400)

        # **Set Background Image**
        palette = QPalette()
        bg_image = QPixmap("about.jpg") 
        palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # **Navbar**
        navbar_layout = QHBoxLayout()
        button_style = (
            "padding: 8px; font-size: 16px; border-radius: 5px; "
            "background-color: white; color: black;"
        )

        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet(button_style)
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet(button_style)
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(button_style)

        self.home_button.clicked.connect(lambda: self.switch_page("LandingPage"))
        self.register_button.clicked.connect(lambda: self.switch_page("RegistrationWindow"))
        self.login_button.clicked.connect(lambda: self.switch_page("LoginWindow"))

        navbar_layout.addWidget(self.home_button)
        navbar_layout.addWidget(self.register_button)
        navbar_layout.addWidget(self.login_button)
        main_layout.addLayout(navbar_layout)

        # **Content Box for "About Us" Section**
        content_container = QFrame()
        content_container.setStyleSheet(
            "border: 2px solid white; padding: 20px; border-radius: 10px; "
            "background-color: rgba(255, 255, 255, 0.95);"
        )
        content_layout = QVBoxLayout(content_container)

        # **Header**
        self.page_header = QLabel("About Personal Expense Tracker")
        self.page_header.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.page_header)

        # **Description Section**
        self.about_text = QTextEdit()
        self.about_text.setReadOnly(True)
        self.about_text.setStyleSheet(
            "font-size: 14px; color: black; font-weight: bold; border: none; "
            "background-color: transparent;"
        )
        self.about_text.setText(
            "The **Personal Expense Tracker** is designed to help users effectively manage their finances.\n\n"
            "With this system, you can:\n"
            "- Track daily, weekly, or monthly expenses\n"
            "- Categorize spending for better budgeting\n"
            "- Securely store financial records\n"
            "- Gain insights on saving strategies\n\n"
            "This intuitive tool empowers users to make informed financial decisions by analyzing their spending habits. "
            "Join now and take control of your expenses!"
        )
        content_layout.addWidget(self.about_text)

        main_layout.addStretch()
        main_layout.addWidget(content_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

    def switch_page(self, page_name):
        """Handles switching pages while maintaining window size."""
        current_size = self.size()
        self.close()

        new_page = None
        if page_name == "LoginWindow":
            from login import LoginWindow
            new_page = LoginWindow()
        elif page_name == "LandingPage":
            from landing import LandingPage
            new_page = LandingPage()
        elif page_name == "RegistrationWindow":
            from register import RegistrationWindow
            new_page = RegistrationWindow()
        elif page_name == "GuidePage":
            from guide import GuidePage  
            new_page = GuidePage()

        if new_page:
            new_page.resize(current_size)
            new_page.show()

if __name__ == "__main__":
    from register import RegistrationWindow
    from login import LoginWindow
    from landing import LandingPage
    from guide import GuidePage

    app = QApplication(sys.argv)
    window = AboutPage()
    window.show()
    sys.exit(app.exec())