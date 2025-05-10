import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush
import webbrowser

class GuidePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guide & Knowledge - Personal Expense Tracker")
        self.resize(500, 400)

        # **Set Background Image**
        palette = QPalette()
        bg_image = QPixmap("guide.jpg")
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

        # **Content Box for Financial Knowledge**
        content_container = QFrame()
        content_container.setStyleSheet(
            "border: 2px solid white; padding: 20px; border-radius: 10px; "
            "background-color: rgba(255, 255, 255, 0.95);"
        )
        content_layout = QVBoxLayout(content_container)

        # **Header**
        self.page_header = QLabel("Guide & Knowledge - Saving Money")
        self.page_header.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.page_header)

        # **Guide Text Section**
        self.guide_text = QTextEdit()
        self.guide_text.setReadOnly(True)
        self.guide_text.setStyleSheet(
            "font-size: 14px; color: black; font-weight: bold; border: none; "
            "background-color: transparent;"
        )
        self.guide_text.setText(
            "Want to save more money? Here are some essential tips:\n\n"
            "1️⃣ **Track Your Spending** – Analyze where your money goes each month.\n"
            "2️⃣ **Create a Budget** – Set realistic limits and stick to them.\n"
            "3️⃣ **Reduce Unnecessary Expenses** – Cut down on impulse purchases.\n"
            "4️⃣ **Automate Savings** – Set up an automatic transfer to your savings account.\n"
            "5️⃣ **Use Cash Instead of Card** – This psychologically helps control spending.\n"
            "6️⃣ **Take Advantage of Discounts & Coupons** – Find ways to save on necessities.\n"
            "7️⃣ **Invest Wisely** – Consider long-term savings through stocks or funds.\n"
            "8️⃣ **Set Financial Goals** – Work towards a major purchase or emergency fund.\n\n"
            "For more detailed guides, check out these expert resources below!"
        )
        content_layout.addWidget(self.guide_text)

        # **Helpful Financial Links**
        self.resources_label = QLabel("Helpful Money-Saving Resources:")
        self.resources_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        content_layout.addWidget(self.resources_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.create_link_button("Investopedia - Saving Basics", "https://www.investopedia.com/articles/personal-finance/041515/top-money-saving-tips.asp", content_layout)
        self.create_link_button("NerdWallet - Budgeting Tips", "https://www.nerdwallet.com/article/finance/how-to-save-money", content_layout)
        self.create_link_button("The Simple Dollar - Smart Savings", "https://www.thesimpledollar.com/save-money/", content_layout)

        main_layout.addStretch()
        main_layout.addWidget(content_container, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

    def create_link_button(self, text, url, layout):
        """Creates a clickable button that opens a financial website in a browser."""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                width: 250px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        button.clicked.connect(lambda: webbrowser.open(url))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

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
        elif page_name == "AboutPage":
            from about import AboutPage
            new_page = AboutPage()

        if new_page:
            new_page.resize(current_size)
            new_page.show()

if __name__ == "__main__":
    from register import RegistrationWindow
    from login import LoginWindow
    from landing import LandingPage
    from about import AboutPage

    app = QApplication(sys.argv)
    window = GuidePage()
    window.show()
    sys.exit(app.exec())