from connect import get_connection

conn = get_connection()
cursor = conn.cursor()

# 1. Поиск по паттерну
def search_contacts():
    pattern = input("Введите часть имени или телефона: ")
    cursor.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Ничего не найдено.")

# 2. Upsert — вставить или обновить
def upsert_contact():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    cursor.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Контакт сохранён.")

# 3. Массовая вставка
def insert_many():
    contacts = []
    print("Вводите контакты (пустое имя — завершить):")
    while True:
        name = input("Имя: ")
        if not name:
            break
        phone = input("Телефон: ")
        contacts.append([name, phone])
    
    if contacts:
        cursor.execute("CALL insert_many_contacts(%s)", (contacts,))
        conn.commit()
        print("Контакты обработаны.")

# 4. Пагинация
def get_paginated():
    limit = int(input("Сколько записей показать: "))
    offset = int(input("Начиная с какой записи (0 = начало): "))
    cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("Записей нет.")

# 5. Удаление
def delete_contact():
    print("Удалить по:")
    print("1 - Имени")
    print("2 - Телефону")
    choice = input("Выбор: ")
    if choice == "1":
        value = input("Введите имя: ")
        cursor.execute("CALL delete_contact(%s, %s)", (value, "name"))
    elif choice == "2":
        value = input("Введите телефон: ")
        cursor.execute("CALL delete_contact(%s, %s)", (value, "phone"))
    conn.commit()
    print("Контакт удалён.")

# Меню
def main():
    while True:
        print("\n=== PhoneBook Practice 8 ===")
        print("1 - Поиск по паттерну")
        print("2 - Добавить / обновить контакт")
        print("3 - Массовая вставка")
        print("4 - Показать с пагинацией")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            upsert_contact()
        elif choice == "3":
            insert_many()
        elif choice == "4":
            get_paginated()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

    cursor.close()
    conn.close()

main()
