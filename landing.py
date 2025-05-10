import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush

class LandingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Expense Tracker")
        self.resize(500, 400)

        # **Set Background Image**
        palette = QPalette()
        bg_image = QPixmap("bg.jpg") 
        palette.setBrush(QPalette.ColorRole.Window, QBrush(bg_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # **Navbar Positioned at the Top**
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

        # **Boxed Container for Header, Description & Buttons**
        content_container = QFrame()
        content_container.setStyleSheet(
            "border: 2px solid white; padding: 20px; border-radius: 10px; "
            "background-color: rgba(255, 255, 255, 0.95);"
        )
        content_layout = QVBoxLayout(content_container)

        # **Header Inside Boxed Section**
        self.page_header = QLabel("Personal Expense Tracker")
        self.page_header.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.page_header)

        # **System Description**
        self.system_description_label = QLabel(
            "Welcome to the Personal Expense Tracker!\n"
            "Our system allows you to efficiently track, manage,\n"
            "and analyze your expenses with ease.\n"
            "Sign up now to take control of your finances!"
        )
        self.system_description_label.setStyleSheet("font-size: 14px; color: black; font-weight: bold")
        self.system_description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.system_description_label)

        # **Get Started Button**
        self.get_started_button = QPushButton("Get Started")
        self.get_started_button.setStyleSheet(
            "padding: 12px; font-size: 18px; font-weight: bold; "
            "border-radius: 5px; background-color: #007BFF; color: white; width: 200px;"
        )
        self.get_started_button.clicked.connect(lambda: self.switch_page("RegistrationWindow"))
        content_layout.addWidget(self.get_started_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # **About Us Button**
        self.about_button = QPushButton("About Us")
        self.about_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                background-color: #007BFF;
                color: white;
                width: 180px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.about_button.clicked.connect(lambda: self.switch_page("AboutPage"))
        content_layout.addWidget(self.about_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # **Guide and Knowledge Button**
        self.guide_button = QPushButton("Guide and Knowledge")
        self.guide_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                background-color: #28A745;
                color: white;
                width: 180px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.guide_button.clicked.connect(lambda: self.switch_page("GuidePage"))
        content_layout.addWidget(self.guide_button, alignment=Qt.AlignmentFlag.AlignCenter)

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
            new_page = LandingPage()
        elif page_name == "RegistrationWindow":
            from register import RegistrationWindow
            new_page = RegistrationWindow()
        elif page_name == "AboutPage":
            from about import AboutPage  
            new_page = AboutPage()
        elif page_name == "GuidePage":
            from guide import GuidePage
            new_page = GuidePage()

        if new_page:
            new_page.resize(current_size)
            new_page.show()

if __name__ == "__main__":
    from register import RegistrationWindow
    from login import LoginWindow
    from about import AboutPage
    from guide import GuidePage

    app = QApplication(sys.argv)
    window = LandingPage()
    window.show()
    sys.exit(app.exec())