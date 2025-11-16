import shlex
from prompt import string

from .utils import load_metadata, save_metadata
from .core import create_table, drop_table

METADATA_FILE = 'db_meta.json'


def run():
    """Главная функция, содержащая основной цикл программы."""
    while True:
        # Загрузка актуальных метаданных
        metadata = load_metadata(METADATA_FILE)
        
        # Запрос ввода у пользователя
        print("\n<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        user_input = string(prompt="Введите команду: ")
        
        # Разбор введенной строки на команду и аргументы
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: Некорректный ввод.")
            continue
        
        if not args:
            continue
        
        command = args[0].lower()
        
        # Обработка команд
        if command == "exit":
            break
        elif command == "help":
            print("\n<command> exit - выйти из программы")
            print("<command> help - справочная информация")
            print("<command> create_table <table_name> <col1:type1> <col2:type2> ... - создать таблицу")
            print("<command> drop_table <table_name> - удалить таблицу")
            print("<command> show_tables - показать все таблицы")
        elif command == "create_table":
            if len(args) < 2:
                print("Ошибка: Укажите имя таблицы и столбцы.")
                continue
            
            table_name = args[1]
            columns = []
            
            # Парсинг столбцов
            for col_arg in args[2:]:
                if ':' not in col_arg:
                    print(f"Ошибка: Некорректный формат столбца '{col_arg}'. Используйте формат 'name:type'")
                    break
                col_name, col_type = col_arg.split(':', 1)
                columns.append((col_name, col_type))
            else:
                # Если цикл завершился без break, обновляем метаданные
                metadata = create_table(metadata, table_name, columns)
                save_metadata(METADATA_FILE, metadata)
        elif command == "drop_table":
            if len(args) < 2:
                print("Ошибка: Укажите имя таблицы.")
                continue
            
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(METADATA_FILE, metadata)
        elif command == "show_tables":
            if not metadata:
                print("База данных пуста. Таблиц нет.")
            else:
                print("\nТаблицы в базе данных:")
                for table_name, table_info in metadata.items():
                    columns = table_info.get('columns', [])
                    col_str = ', '.join([f"{col[0]}:{col[1]}" for col in columns])
                    print(f"  - {table_name}: {col_str}")
        else:
            print(f"Неизвестная команда: {command}. Введите 'help' для справки.")
