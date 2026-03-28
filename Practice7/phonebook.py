import csv
from connect import get_connection

conn = get_connection()
cursor = conn.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE
        )
    """)
    conn.commit()

def insert_from_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name, phone = row[0], row[1]
            cursor.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                (name, phone)
            )
    conn.commit()
    print("Данные из CSV загружены.")

def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    cursor.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
        (name, phone)
    )
    conn.commit()
    print("Контакт добавлен.")

def update_contact():
    print("Что обновить?")
    print("1 - Имя")
    print("2 - Телефон")
    choice = input("Выбор: ")
    if choice == "1":
        old_name = input("Введите текущее имя: ")
        new_name = input("Введите новое имя: ")
        cursor.execute(
            "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
            (new_name, old_name)
        )
    elif choice == "2":
        old_phone = input("Введите текущий телефон: ")
        new_phone = input("Введите новый телефон: ")
        cursor.execute(
            "UPDATE phonebook SET phone = %s WHERE phone = %s",
            (new_phone, old_phone)
        )
    conn.commit()
    print("Контакт обновлён.")

def search_contacts():
    print("Поиск по:")
    print("1 - Имени")
    print("2 - Префиксу телефона")
    choice = input("Выбор: ")
    if choice == "1":
        name = input("Введите имя (или часть): ")
        cursor.execute(
            "SELECT * FROM phonebook WHERE first_name ILIKE %s",
            (f"%{name}%",)
        )
    elif choice == "2":
        prefix = input("Введите префикс телефона: ")
        cursor.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Ничего не найдено.")

def delete_contact():
    print("Удалить по:")
    print("1 - Имени")
    print("2 - Телефону")
    choice = input("Выбор: ")
    if choice == "1":
        name = input("Введите имя: ")
        cursor.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "2":
        phone = input("Введите телефон: ")
        cursor.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Контакт удалён.")

def main():
    create_table()
    while True:
        print("\n=== Телефонная книга ===")
        print("1 - Загрузить из CSV")
        print("2 - Добавить контакт вручную")
        print("3 - Обновить контакт")
        print("4 - Найти контакт")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")
        if choice == "1":
            filename = input("Введите имя CSV файла: ")
            insert_from_csv(filename)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

    cursor.close()
    conn.close()

main()
