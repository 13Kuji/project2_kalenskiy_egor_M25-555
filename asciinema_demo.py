#!/usr/bin/env python3
"""
Скрипт для создания входных данных для asciinema с реалистичными задержками.
Используется вместе с asciinema rec для создания записи.
"""
import time
import sys

def type_command(cmd, delay=0.8):
    """Имитирует ввод команды с задержкой."""
    # Печатаем команду посимвольно для реалистичности
    for char in cmd:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)  # Небольшая задержка между символами
    
    sys.stdout.write('\n')
    sys.stdout.flush()
    time.sleep(delay)  # Задержка после команды

def main():
    # Очистка
    import os
    if os.path.exists('db_meta.json'):
        os.remove('db_meta.json')
    
    # Небольшая задержка в начале
    time.sleep(0.5)
    
    # Команды для демонстрации
    type_command("help", 0.8)
    type_command("create_table users name:str age:int email:str active:bool", 1.2)
    type_command("show_tables", 1.0)
    type_command("create_table products title:str price:int in_stock:bool", 1.2)
    type_command("show_tables", 1.0)
    type_command("drop_table products", 1.0)
    type_command("show_tables", 1.0)
    type_command("exit", 0.5)

if __name__ == '__main__':
    main()

