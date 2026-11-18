import sys
import os
import csv
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                               QPushButton, QMessageBox, QFileDialog)

class IceCreamApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ice Cream Profits")
        self.resize(800, 600)

        self.temperatures = []
        self.profits = []
        self.selected_file = ""

        main_layout = QVBoxLayout(self)

        self.load_btn = QPushButton("Load Ice Cream Data")
        self.load_btn.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_btn)

        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.load_stylesheet()

    def load_stylesheet(self):
        file = open("style.qss", "r")
        self.setStyleSheet(file.read())
        file.close()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamApp()
    window.show()
    sys.exit(app.exec())