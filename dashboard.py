import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox,
    QComboBox, QLineEdit, QGroupBox, QHeaderView, QInputDialog
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QPixmap

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Management Dashboard")
        self.resize(900, 650)
        self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #30475E, stop:1 #222831);")

        
        self.page_header = QLabel("Expense Dashboard")
        self.page_header.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 12px;")
        self.page_header.setAlignment(Qt.AlignmentFlag.AlignLeft)

        
        self.logout_button = QPushButton("Log Out")
        self.logout_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                background-color: #dc3545;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.logout_button.clicked.connect(self.logout)

    
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.page_header)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_button)

        
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(3)
        self.expense_table.setHorizontalHeaderLabels(["Expense Type", "Amount (₱)", "Actions"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.expense_table.verticalHeader().setVisible(False)


        self.form_box = QGroupBox("Add New Expense")
        self.form_box.setStyleSheet("border: 2px solid white; padding: 20px; background-color: rgba(0, 0, 0, 0.6); color: white;")
        form_layout = QVBoxLayout()


        dropdown_layout = QHBoxLayout()
        self.expense_type_label = QLabel("Expense Type")
        self.expense_type_label.setStyleSheet("font-size: 18px; color: white;")
        dropdown_layout.addWidget(self.expense_type_label)

        self.expense_type_dropdown = QComboBox()
        self.expense_type_dropdown.addItems(["Food", "Transportation", "Bills", "Entertainment", "Shopping", "Health", "Others", "Custom"])
        self.expense_type_dropdown.currentIndexChanged.connect(self.handle_custom_expense)
        dropdown_layout.addWidget(self.expense_type_dropdown)
        form_layout.addLayout(dropdown_layout)


        self.custom_expense_input = QLineEdit()
        self.custom_expense_input.setPlaceholderText("Enter custom expense type")
        self.custom_expense_input.setVisible(False)
        form_layout.addWidget(self.custom_expense_input)


        self.amount_label = QLabel("Amount (₱)")
        self.amount_label.setStyleSheet("font-size: 18px; color: white;")
        form_layout.addWidget(self.amount_label)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount spent")
        form_layout.addWidget(self.amount_input)

        
        self.add_button = QPushButton("Add Expense")
        self.add_button.setStyleSheet("""
            QPushButton {
                padding: 14px;
                font-size: 20px;
                font-weight: bold;
                border-radius: 6px;
                background-color: #007BFF;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.add_button.clicked.connect(self.add_expense)
        form_layout.addWidget(self.add_button)

        self.form_box.setLayout(form_layout)

        
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.expense_table)
        main_layout.addWidget(self.form_box)
        self.setLayout(main_layout)

        self.load_user_expenses()

    def handle_custom_expense(self):
        """Shows input field when 'Custom' is selected."""
        self.custom_expense_input.setVisible(self.expense_type_dropdown.currentText() == "Custom")

    def load_user_expenses(self):
        """Loads expenses of the logged-in user into the table."""
        settings = QSettings("MyApp", "ExpenseTracker")
        user_id = settings.value("user_id")

        if not user_id:
            QMessageBox.warning(self, "Session Error", "User session not found. Please log in again.")
            return

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
            cursor = db.cursor()
            cursor.execute("SELECT expense_type, amount FROM expenses WHERE user_id = %s", (user_id,))
            expenses = cursor.fetchall()
            db.close()

            self.expense_table.setRowCount(0)
            for expense_type, amount in expenses:
                row_position = self.expense_table.rowCount()
                self.expense_table.insertRow(row_position)
                self.expense_table.setItem(row_position, 0, QTableWidgetItem(expense_type))
                self.expense_table.setItem(row_position, 1, QTableWidgetItem(f"₱{amount:.2f}"))
                self.add_buttons_to_row(row_position)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")

    def add_buttons_to_row(self, row_position):
        """Adds edit and delete buttons dynamically."""
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda _, r=row_position: self.edit_expense(r))
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, r=row_position: self.confirm_delete(r))

        action_widget = QWidget()
        layout = QHBoxLayout(action_widget)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.expense_table.setCellWidget(row_position, 2, action_widget)

    def add_expense(self):
        """Adds a new expense to the table and inserts it into the database."""
        expense_type = self.expense_type_dropdown.currentText()
        if expense_type == "Custom":
            expense_type = self.custom_expense_input.text().strip()

        amount_text = self.amount_input.text().strip()
        if not expense_type or not amount_text:
            QMessageBox.warning(self, "Input Error", "Please enter both expense type and amount.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for amount.")
            return

        settings = QSettings("MyApp", "ExpenseTracker")
        user_id = settings.value("user_id")

        if not user_id:
            QMessageBox.warning(self, "Session Error", "User session not found. Please log in again.")
            return

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
            cursor = db.cursor()
            cursor.execute("INSERT INTO expenses (user_id, expense_type, amount) VALUES (%s, %s, %s)", 
                        (user_id, expense_type, amount))
            db.commit()
            db.close()

            self.load_user_expenses()
            self.expense_type_dropdown.setCurrentIndex(0)
            self.custom_expense_input.clear()
            self.amount_input.clear()

            QMessageBox.information(self, "Success", "Expense added successfully!")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")

    def edit_expense(self, row_position):
        """Allows the user to edit an expense entry."""
        expense_type = self.expense_table.item(row_position, 0).text()
        amount_text = self.expense_table.item(row_position, 1).text().replace("₱", "")

        new_expense_type, ok_type = QInputDialog.getText(self, "Edit Expense", "Enter new expense type:", text=expense_type)
        if not ok_type or not new_expense_type.strip():
            return

        new_amount_text, ok_amount = QInputDialog.getText(self, "Edit Expense", "Enter new amount:", text=amount_text)
        if not ok_amount or not new_amount_text.strip():
            return

        try:
            new_amount = float(new_amount_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for amount.")
            return

        settings = QSettings("MyApp", "ExpenseTracker")
        user_id = settings.value("user_id")

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
            cursor = db.cursor()
            cursor.execute("""
                UPDATE expenses SET expense_type = %s, amount = %s 
                WHERE user_id = %s AND expense_type = %s AND amount = %s
            """, (new_expense_type, new_amount, user_id, expense_type, float(amount_text)))
            db.commit()
            db.close()
            self.load_user_expenses()

            QMessageBox.information(self, "Success", "Expense updated successfully!")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")

    def confirm_delete(self, row_position):
        """Confirms and deletes an expense from both the UI and database."""
        expense_type = self.expense_table.item(row_position, 0).text()
        amount_text = self.expense_table.item(row_position, 1).text().replace("₱", "")

        confirmation = QMessageBox.question(self, "Delete Expense", f"Are you sure you want to delete '{expense_type}'?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        settings = QSettings("MyApp", "ExpenseTracker")
        user_id = settings.value("user_id")

        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
            cursor = db.cursor()
            cursor.execute("DELETE FROM expenses WHERE user_id = %s AND expense_type = %s AND amount = %s",
                        (user_id, expense_type, float(amount_text)))
            db.commit()
            db.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
            return

        self.expense_table.removeRow(row_position)

    def logout(self):
        """Logs the user out by clearing session data and closing the dashboard."""
        settings = QSettings("MyApp", "ExpenseTracker")
        settings.remove("user_id")

        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
