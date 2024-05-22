import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea, QMessageBox

class InterleaveApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_data = []
        self.labels = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamic JSON Interleaver with Weighted Distribution')
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(QVBoxLayout())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.btn_add_file = QPushButton('Add JSON File')
        self.btn_add_file.clicked.connect(self.add_json_file)
        self.btn_interleave = QPushButton('Interleave JSON Files')
        self.btn_interleave.clicked.connect(self.interleave_json)

        self.main_layout.addWidget(QLabel('Welcome to Dynamic JSON Interleaver!'))
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.btn_add_file)
        self.main_layout.addWidget(self.btn_interleave)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def add_json_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Load JSON File', '', 'JSON Files (*.json)')
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:  # Ensuring UTF-8 encoding
                    data = json.load(file)
                    self.json_data.append(data)
                    label = QLabel(f'Loaded: {filename}')
                    self.labels.append(label)
                    self.scroll_widget.layout().addWidget(label)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def interleave_json(self):
        if len(self.json_data) < 2:
            QMessageBox.warning(self, "Warning", "Please load at least two JSON files.")
            return

        try:
            interleaved_data = self.weighted_interleave(self.json_data.copy())
            self.save_interleaved(interleaved_data)
        except Exception as e:
            QMessageBox.critical(self, "Interleaving Error", f"An error occurred during interleaving: {e}")

    def weighted_interleave(self, datasets):
        total_items = sum(len(data) for data in datasets)
        active_indices = [i for i, data in enumerate(datasets) if len(data) > 0]

        interleaved_data = []

        while total_items > 0:
            weights = [len(datasets[i]) / total_items for i in active_indices]
            chosen_index = random.choices(active_indices, weights=weights)[0]
            interleaved_data.append(datasets[chosen_index].pop(0))
            total_items -= 1
            active_indices = [i for i in active_indices if len(datasets[i]) > 0]

        return interleaved_data

    def save_interleaved(self, interleaved_data):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Interleaved JSON', '', 'JSON Files (*.json)')
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:  # Ensuring UTF-8 encoding
                    json.dump(interleaved_data, file, indent=4)
                QMessageBox.information(self, "Success", f"Interleaved JSON saved to: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save interleaved JSON: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InterleaveApp()
    ex.show()
    sys.exit(app.exec_())
