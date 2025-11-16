ALLOWED_TYPES = {'int', 'str', 'bool'}


def _validate_type(value, expected_type):
    """Проверяет, соответствует ли значение ожидаемому типу."""
    if expected_type == 'int':
        return isinstance(value, int)
    elif expected_type == 'str':
        return isinstance(value, str)
    elif expected_type == 'bool':
        return isinstance(value, bool)
    return False


def _convert_value(value, expected_type):
    """Преобразует значение в нужный тип."""
    try:
        if expected_type == 'int':
            return int(value)
        elif expected_type == 'str':
            return str(value)
        elif expected_type == 'bool':
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return bool(value)
    except (ValueError, TypeError):
        return None
    return value


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


def insert(metadata, table_name, values):
    """
    Вставляет новую запись в таблицу.
    
    Args:
        metadata: Словарь с метаданными базы данных
        table_name: Имя таблицы
        values: Список значений для вставки (без ID)
    
    Returns:
        Обновленные данные таблицы или None при ошибке
    """
    # Проверка существования таблицы
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return None
    
    # Получаем схему таблицы
    table_info = metadata[table_name]
    columns = table_info.get('columns', [])
    
    # Проверка количества значений (минус ID)
    expected_count = len(columns) - 1  # Все столбцы кроме ID
    if len(values) != expected_count:
        column_names = [col[0] for col in columns[1:]]  # Исключаем ID
        print(f"Ошибка: Количество значений ({len(values)}) не соответствует количеству столбцов ({expected_count}).")
        print(f"Ожидаемые столбцы (ID генерируется автоматически): {', '.join(column_names)}")
        return None
    
    # Загружаем текущие данные таблицы
    from .utils import load_table_data
    table_data = load_table_data(table_name)
    
    # Генерируем новый ID
    if table_data:
        max_id = max(row.get('ID', 0) for row in table_data)
        new_id = max_id + 1
    else:
        new_id = 1
    
    # Создаем новую запись
    new_row = {'ID': new_id}
    
    # Валидация и добавление значений
    for i, (col_name, col_type) in enumerate(columns[1:], 0):  # Пропускаем ID
        value = values[i]
        
        # Проверка на пустое значение (все поля обязательные)
        if value is None or (isinstance(value, str) and value.strip() == ''):
            print(f"Ошибка: Поле '{col_name}' является обязательным и не может быть пустым.")
            return None
        
        # Преобразуем значение в нужный тип
        converted_value = _convert_value(value, col_type)
        if converted_value is None:
            print(f"Ошибка: Невозможно преобразовать значение '{value}' в тип {col_type} для столбца '{col_name}'.")
            return None
        
        # Дополнительная проверка на пустые строки после преобразования
        if col_type == 'str' and isinstance(converted_value, str) and converted_value.strip() == '':
            print(f"Ошибка: Поле '{col_name}' является обязательным и не может быть пустым.")
            return None
        
        # Валидация типа
        if not _validate_type(converted_value, col_type):
            print(f"Ошибка: Значение '{converted_value}' не соответствует типу {col_type} для столбца '{col_name}'.")
            return None
        
        new_row[col_name] = converted_value
    
    # Добавляем запись
    table_data.append(new_row)
    
    print(f"Запись успешно добавлена в таблицу '{table_name}' (ID: {new_id}).")
    return table_data


def select(table_data, where_clause=None):
    """
    Выбирает записи из таблицы с опциональным условием WHERE.
    
    Args:
        table_data: Список записей таблицы
        where_clause: Словарь условий, например {'age': 28}
    
    Returns:
        Список отфильтрованных записей
    """
    if where_clause is None:
        return table_data
    
    # Фильтрация по условиям
    result = []
    for row in table_data:
        match = True
        for column, value in where_clause.items():
            if column not in row or row[column] != value:
                match = False
                break
        if match:
            result.append(row)
    
    return result


def update(table_data, set_clause, where_clause):
    """
    Обновляет записи в таблице.
    
    Args:
        table_data: Список записей таблицы
        set_clause: Словарь полей для обновления, например {'age': 30}
        where_clause: Словарь условий, например {'name': 'John'}
    
    Returns:
        Обновленные данные таблицы
    """
    updated_count = 0
    
    for row in table_data:
        # Проверяем условие WHERE
        match = True
        if where_clause:
            for column, value in where_clause.items():
                if column not in row or row[column] != value:
                    match = False
                    break
        
        if match:
            # Обновляем поля согласно SET
            for column, value in set_clause.items():
                if column != 'ID':  # ID нельзя изменять
                    row[column] = value
            updated_count += 1  # Считаем записи, а не поля
    
    if updated_count > 0:
        print(f"Обновлено записей: {updated_count}.")
    else:
        print("Записи для обновления не найдены.")
    
    return table_data


def delete(table_data, where_clause):
    """
    Удаляет записи из таблицы по условию WHERE.
    
    Args:
        table_data: Список записей таблицы
        where_clause: Словарь условий, например {'age': 28}
    
    Returns:
        Обновленные данные таблицы
    """
    if where_clause is None:
        print("Ошибка: Условие WHERE обязательно для команды DELETE.")
        return table_data
    
    # Находим индексы записей для удаления
    indices_to_remove = []
    for i, row in enumerate(table_data):
        match = True
        for column, value in where_clause.items():
            if column not in row or row[column] != value:
                match = False
                break
        if match:
            indices_to_remove.append(i)
    
    # Удаляем записи в обратном порядке
    for i in reversed(indices_to_remove):
        del table_data[i]
    
    deleted_count = len(indices_to_remove)
    if deleted_count > 0:
        print(f"Удалено записей: {deleted_count}.")
    else:
        print("Записи для удаления не найдены.")
    
    return table_data

