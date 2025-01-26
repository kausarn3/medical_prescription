import sys
import sqlite3
from PyQt6.QtWidgets import (
    QHBoxLayout, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit, QPushButton, QFrame, QMessageBox, QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime
from db.database_manager import DatabaseManager
from resources.styles import Main_window_Styles as Styles

class CreatePrescriptionUI(QWidget):
    def __init__(self, serial_no=None, doctor_info=None):
        super().__init__()
        self.attached_images = []
        self.db_manager = DatabaseManager("db/prescriptions.db")
        self.serial_no = serial_no  # Will be None for new prescriptions
        self.doctor_info = doctor_info
        self.prescription_data = self.db_manager.fetch_prescription(serial_no)
        self._setup_ui()
        if self.serial_no:
            self.setWindowTitle("Edit Prescription")
            self._load_data(self.serial_no)

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        #self.setStyleSheet(Styles.apply_gradient())
        self.setLayout(main_layout)

        main_layout.addWidget(self._create_header_section())
        main_layout.addLayout(self._create_patient_details_section())
        main_layout.addWidget(self._create_label("Observations:", bold=True, fontsize=14))
        self.observations_text = QTextEdit()
        self.observations_text.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(self.observations_text)

        main_layout.addWidget(self._create_label("Prescription:", bold=True, fontsize=14))
        self.prescription_text = QTextEdit()
        self.prescription_text.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(self.prescription_text)

        self.save_button = QPushButton("  Save  ")        
        #self.save_button.setFixedSize(100, 45)
        self.save_button.setStyleSheet(Styles.LOGIN_BUTTON)
        self.save_button.clicked.connect(self._save_to_database)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        footer_label = self._create_label(f"Contact/Appointment: {self.doctor_info[8]}\nEmail: {self.doctor_info[9]}", bold=True, fontsize=12)
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("font-style: italic;color: #eb300b;")
        main_layout.addWidget(footer_label)


    def _create_header_section(self):
        header_layout = QVBoxLayout()

        clinic_name = self._create_label(f"{self.doctor_info[3]}", bold=True, fontsize=14)
        clinic_name.setStyleSheet("color: #eb300b;")
        clinic_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(clinic_name)

        doctor_details = self._create_label(f"{self.doctor_info[4]}\n{self.doctor_info[5]}\n{self.doctor_info[6]}", bold=True, fontsize=14)
        doctor_details.setStyleSheet("font-style: italic;color: #eb300b;")
        doctor_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(doctor_details)

        header_frame = QFrame()
        header_frame.setLayout(header_layout)
        return header_frame
    
    def _create_line_edit(self):
        line_edit = QLineEdit()
        line_edit.setStyleSheet("font-weight: bold;")
        return line_edit

    def _create_patient_details_section(self):
        patient_layout = QGridLayout()

        if self.serial_no:
            serial_doctor_id = [("Serial No:", self._create_label(self.serial_no if not self.serial_no else str(self.serial_no), bold=True)),
            ("Doctor ID:", self._create_label(f"", bold=True)),]
        else:
            # From db calculate serial no
            serial_no = self.db_manager.get_serial_no()
            serial_doctor_id = [("Serial No:", self._create_label(str(serial_no + 1) if not self.serial_no else str(self.serial_no), bold=True)),
            ("Doctor ID:", self._create_label(f"{self.doctor_info[7]}", bold=True)),]

        self._add_grid_row(patient_layout, 0, serial_doctor_id)

        self._add_grid_row(patient_layout, 1, [
            ("Last Visit:", self._create_label(datetime.today().strftime("%d-%m-%Y"), bold=True)),
        ])

        self._add_grid_row(patient_layout, 2, [
            ("Name:", self._create_line_edit()),
            ("Age:", self._create_line_edit()),
            ("Sex:", self._create_combo_box(["Male", "Female", "Other"])),
            ("Weight:", self._create_line_edit()),
            ("BP:", self._create_line_edit()),
        ])

        self._add_grid_row(patient_layout, 3, [
            ("Phone Number:", self._create_line_edit()) ])

        self.serial_no_display = patient_layout.itemAtPosition(0, 1).widget()
        self.doctor_id = patient_layout.itemAtPosition(0, 3).widget()
        self.date_input = patient_layout.itemAtPosition(1, 1).widget()
        self.name_input = patient_layout.itemAtPosition(2, 1).widget()
        self.age_input = patient_layout.itemAtPosition(2, 3).widget()
        self.sex_input = patient_layout.itemAtPosition(2, 5).widget()
        self.weight_input = patient_layout.itemAtPosition(2, 7).widget()
        self.bp_input = patient_layout.itemAtPosition(2, 9).widget()
        self.phone_number = patient_layout.itemAtPosition(3, 1).widget()

        return patient_layout

    def _add_grid_row(self, layout, row, widgets):
        for col, (label, widget) in enumerate(widgets):
            layout.addWidget(self._create_label(label, bold=True), row, col * 2)
            layout.addWidget(widget, row, col * 2 + 1)

    def _create_label(self, text, bold=False, fontsize=11):
        label = QLabel(text)
        font = QFont("Arial", fontsize, QFont.Weight.Bold if bold else QFont.Weight.Normal)
        #label.setStyleSheet("color: #206de5;")
        label.setFont(font)
        return label

    def _create_combo_box(self, items):
        combo_box = QComboBox()
        combo_box.setStyleSheet("font-size: 12px;font-weight: bold;")        
        combo_box.addItems(items)
        return combo_box

    def _load_data(self, serial_no):
        
        if self.prescription_data:
            # Fill in the details from the prescription data
            self.doctor_id.setText(str(self.prescription_data[1]))
            self.date_input.setText(self.prescription_data[2])
            self.name_input.setText(self.prescription_data[3])
            self.age_input.setText(self.prescription_data[4])
            self.sex_input.setCurrentText(self.prescription_data[5])
            self.weight_input.setText(self.prescription_data[6])
            self.bp_input.setText(str(self.prescription_data[7]))
            self.observations_text.setText(self.prescription_data[8])
            self.prescription_text.setText(self.prescription_data[9])
            self.phone_number.setText(str(self.prescription_data[10]))
            # Load images
            # self.cursor.execute("""
            #     SELECT image_path FROM images WHERE serial_no = ?
            # """, (serial_no,))
            # image_paths = self.cursor.fetchall()
            # for image_path in image_paths:
            #     self.attached_images.append(image_path[0])

    def _save_to_database(self):
        doctor_id = self.doctor_info[7]  # Static Doctor ID
        date = datetime.today().strftime("%d-%m-%Y")
        name = self.name_input.text()
        age = self.age_input.text()
        sex = self.sex_input.currentText()
        weight = self.weight_input.text()
        bp = self.bp_input.text()
        observations = self.observations_text.toPlainText()
        prescription = self.prescription_text.toPlainText()
        phone_no = self.phone_number.text()

        if not name or not age or not weight or not bp:
            QMessageBox.warning(self, "Validation Error", "Please fill all mandatory fields.")
            return

        try:
            if self.serial_no:
                # Update existing prescription
                self.db_manager.update_prescription(self.serial_no, doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no)
            else:
                # Insert new prescription
                self.db_manager.insert_prescription(doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no)

            # Save images
            # for image_path in self.attached_images:
            #     self.cursor.execute("""
            #         INSERT INTO images (serial_no, image_path)
            #         VALUES (?, ?)
            #     """, (self.serial_no, image_path))
            # self.conn.commit()

            QMessageBox.information(self, "Success", f"Prescription saved successfully!")
            self._clear_form()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to save prescription: {e}")

    def _clear_form(self):
        self.name_input.clear()
        self.age_input.clear()
        self.weight_input.clear()
        self.bp_input.clear()
        self.observations_text.clear()
        self.prescription_text.clear()
        # self.attached_images.clear()
        # while self.image_preview_layout.count():
        #     widget = self.image_preview_layout.takeAt(0).widget()
        #     if widget:
        #         widget.deleteLater()