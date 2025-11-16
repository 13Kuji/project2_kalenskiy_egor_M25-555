#!/bin/bash
# Скрипт для создания asciinema демонстрации

# Очистка предыдущих данных
rm -f db_meta.json

# Создаем файл с командами для демонстрации
cat > /tmp/demo_input.txt << 'EOF'
help
create_table users name:str age:int email:str active:bool
show_tables
create_table products title:str price:int in_stock:bool
show_tables
drop_table products
show_tables
exit
EOF

# Запускаем запись
echo "Начинаем запись демонстрации..."
asciinema rec -c "poetry run database" demo.cast < /tmp/demo_input.txt

echo "Запись завершена. Файл: demo.cast"
echo "Для загрузки выполните: asciinema upload demo.cast"

