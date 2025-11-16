"""
Декораторы для обработки ошибок, логирования и кэширования.
"""
import time
import functools
from prompt import string


def handle_db_errors(func):
    """
    Декоратор для перехвата ошибок базы данных.
    Обрабатывает KeyError, ValueError и FileNotFoundError.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Ошибка: Ключ не найден - {e}")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Ошибка: Файл не найден - {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None
    return wrapper


def confirm_action(action_name):
    """
    Декоратор-фабрика для подтверждения опасных операций.
    
    Args:
        action_name: Название действия для отображения пользователю
    
    Returns:
        Декоратор функции
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = string(prompt=f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if response.lower() != 'y':
                print("Операция отменена.")
                # Возвращаем исходные данные без изменений
                if len(args) > 0:
                    return args[0]  # Первый аргумент обычно metadata или table_data
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для замера времени выполнения функции.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """
    Фабрика для создания функции кэширования с замыканием.
    
    Returns:
        Функция cache_result(key, value_func) для кэширования результатов
    """
    cache = {}  # Кэш хранится в замыкании
    
    def cache_result(key, value_func):
        """
        Кэширует результат выполнения функции.
        
        Args:
            key: Ключ для кэша (должен быть хешируемым)
            value_func: Функция для получения значения, если его нет в кэше
        
        Returns:
            Результат из кэша или результат выполнения value_func()
        """
        if key in cache:
            return cache[key]
        
        result = value_func()
        cache[key] = result
        return result
    
    def clear_cache():
        """Очищает кэш."""
        cache.clear()
    
    # Добавляем метод очистки кэша
    cache_result.clear = clear_cache
    
    return cache_result
