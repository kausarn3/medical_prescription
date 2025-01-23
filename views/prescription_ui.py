import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit, QPushButton, QFrame, QMessageBox, QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime

class CreatePrescriptionUI(QWidget):
    def __init__(self, serial_no=None):
        super().__init__()
        self.attached_images = []
        self.serial_no = serial_no  # Will be None for new prescriptions
        self._setup_database()
        self._setup_ui()

        if self.serial_no:
            self._load_data(self.serial_no)

    def _setup_database(self):
        self.conn = sqlite3.connect("db/prescriptions.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "prescriptions" (
            "serial_no"	INTEGER,
            "doctor_id"	INTEGER,
            "date"	DATE,
            "name"	TEXT,
            "age"	TEXT,
            "sex"	TEXT,
            "weight"	TEXT,
            "bp"	BLOB,
            "observations"	TEXT,
            "prescription"	TEXT,
            "phone_no"	NUMERIC,
            PRIMARY KEY("serial_no" AUTOINCREMENT)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_no INTEGER,
                image_path TEXT,
                FOREIGN KEY (serial_no) REFERENCES prescriptions (serial_no)
            )
        """)
        self.conn.commit()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self._create_header_section())
        main_layout.addLayout(self._create_patient_details_section())
        main_layout.addWidget(self._create_label("Observations:", bold=True))
        self.observations_text = QTextEdit()
        main_layout.addWidget(self.observations_text)

        main_layout.addWidget(self._create_label("Prescription:", bold=True))
        self.prescription_text = QTextEdit()
        main_layout.addWidget(self.prescription_text)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._save_to_database)
        main_layout.addWidget(self.save_button)

        footer_label = QLabel("Contact/Appointment: 7001849780\nEmail: raybakhatoon24@gmail.com")
        footer_label.setFont(QFont("Arial", 10))
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer_label)

    def _create_header_section(self):
        header_layout = QVBoxLayout()

        clinic_name = QLabel("Gulshan Holistic Homeopathic Clinic")
        clinic_name.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        clinic_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(clinic_name)

        doctor_details = QLabel("Dr. Rayba Khatoon\nB.H.M.S (WBUHS), MD (PGT)\nConsultant Homeopathic Physician")
        doctor_details.setFont(QFont("Arial", 12))
        doctor_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(doctor_details)

        header_frame = QFrame()
        header_frame.setLayout(header_layout)
        return header_frame

    def _create_patient_details_section(self):
        patient_layout = QGridLayout()

        self._add_grid_row(patient_layout, 0, [
            ("Serial No:", QLabel("123" if not self.serial_no else str(self.serial_no))),
            ("Doctor ID:", QLabel("101")),
        ])

        self._add_grid_row(patient_layout, 1, [
            ("Last Visit:", QLabel(datetime.today().strftime("%d-%m-%Y"))),
        ])

        self._add_grid_row(patient_layout, 2, [
            ("Name:", QLineEdit()),
            ("Age:", QLineEdit()),
            ("Sex:", self._create_combo_box(["Male", "Female", "Other"])),
            ("Weight:", QLineEdit()),
            ("BP:", QLineEdit()),
        ])

        self._add_grid_row(patient_layout, 3, [
            ("Phone Number:", QLineEdit()) ])

        self.serial_no_display = patient_layout.itemAtPosition(0, 1).widget()
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
            layout.addWidget(QLabel(label), row, col * 2)
            layout.addWidget(widget, row, col * 2 + 1)

    def _create_label(self, text, bold=False):
        label = QLabel(text)
        font = QFont("Arial", 12, QFont.Weight.Bold if bold else QFont.Weight.Normal)
        label.setFont(font)
        return label

    def _create_combo_box(self, items):
        combo_box = QComboBox()
        combo_box.addItems(items)
        return combo_box

    def _load_data(self, serial_no):
        self.cursor.execute("""
            SELECT * FROM prescriptions WHERE serial_no = ?
        """, (serial_no,))
        prescription_data = self.cursor.fetchone()
        print(prescription_data)

        if prescription_data:
            # Fill in the details from the prescription data
            self.date_input.setText(prescription_data[2])
            self.name_input.setText(prescription_data[3])
            self.age_input.setText(prescription_data[4])
            self.sex_input.setCurrentText(prescription_data[5])
            self.weight_input.setText(prescription_data[6])
            self.bp_input.setText(prescription_data[7])
            self.observations_text.setText(prescription_data[8])
            self.prescription_text.setText(prescription_data[9])

            # Load images
            # self.cursor.execute("""
            #     SELECT image_path FROM images WHERE serial_no = ?
            # """, (serial_no,))
            # image_paths = self.cursor.fetchall()
            # for image_path in image_paths:
            #     self.attached_images.append(image_path[0])

    def _save_to_database(self):
        doctor_id = 101  # Static Doctor ID
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
                self.cursor.execute("""
                    UPDATE prescriptions SET doctor_id = ?, date = ?, name = ?, age = ?, sex = ?, weight = ?, bp = ?, observations = ?, prescription = ?,
                    phone_no = ?  WHERE serial_no = ?
                """, (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no, self.serial_no))
                self.conn.commit()
            else:
                # Insert new prescription
                self.cursor.execute("""
                    INSERT INTO prescriptions (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (doctor_id, date, name, age, sex, weight, bp, observations, prescription, phone_no))
                self.conn.commit()
                self.serial_no = self.cursor.lastrowid

            # Save images
            for image_path in self.attached_images:
                self.cursor.execute("""
                    INSERT INTO images (serial_no, image_path)
                    VALUES (?, ?)
                """, (self.serial_no, image_path))
            self.conn.commit()

            QMessageBox.information(self, "Success", f"Prescription saved successfully! Serial No: {self.serial_no}")
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