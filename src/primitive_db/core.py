ALLOWED_TYPES = {'int', 'str', 'bool'}


def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных.
    
    Args:
        metadata: Словарь с метаданными базы данных
        table_name: Имя создаваемой таблицы
        columns: Список столбцов в формате [('name', 'type'), ...]
    
    Returns:
        Обновленный словарь метаданных
    """
    # Проверка существования таблицы
    if table_name in metadata:
        print(f"Ошибка: Таблица '{table_name}' уже существует.")
        return metadata
    
    # Проверка корректности типов данных
    for col_name, col_type in columns:
        if col_type not in ALLOWED_TYPES:
            print(f"Ошибка: Недопустимый тип данных '{col_type}'. Разрешены только: {', '.join(ALLOWED_TYPES)}")
            return metadata
    
    # Автоматическое добавление столбца ID:int в начало
    columns_with_id = [('ID', 'int')] + list(columns)
    
    # Обновление метаданных
    metadata[table_name] = {
        'columns': columns_with_id
    }
    
    print(f"Таблица '{table_name}' успешно создана.")
    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных.
    
    Args:
        metadata: Словарь с метаданными базы данных
        table_name: Имя удаляемой таблицы
    
    Returns:
        Обновленный словарь метаданных
    """
    # Проверка существования таблицы
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return metadata
    
    # Удаление таблицы из метаданных
    del metadata[table_name]
    
    print(f"Таблица '{table_name}' успешно удалена.")
    return metadata

