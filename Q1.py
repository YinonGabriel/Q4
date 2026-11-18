import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QTableWidget, 
                               QTableWidgetItem, QLineEdit, QLabel, QMessageBox, 
                               QFileDialog)

class GradesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Grades Manager")
        self.resize(500, 600)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.load_btn = QPushButton("Load File")
        self.load_btn.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_btn)

        self.table = QTableWidget(50, 3)
        header_id = QTableWidgetItem("ID")
        header_original = QTableWidgetItem("Original Grades")
        header_corrected = QTableWidgetItem("Corrected Grades")

        self.table.setHorizontalHeaderItem(0, header_id)
        self.table.setHorizontalHeaderItem(1, header_original)
        self.table.setHorizontalHeaderItem(2, header_corrected)

        main_layout.addWidget(self.table)

        bonus_layout = QHBoxLayout()
        self.bonus_label = QLabel("Enter Bonus Points:")
        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText("Press ENTER to apply")
        self.bonus_input.returnPressed.connect(self.apply_bonus) 
        bonus_layout.addWidget(self.bonus_label)
        bonus_layout.addWidget(self.bonus_input)
        main_layout.addLayout(bonus_layout)

        self.update_btn = QPushButton("Update File")
        self.update_btn.clicked.connect(self.update_file)
        main_layout.addWidget(self.update_btn)

        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.load_stylesheet()

    def load_stylesheet(self):
        
        if os.path.exists("style.qss"):
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())

    def update_table_view(self):
        self.table.clearContents()
        for row in range(min(50, len(self.student_ids))):
            id_item = QTableWidgetItem(str(self.student_ids[row]))
            orig_item = QTableWidgetItem(str(self.original_grades[row]))
            corr_item = QTableWidgetItem(str(self.corrected_grades[row]))
            
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, orig_item)
            self.table.setItem(row, 2, corr_item)

    def load_file(self):
        
        result = QFileDialog.getOpenFileName(self, "Select Grades File", "", "Excel Files")
        file_name = result[0]
        
        if file_name:
            self.selected_file = file_name
            print(f"Selected: {self.selected_file}")
            
            self.student_ids.clear()
            self.original_grades.clear()
            self.corrected_grades.clear()
            
            with open(self.selected_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                
                for row in reader:
                    student_id = row[0]       
                    grade = int(row[1])      
                    self.student_ids.append(student_id)
                    self.original_grades.append(grade)
                    self.corrected_grades.append(grade)
            
            self.update_table_view()


    