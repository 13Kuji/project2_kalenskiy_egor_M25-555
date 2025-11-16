"""
Парсеры для разбора условий WHERE и SET в SQL-подобных командах.
"""


def parse_where_clause(where_str):
    """
    Парсит строку условия WHERE в словарь.
    
    Примеры:
        "age = 28" -> {'age': 28}
        "name = 'John'" -> {'name': 'John'}
        "active = true" -> {'active': True}
    
    Args:
        where_str: Строка условия, например "age = 28"
    
    Returns:
        Словарь вида {'column': value} или None при ошибке
    """
    if not where_str:
        return None
    
    # Разбиваем по '='
    parts = where_str.split('=', 1)
    if len(parts) != 2:
        return None
    
    column = parts[0].strip()
    value_str = parts[1].strip()
    
    # Обработка значений
    # Строки в кавычках
    if value_str.startswith("'") and value_str.endswith("'"):
        value = value_str[1:-1]
    elif value_str.startswith('"') and value_str.endswith('"'):
        value = value_str[1:-1]
    # Булевы значения
    elif value_str.lower() == 'true':
        value = True
    elif value_str.lower() == 'false':
        value = False
    # Целые числа
    elif value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        value = int(value_str)
    else:
        # Попытка как строка без кавычек (для обратной совместимости)
        value = value_str
    
    return {column: value}


def parse_set_clause(set_str):
    """
    Парсит строку условия SET в словарь.
    
    Примеры:
        "age = 30" -> {'age': 30}
        "name = 'Jane'" -> {'name': 'Jane'}
        "active = false" -> {'active': False}
    
    Args:
        set_str: Строка условия, например "age = 30"
    
    Returns:
        Словарь вида {'column': value} или None при ошибке
    """
    # SET использует тот же формат, что и WHERE
    return parse_where_clause(set_str)

