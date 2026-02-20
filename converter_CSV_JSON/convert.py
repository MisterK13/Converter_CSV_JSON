import os
import pandas as pd
import json
from PyQt6.QtWidgets import QMessageBox

FILE_CONVERT_FORMAT = ('csv', 'json')
TEST_CSV_FILE = 'test.csv'
TEST_JSON_FILE = 'test.json'
MESSAGES = {
    "select_file": "Выберите файл.",
    "empty_file": "Файл пуст.",
    "success": "Конвертация успешно завершена!\nСоздан файл: {}",
    "invalid_format": "Неверный формат. Поддерживаются только файлы .csv и .json",
    "same_format": "Форматы одинаковы, конвертация не требуется.",
    "test_files_created": "Тестовые файлы созданы:\n{}\n{}",
}

class FileConverter:
    @staticmethod
    def convert_file(input_file_path: str, output_file_path: str) -> bool:
        try:
            if os.path.getsize(input_file_path) == 0:
                QMessageBox.critical(None, "Ошибка", MESSAGES["empty_file"])
                return False

            input_format = input_file_path.split('.')[-1].lower()
            output_format = output_file_path.split('.')[-1].lower()

            if input_format not in FILE_CONVERT_FORMAT or output_format not in FILE_CONVERT_FORMAT:
                QMessageBox.critical(None, "Ошибка", MESSAGES["invalid_format"])
                return False

            if input_format == output_format:
                QMessageBox.critical(None, "Ошибка", MESSAGES["same_format"])
                return False

            if input_format == 'csv':
                df = pd.read_csv(input_file_path)
            else:
                df = pd.read_json(input_file_path, orient='records')

            if output_format == 'csv':
                df.to_csv(output_file_path, index=False)
            else:
                df.to_json(output_file_path, orient='records', indent=4, force_ascii=False)

            return True

        except pd.errors.EmptyDataError:
            QMessageBox.critical(None, "Ошибка", f"Файл содержит только заголовки без данных")
            return False
        except (json.JSONDecodeError, ValueError) as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка чтения файла\n{str(e)}")
            return False
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Неизвестная ошибка\n{str(e)}")
            return False

class FileGenerator:
    @staticmethod
    def generate_file(save_directory: str):
        test_data = {
            "Имя": ["Кирилл", "Антон", "Влад", "Анастасия", "Ирина", "Александра"],
            "Возраст": [28, 26, 27, 25, 24, 26],
            "Город": ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Владивосток"],
            "Активен": [False, True, True, True, False, True]
        }
        df = pd.DataFrame(test_data)

        csv_path = os.path.join(save_directory, TEST_CSV_FILE)
        json_path = os.path.join(save_directory, TEST_JSON_FILE)

        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        df.to_json(json_path, orient='records', indent=4, force_ascii=False)

        return csv_path, json_path
