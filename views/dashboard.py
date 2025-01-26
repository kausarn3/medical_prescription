import sqlite3
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from resources.styles import Dashboard_styles as Styles
from views.prescription_ui import CreatePrescriptionUI
from db.database_manager import DatabaseManager

class Dashboard(QWidget):
    def __init__(self, doctor_info):
        super().__init__()
        self.setWindowTitle("Dashboard")
        #self.setFixedSize(800, 500)
        self.resize(500, 700)
        self.doctor_info = doctor_info
        self.username = self.doctor_info[4]
        self.db_manager = DatabaseManager("db/prescriptions.db")
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)

        # Sidebar and content area setup
        self.sidebar_widget = self.create_sidebar()
        self.content_area = QVBoxLayout()
        self.content_area.setContentsMargins(10, 10, 10, 10)

        # Add to main layout
        self.main_layout.addWidget(self.sidebar_widget, 1)
        self.main_layout.addLayout(self.content_area, 4)
        self.setLayout(self.main_layout)

        self.show_dashboard_ui()

    def create_sidebar(self):
        sidebar_widget = QWidget(self)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(20, 30, 30, 30)
        sidebar_layout.setSpacing(25)
        sidebar_widget.setStyleSheet(Styles.SIDEBAR_WIDGET_STYLE)

        buttons = ["Dashboard", "Create Prescription", "Search Record", "About"]
        for button_text in buttons:
            button = QPushButton(button_text, self)
            button.setStyleSheet(Styles.DASHBOARD_BUTTON_STYLE)
            button.clicked.connect(lambda _, text=button_text: self.handle_sidebar_click(text))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        return sidebar_widget

    def handle_sidebar_click(self, button_text):
        self.clear_dynamic_content(button_text)

        if button_text == "Dashboard":
            self.show_dashboard_ui()
        elif button_text == "Create Prescription":
            self.show_create_prescription_ui()
        elif button_text == "Search Record":
            self.show_search_ui()
        elif button_text == "About":
            self.show_about_ui()

    def show_create_prescription_ui(self):
        self.add_welcome_message()
        create_prescription_ui = CreatePrescriptionUI(None, self.doctor_info)
        self.content_area.addWidget(create_prescription_ui)

    def add_welcome_message(self):
        """Adds a persistent welcome message at the top of the content area."""
        welcome_label = QLabel(f"Welcome, {self.username}!", self)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        welcome_label.setStyleSheet(Styles.WELCOME_LABEL_STYLE)
        self.content_area.addWidget(welcome_label)

    def show_dashboard_ui(self):
        # Fetch insights from the prescription database
        self.add_welcome_message()
        insights = self.get_prescription_insights()

        insights_layout = QHBoxLayout()
        insights_layout.setSpacing(15)        

        # Add insights to the horizontal layout
        for i, insight in enumerate(insights):
            insight_label = QLabel(insight, self)
            insight_label.setStyleSheet(Styles.DASHBOARD_UI[i % len(Styles.DASHBOARD_UI)])
            insight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            insight_label.setWordWrap(True)
            insights_layout.addWidget(insight_label)

        # Create a widget to hold the insights layout
        insights_widget = QWidget()
        insights_widget.setLayout(insights_layout)
        insights_widget.setStyleSheet("background-color: #f9f9f9; padding: 10px; border-radius: 5px;")

        centered_layout = QVBoxLayout()
        centered_layout.addStretch()
        centered_layout.addWidget(insights_widget)
        centered_layout.addStretch()

        centered_widget = QWidget()
        centered_widget.setLayout(centered_layout)

        # Add the insights widget to the content area
        self.content_area.addWidget(centered_widget)

    def get_prescription_insights(self):
        # This is a placeholder function. Replace it with actual database queries.
        total_patient, prescriptions_today =self.db_manager.get_total_patients_and_prescriptions_today()
        return [
            f"Total Patients: {total_patient}",
            f"Prescriptions Issued Today: {prescriptions_today}",
        ]

    def show_search_ui(self):
        self.add_welcome_message()
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("🔎 Search Patient by Name or Phone")
        search_bar.setStyleSheet(Styles.SEARCH_BAR_STYLE)
        search_bar.textChanged.connect(self.search_patient)
        self.content_area.addWidget(search_bar)

        self.results_area = QScrollArea(self)
        self.results_area.setWidgetResizable(True)
        self.results_area.setStyleSheet("border: none;")
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.results_layout.setSpacing(0)  # Remove spacing
        self.results_widget.setLayout(self.results_layout)
        self.results_area.setWidget(self.results_widget)

        self.content_area.addWidget(self.results_area)

    def show_about_ui(self):
        self.add_welcome_message()
        about_label = QLabel(
            "About Us\n\n"
            "Designed and Developed by:\n"
            "Kaushar Nazir\n\n"
            "Contacts:\n"
            "Email: babayaaga03@gmail.com"
            ,
            self,
        )
        about_label.setStyleSheet("font-size: 24px; font-weight: bold;font-style: italic;")
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        centered_layout = QVBoxLayout()
        centered_layout.addStretch()
        centered_layout.addWidget(about_label)
        centered_layout.addStretch()

        # Create a widget to hold the centered layout
        centered_widget = QWidget()
        centered_widget.setLayout(centered_layout)

        # Add the centered widget to the content area
        self.content_area.addWidget(centered_widget)

    def clear_dynamic_content(self, button_text):
        """Clears only the dynamic content (below the welcome message)."""
        # while self.content_area.count() > 1:  # Keep the welcome message
        #     widget = self.content_area.takeAt(1).widget()
        #     if widget:
        #         widget.deleteLater()

        for i in reversed(range(self.content_area.count())):
            widget = self.content_area.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def search_patient(self, query):
        if not query.strip():
            self.clear_search_results()
            return

        results = self.db_manager.search_patients(query)
        self.display_search_results(results)

    def clear_search_results(self):
        if hasattr(self, "results_layout"):
            for i in reversed(range(self.results_layout.count())):
                widget = self.results_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

    def display_search_results(self, results):
        self.clear_search_results()

        if results:
            for patient_id, name, phone in results:
                result_label = QLabel(f"Name: {name}, Phone: {phone}", self)
                result_label.setStyleSheet(Styles.RESULT_LABEL_STYLE)
                result_label.mouseDoubleClickEvent = lambda event, pid=patient_id: self.open_patient_details(pid)
                result_label.setFixedSize(300, 50)
                self.results_layout.addWidget(result_label)
        else:
            no_results_label = QLabel("No results found.", self)
            no_results_label.setStyleSheet(Styles.NO_RESULTS_LABEL_STYLE)
            no_results_label.setFixedSize(300, 50)
            self.results_layout.addWidget(no_results_label)

    def open_patient_details(self, patient_id):
        self.dashboard = CreatePrescriptionUI(patient_id, self.doctor_info)
        self.dashboard.show()


# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)
#     window = Dashboard("Kausar")
#     window.show()
#     sys.exit(app.exec())
