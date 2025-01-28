# main_window.py
import sqlite3
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QHBoxLayout,
    QMessageBox,
)
from views.tilt_view import TiltView
from resources.styles import Main_window_Styles as Styles
from views.dashboard import Dashboard
from db.database_manager import DatabaseManager
from utils.crypt import get_windows_mac_address, decrypt_mac_address


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(os.path.join(os.getcwd(),"db//prescriptions.db"))
        print(os.path.join(os.getcwd(),"db/prescriptions.db"))
        self.db.create_tables()
        self.setWindowTitle("Medical Prescription")
        self.setFixedSize(800, 500)

        # Tilt view for the left pane
        self.tilt_view = TiltView()

        # Title label
        title_label = QLabel("Member Login", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(Styles.TITLE_LABEL)

        # Create the username (email) and password fields
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("📨 Username")
        self.username_input.setStyleSheet(Styles.INPUT_FIELD)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("🔑 Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(Styles.INPUT_FIELD)
        self.password_input.returnPressed.connect(self.handle_login)

        # Login button
        self.login_button = QPushButton("LOGIN", self)
        self.login_button.setStyleSheet(Styles.LOGIN_BUTTON)
        self.login_button.clicked.connect(self.handle_login)

        # Sign up link
        forgot_password_label = QLabel("<a href='#'>No Account Create one</a>", self)
        forgot_password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_password_label.setStyleSheet(Styles.LINK_LABEL)
        forgot_password_label.setOpenExternalLinks(False)
        forgot_password_label.linkActivated.connect(self.show_signup_dialog)

        # Get License
        create_account_label = QLabel("<a href='#'>Activate your App →</a>", self)
        create_account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_account_label.setStyleSheet(Styles.LINK_LABEL)
        create_account_label.setOpenExternalLinks(False)
        create_account_label.linkActivated.connect(self.show_activation_dialog)

        # Form layout for the fields
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 0, 20, 0)
        form_layout.addRow(self.username_input)
        form_layout.addRow(self.password_input)
        form_layout.addRow(self.login_button)

        # Wrap the form layout in a vertical layout with title and spacing
        form_widget_layout = QVBoxLayout()
        form_widget_layout.addWidget(title_label)
        form_widget_layout.addSpacing(20)  # Gap below the title
        form_widget_layout.addLayout(form_layout)
        form_widget_layout.addWidget(forgot_password_label)
        form_widget_layout.addSpacing(10)  # Gap before "Create your Account"
        form_widget_layout.addWidget(create_account_label)

        # Create a widget for the form and set its background
        form_widget = QWidget(self)
        form_widget.setLayout(form_widget_layout)
        form_widget.setStyleSheet(Styles.FORM_WIDGET)

        # Center the form widget vertically
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_widget)
        center_layout.addStretch()

        # Main layout: Tilt view on the left, centered form widget on the right
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.tilt_view, 2)  # Left pane with a stretch factor of 2
        main_layout.addLayout(center_layout, 1)  # Centered layout in the right pane with a stretch factor of 1
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            self.show_message("Error", "Please enter both username and password.")
            return
        res = self.authenticate_user(username, password)

        if res is None:
            self.show_message("Error", "Invalid username or password or user does not exist")
            return
        else:        
            if res[10] == get_windows_mac_address():
                self.show_message("Error", "App not activated. Please activate the app.")
                return 
            if username == res[1] and password == res[2]:
                self.open_dashboard(res)
            
    def authenticate_user(self, username, password):
        try:
            result = self.db.authenticate_user(username, password)
            return result
        except sqlite3.Error as e:
            self.show_message("Database Error", str(e))
            return False

    def show_message(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning if title == "Error" else QMessageBox.Icon.Information)
        msg.exec()

    def open_dashboard(self, res):
        self.dashboard = Dashboard(res, self)
        self.dashboard.show()
        self.close()

    def show_activation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Activate your App")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()
        username = QLineEdit(dialog)
        username.setPlaceholderText("Enter Username")
        username.setStyleSheet(Styles.INPUT_FIELD)

        activation_code = QLineEdit(dialog)
        activation_code.setPlaceholderText("Enter Activation code")
        activation_code.setStyleSheet(Styles.INPUT_FIELD)

        message = QLabel(f"Please Share Secret code: {get_windows_mac_address()} to the admin to activate the app.")
        message.setStyleSheet("font-size: 10px; font-weight: bold;Font-style: italic;")
        message.setWordWrap(True)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, dialog)
        button_box.setStyleSheet(Styles.LOGIN_BUTTON)
        button_box.accepted.connect(lambda: self.handle_activation_dialog(username.text(), activation_code.text(),dialog))
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(username)
        layout.addWidget(activation_code)
        layout.addWidget(message)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec()

    def show_signup_dialog(self):
        signup_dialog = QDialog(self)
        signup_dialog.setWindowTitle("Create Account")
        signup_dialog.setFixedSize(800, 600)

        layout = QVBoxLayout()
        #layout.setStyleSheet(Styles.FORM_WIDGET)
        title_label = QLabel("Create a New Account")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        form_layout = QFormLayout()
        
        username_input = QLineEdit()
        username_input.setPlaceholderText("Username")
        username_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_password_input = QLineEdit()
        confirm_password_input.setPlaceholderText("Confirm Password")
        confirm_password_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        clinic_name_input = QLineEdit()
        clinic_name_input.setPlaceholderText("Clinic Name")
        clinic_name_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        name_input = QLineEdit()
        name_input.setPlaceholderText("Name")
        name_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        qualifications_input = QLineEdit()
        qualifications_input.setPlaceholderText("Qualifications")
        qualifications_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        designation_input = QLineEdit()
        designation_input.setPlaceholderText("Designation")
        designation_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)  
        doctor_id_input = QLineEdit()
        doctor_id_input.setPlaceholderText("Doctor ID")
        doctor_id_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        phone_no_input = QLineEdit()
        phone_no_input.setPlaceholderText("Phone Number")
        phone_no_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setStyleSheet(Styles.CREATE_ACCOUNT_INPUT_FIELD)

        form_layout.addRow("Username:", username_input)
        form_layout.addRow("Password:", password_input)
        form_layout.addRow("Confirm Password:", confirm_password_input)
        form_layout.addRow("Clinic Name:", clinic_name_input)
        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Qualifications:", qualifications_input)
        form_layout.addRow("Designation:", designation_input)
        form_layout.addRow("Doctor ID:", doctor_id_input)
        form_layout.addRow("Phone Number:", phone_no_input)
        form_layout.addRow("Email:", email_input)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setStyleSheet("background-color: white; padding: 10px; border-radius: 15px;font-weight: bold;")


        signup_button = QPushButton("Sign Up")
        signup_button.setFixedSize(100, 45)
        signup_button.setStyleSheet(Styles.LOGIN_BUTTON)
        signup_button.clicked.connect(lambda: self.handle_signup(
            username_input, password_input, confirm_password_input, clinic_name_input, name_input, 
            qualifications_input, designation_input, doctor_id_input, phone_no_input, email_input, signup_dialog))

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(signup_button)
        button_layout.addStretch()

        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(form_widget)
        layout.addSpacing(20)
        layout.addLayout(button_layout)

        signup_dialog.setLayout(layout)
        signup_dialog.exec()

    def handle_signup(self, username_input, password_input, confirm_password_input, clinic_name_input, name_input, 
                      qualifications_input, designation_input, doctor_id_input, phone_no_input, email_input, dialog):
        username = username_input.text()
        password = password_input.text()
        confirm_password = confirm_password_input.text()
        clinic_name = clinic_name_input.text()
        name = name_input.text()
        qualifications = qualifications_input.text()
        designation = designation_input.text()
        doctor_id = doctor_id_input.text()
        phone_no = phone_no_input.text()
        email = email_input.text()
        mac_address = get_windows_mac_address()

        if not all([username, password, confirm_password, clinic_name, name, qualifications, designation, doctor_id, phone_no, email]):
            self.show_message("Error", "All fields are mandatory.")
            return

        if password != confirm_password:
            self.show_message("Error", "Passwords do not match.")
            return

        # Add logic to save the user data to the database here
        if self.db.insert_user(username, password, clinic_name, name, qualifications, designation, doctor_id, phone_no, email, mac_address):
            self.show_message("Success", "Account created successfully.")
        else:
            self.show_message("Error", "Failed to create account. Please try again.")
        dialog.accept()

    def handle_activation_dialog(self, username,activation_code, dialog):
        if not username or not activation_code:
            self.show_message("Error", "Username and Activation is required.")
            return
        # Add logic to activate the app here
        res = self.db.fetch_mac_address(username)
        if res is None:
            self.show_message("Error", "No user found with the given username.")
            return
        
        if res[0] != decrypt_mac_address(activation_code, b'NxhLBBnSCAsWT_I-fxUIJqfRGI4SoG-1bqpS4nhcPR0=').replace("b'", "").replace("'", ""):
            self.show_message("Error", "Invalid activation code.")
            return
        else:
            self.db.insert_mac_address(username, activation_code)
            self.show_message("Success", "App activated successfully.")
            dialog.accept()