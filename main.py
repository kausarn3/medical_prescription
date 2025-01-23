import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


def set_light_theme(app):
    # Create a light theme palette
    palette = QPalette()

    # Set background color
    palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)

    # Set text colors
    palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#F0F0F0"))
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Button, QColor("#E0E0E0"))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.PlaceholderText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Link, QColor("#777"))

    # Set disabled colors
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, Qt.GlobalColor.gray)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, Qt.GlobalColor.gray)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, Qt.GlobalColor.gray)

    # Apply the palette to the application
    app.setPalette(palette)

def main():
    app = QApplication(sys.argv)
    set_light_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
