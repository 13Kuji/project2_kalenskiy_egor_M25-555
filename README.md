# Primitive DB

Простая база данных для управления таблицами и метаданными.

## Установка

```bash
poetry install
```

## Запуск

```bash
poetry run database
```

или

```bash
poetry run project
```

## Управление таблицами

### Создание таблицы

Создает новую таблицу с указанными столбцами. Столбец `ID:int` добавляется автоматически.

**Синтаксис:**
```
create_table <table_name> <col1:type1> <col2:type2> ...
```

**Пример:**
```
create_table users name:str age:int email:str active:bool
```

**Допустимые типы данных:**
- `int` - целое число
- `str` - строка
- `bool` - логическое значение

### Просмотр таблиц

Показывает список всех созданных таблиц и их структуру.

**Синтаксис:**
```
show_tables
```

### Удаление таблицы

Удаляет таблицу из базы данных.

**Синтаксис:**
```
drop_table <table_name>
```

**Пример:**
```
drop_table users
```

### Справка

Показывает список доступных команд.

**Синтаксис:**
```
help
```

### Выход

Завершает работу программы.

**Синтаксис:**
```
exit
```

## Демонстрация

### Демонстрация операций с таблицами
Посмотрите интерактивную демонстрацию работы базы данных:

[![asciicast](https://asciinema.org/a/cXlwBgIOYZ08or9lFKma70G6m.svg)](https://asciinema.org/a/cXlwBgIOYZ08or9lFKma70G6m)

Для создания записи выполните:
```bash
bash create_tables_demo.sh
```

Затем загрузите на asciinema.org:
```bash
asciinema upload tables_demo.cast
```

### Демонстрация CRUD-операций

Посмотрите интерактивную демонстрацию всех CRUD-операций (INSERT, SELECT, UPDATE, DELETE):

[![asciicast](https://asciinema.org/a/qKUZrMR1xFKTXvov1joU41U6U.svg)](https://asciinema.org/a/qKUZrMR1xFKTXvov1joU41U6U)

## Пример использования

```
<command> exit - выйти из программы
<command> help - справочная информация
Введите команду: create_table users name:str age:int email:str
Таблица 'users' успешно создана.

<command> exit - выйти из программы
<command> help - справочная информация
Введите команду: show_tables

Таблицы в базе данных:
  - users: ID:int, name:str, age:int, email:str

<command> exit - выйти из программы
<command> help - справочная информация
Введите команду: drop_table users
Таблица 'users' успешно удалена.

<command> exit - выйти из программы
<command> help - справочная информация
Введите команду: exit
```

## CRUD-операции

### INSERT - Вставка записей

Добавляет новую запись в таблицу. **ID генерируется автоматически** и не должен указываться в команде.

**Синтаксис:**
```
insert <table_name> <val1> <val2> <val3> ...
```

**Пример:**
```
# Для таблицы с колонками: ID (авто), name:str, age:int, email:str, active:bool
insert users John 28 john@example.com true
```

**Примечания:** 
- **ID не нужно указывать** - он генерируется автоматически на основе последней записи
- Количество значений должно соответствовать количеству столбцов **минус ID**
- Все поля являются обязательными и не могут быть пустыми
- Типы данных проверяются автоматически

### SELECT - Выборка записей

Выбирает записи из таблицы. Результаты отображаются в виде красивой таблицы с использованием библиотеки PrettyTable.

**Синтаксис:**
```
select <table_name> [where <column>=<value>]
```

**Примеры:**
```
# Выбрать все записи
select users

# Выбрать записи с условием
select users where age=28
select users where name='John'
select users where active=true
```

**Примечание:** 
- Строковые значения должны быть в кавычках: `'John'` или `"John"`
- Числовые значения указываются без кавычек: `28`
- Булевы значения: `true` или `false`

### UPDATE - Обновление записей

Обновляет записи в таблице по условию WHERE.

**Синтаксис:**
```
update <table_name> set <column>=<value> where <column>=<value>
```

**Примеры:**
```
update users set age=30 where name='John'
update users set active=false where age=25
update users set email='new@example.com' where ID=1
```

**Примечание:** ID нельзя изменять. Обновляются все записи, соответствующие условию WHERE.

### DELETE - Удаление записей

Удаляет записи из таблицы по условию WHERE.

**Синтаксис:**
```
delete <table_name> where <column>=<value>
```

**Примеры:**
```
delete users where ID=1
delete users where age=25
delete users where active=false
```

**Примечание:** Условие WHERE обязательно. Удаляются все записи, соответствующие условию.

## Хранение данных

Метаданные о таблицах хранятся в файле `db_meta.json` в формате JSON.
Данные каждой таблицы хранятся в отдельных JSON-файлах в директории `data/`.
Например, данные таблицы `users` хранятся в файле `data/users.json`.

## Разработка

### Установка зависимостей для разработки

```bash
poetry install --with dev
```

### Проверка кода

```bash
make lint
```

### Сборка пакета

```bash
make build
```

