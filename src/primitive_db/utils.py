import json
import os


def load_metadata(filepath):
    """Загружает данные из JSON-файла. Если файл не найден, возвращает пустой словарь."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет переданные данные в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла. Если файл не найден, возвращает пустой список."""
    # Создаем директорию data, если её нет
    os.makedirs('data', exist_ok=True)
    
    filepath = f'data/{table_name}.json'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл."""
    # Создаем директорию data, если её нет
    os.makedirs('data', exist_ok=True)
    
    filepath = f'data/{table_name}.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

