# main_window.py
import sqlite3
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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        self.username_input.setPlaceholderText("📨 Email")
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

        # Forgot password link
        forgot_password_label = QLabel("<a href='#'>No Account Create one</a>", self)
        forgot_password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_password_label.setStyleSheet(Styles.LINK_LABEL)
        forgot_password_label.setOpenExternalLinks(False)

        # Get License
        create_account_label = QLabel("<a href='#'>Activate your App →</a>", self)
        create_account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_account_label.setStyleSheet(Styles.LINK_LABEL)
        create_account_label.setOpenExternalLinks(False)
        create_account_label.linkActivated.connect(self.show_forgot_password_dialog)

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

        if self.authenticate_user(username, password):
            self.open_dashboard()
        else:
            self.show_message("Error", "Invalid username or password.")

    def authenticate_user(self, username, password):
        try:
            conn = sqlite3.connect("db/prescriptions.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error as e:
            self.show_message("Database Error", str(e))
            return False

    def show_message(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning if title == "Error" else QMessageBox.Icon.Information)
        msg.exec()

    def open_dashboard(self):
        self.dashboard = Dashboard( self.username_input.text())
        self.dashboard.show()
        self.close()

    def show_forgot_password_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Activate your App")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()
        info_label = QLabel("Enter Activation code :", dialog)
        info_label.setWordWrap(True)

        email_input = QLineEdit(dialog)
        email_input.setPlaceholderText("Activation code")

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, dialog)
        button_box.setStyleSheet(Styles.LOGIN_BUTTON)
        button_box.accepted.connect(lambda: self.handle_forgot_password(email_input.text(), dialog))
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(info_label)
        layout.addWidget(email_input)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec()
