import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
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
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        self.load_btn = QPushButton("Load Ice Cream Data")
        self.load_btn.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_btn)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.figure.patch.set_facecolor("#f8fafc")
        self.ax.set_facecolor("#ffffff")
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.load_stylesheet()

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")

        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())

    def load_file(self):
        result = QFileDialog.getOpenFileName(self, "Select Ice Cream File", "", "Excel Files (*)")
        file_name = result[0]
    
        if file_name:
            self.selected_file = file_name
            print(f"Selected: {self.selected_file}")
            self.temperatures.clear()
            self.profits.clear()
            
            with open(self.selected_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                
                for row in reader:
                    temp = float(row[0])  
                    profit = float(row[1]) 
                    self.temperatures.append(temp)
                    self.profits.append(profit)

            print(f"Loaded {len(self.temperatures)} rows successfully!")
            self.plot_graph()

    def plot_graph(self):
        self.ax.clear()
        self.ax.set_facecolor("#ffffff")
        self.ax.scatter(
            self.temperatures,
            self.profits,
            s=28,
            color="#2563eb",
            edgecolor="#ffffff",
            linewidth=0.6,
            alpha=0.8,
        )
    
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color("#cbd5e1")
        self.ax.spines['bottom'].set_color("#cbd5e1")
        self.ax.grid(True, color="#e2e8f0", linestyle="--", linewidth=0.8)
        self.ax.tick_params(colors="#64748b")
        
        self.ax.set_title("Ice Cream Profits vs Outside Temperature")
        self.ax.set_xlabel("Outside Temperature")
        self.ax.set_ylabel("Ice Cream Profits")
        
        coefficients = np.polyfit(self.temperatures, self.profits, 1)
        m = coefficients[0] 
        b = coefficients[1] 
        
        trendline_y = []
        for temp in self.temperatures:
            y_val = m * temp + b
            trendline_y.append(y_val)
            
        equation_text = f"y = {m:.2f}x + {b:.2f}"
        self.ax.plot(
            self.temperatures,
            trendline_y,
            color="#f97316",
            linewidth=2.5,
            label=equation_text,
        )
        
        self.ax.legend()
        self.canvas.draw()

    def show_about(self):
        about_text = "Name: Yinon Gabriel Debi\nGitHub: https://github.com/YinonGabriel/Q4"
        QMessageBox.about(self, "About", about_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IceCreamApp()
    window.show()
    sys.exit(app.exec())