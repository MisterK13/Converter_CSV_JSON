import os

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton,QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from convert import FileConverter, FileGenerator, MESSAGES, TEST_JSON_FILE, TEST_CSV_FILE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_file_path = None
        self.init_interface()
        self.generate_test_files()

    def init_interface(self):
        self.setWindowTitle("Конвертер CSV/JSON")
        self.setMinimumSize(500, 200)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Отображения выбранного файла
        self.file_label = QLabel("Файл не выбран")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("padding: 10px; border: 1px solid #ccc;")
        main_layout.addWidget(self.file_label)

        # Кнопка выбора файла
        self.select_button = QPushButton("Выбрать файл (CSV или JSON)")
        self.select_button.clicked.connect(self.select_file)
        main_layout.addWidget(self.select_button)

        # Кнопки конвертации
        convert_layout = QHBoxLayout()

        self.to_json_button = QPushButton("Конвертировать в JSON")
        self.to_json_button.clicked.connect(self.convert_to_json)
        self.to_json_button.setEnabled(False)

        self.to_csv_button = QPushButton("Конвертировать в CSV")
        self.to_csv_button.clicked.connect(self.convert_to_csv)
        self.to_csv_button.setEnabled(False)

        convert_layout.addWidget(self.to_json_button)
        convert_layout.addWidget(self.to_csv_button)
        main_layout.addLayout(convert_layout)

        # Кнопка генерации тестовых файлов
        self.test_button = QPushButton("Сгенерировать тестовые файлы заново")
        self.test_button.clicked.connect(self.generate_test_files)
        main_layout.addWidget(self.test_button)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Данные (*.csv *.json);;Все файлы (*)"
        )

        if file_path:
            self.input_file_path = file_path
            self.file_label.setText(f"Выбран: {file_path.split('/')[-1]}")
            self.to_json_button.setEnabled(True)
            self.to_csv_button.setEnabled(True)

    def generate_test_files(self):
        save_directory = os.path.dirname(os.path.abspath(__file__))

        csv_exists = os.path.exists(os.path.join(save_directory, TEST_CSV_FILE))
        json_exists = os.path.exists(os.path.join(save_directory, TEST_JSON_FILE))

        if csv_exists and json_exists:
            return

        generator = FileGenerator()
        csv_path, json_path = generator.generate_file(save_directory)

        if not csv_exists or not json_exists:
            QMessageBox.information(
                self,
                "Тестовые файлы созданы",
                MESSAGES["test_files_created"].format(
                    os.path.basename(csv_path),
                    os.path.basename(json_path)
                )
            )

    def convert_to_json(self):
        self._convert_file('json')

    def convert_to_csv(self):
        self._convert_file('csv')

    def _convert_file(self, target_format: str):

        if not self.input_file_path:
            QMessageBox.warning(self, "Предупреждение", MESSAGES["select_file"])
            return

        base_name = os.path.splitext(self.input_file_path)[0]
        output_path = f"{base_name}_converted.{target_format}"

        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base_name}_converted_{counter}.{target_format}"
            counter += 1

        converter = FileConverter()
        if converter.convert_file(self.input_file_path, output_path):
            QMessageBox.information(
                self,
                "Успех",
                MESSAGES["success"].format(os.path.basename(output_path))
            )