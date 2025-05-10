import sys
from PyQt6.QtWidgets import QApplication
from landing import LandingPage

app = QApplication(sys.argv)
window = LandingPage()  # Start on Landing Page
window.show()
sys.exit(app.exec())