import shlex
from prompt import string
from prettytable import PrettyTable

from .utils import load_metadata, save_metadata, load_table_data, save_table_data
from .core import create_table, drop_table, insert, select, update, delete
from .parser import parse_where_clause, parse_set_clause

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
            print("<command> insert <table_name> <val1> <val2> ... - вставить запись")
            print("<command> select <table_name> [where <column>=<value>] - выбрать записи")
            print("<command> update <table_name> set <column>=<value> where <column>=<value> - обновить записи")
            print("<command> delete <table_name> where <column>=<value> - удалить записи")
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
        elif command == "insert":
            if len(args) < 3:
                print("Ошибка: Укажите имя таблицы и значения для вставки.")
                continue
            
            table_name = args[1]
            values = args[2:]
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name)
            
            # Выполняем вставку
            updated_data = insert(metadata, table_name, values)
            if updated_data is not None:
                save_table_data(table_name, updated_data)
        elif command == "select":
            if len(args) < 2:
                print("Ошибка: Укажите имя таблицы.")
                continue
            
            table_name = args[1]
            
            # Проверка существования таблицы
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                continue
            
            # Парсинг WHERE условия
            where_clause = None
            if len(args) > 2:
                if args[2].lower() == 'where' and len(args) > 3:
                    where_str = args[3]
                    where_clause = parse_where_clause(where_str)
                    if where_clause is None:
                        print("Ошибка: Некорректный формат условия WHERE. Используйте: where column=value")
                        continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name)
            
            # Выполняем выборку
            result = select(table_data, where_clause)
            
            # Выводим результат с помощью PrettyTable
            if not result:
                print("Записи не найдены.")
            else:
                # Получаем названия столбцов из метаданных
                table_info = metadata[table_name]
                columns = table_info.get('columns', [])
                column_names = [col[0] for col in columns]
                
                # Создаем таблицу для вывода
                pt = PrettyTable()
                pt.field_names = column_names
                
                # Добавляем строки
                for row in result:
                    pt.add_row([row.get(col, '') for col in column_names])
                
                print()
                print(pt)
        elif command == "update":
            if len(args) < 6:
                print("Ошибка: Используйте формат: update <table_name> set <column>=<value> where <column>=<value>")
                continue
            
            table_name = args[1]
            
            # Проверка существования таблицы
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                continue
            
            # Парсинг SET и WHERE
            if args[2].lower() != 'set' or args[4].lower() != 'where':
                print("Ошибка: Используйте формат: update <table_name> set <column>=<value> where <column>=<value>")
                continue
            
            set_str = args[3]
            where_str = args[5]
            
            set_clause = parse_set_clause(set_str)
            where_clause = parse_where_clause(where_str)
            
            if set_clause is None or where_clause is None:
                print("Ошибка: Некорректный формат условий. Используйте: column=value")
                continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name)
            
            # Выполняем обновление
            updated_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, updated_data)
        elif command == "delete":
            if len(args) < 4:
                print("Ошибка: Используйте формат: delete <table_name> where <column>=<value>")
                continue
            
            table_name = args[1]
            
            # Проверка существования таблицы
            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не существует.")
                continue
            
            # Парсинг WHERE
            if args[2].lower() != 'where':
                print("Ошибка: Используйте формат: delete <table_name> where <column>=<value>")
                continue
            
            where_str = args[3]
            where_clause = parse_where_clause(where_str)
            
            if where_clause is None:
                print("Ошибка: Некорректный формат условия WHERE. Используйте: where column=value")
                continue
            
            # Загружаем данные таблицы
            table_data = load_table_data(table_name)
            
            # Выполняем удаление
            updated_data = delete(table_data, where_clause)
            save_table_data(table_name, updated_data)
        else:
            print(f"Неизвестная команда: {command}. Введите 'help' для справки.")
