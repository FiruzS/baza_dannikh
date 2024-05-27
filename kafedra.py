import sqlite3
import re

# Создание базы данных и таблицы
conn = sqlite3.connect('kafedra.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS kafedra
             (kod_kafedri INTEGER PRIMARY KEY, 
              nazvanie_kafedri TEXT, 
              adres_kafedri TEXT, 
              kontaktnye_dannye TEXT)''')
conn.commit()

def add_kafedra(nazvanie_kafedri, adres_kafedri, kontaktnye_dannye):
    # Проверка формата контактных данных
    if not re.match(r'^\+\d{11,12}$', kontaktnye_dannye):
        raise ValueError("Неверный формат контактных данных")
    c.execute("INSERT INTO kafedra (nazvanie_kafedri, adres_kafedri, kontaktnye_dannye) VALUES (?, ?, ?)",
              (nazvanie_kafedri, adres_kafedri, kontaktnye_dannye))
    conn.commit()

def edit_kafedra(kod_kafedri, nazvanie_kafedri, adres_kafedri, kontaktnye_dannye):
    # Проверка формата контактных данных
    if not re.match(r'^\+\d{11,12}$', kontaktnye_dannye):
        raise ValueError("Неверный формат контактных данных")
    c.execute("UPDATE kafedra SET nazvanie_kafedri = ?, adres_kafedri = ?, kontaktnye_dannye = ? WHERE kod_kafedri = ?",
              (nazvanie_kafedri, adres_kafedri, kontaktnye_dannye, kod_kafedri))
    conn.commit()

def delete_kafedra(kod_kafedri):
    c.execute("DELETE FROM kafedra WHERE kod_kafedri = ?", (kod_kafedri,))
    conn.commit()

def get_all_kafedra():
    c.execute("SELECT * FROM kafedra")
    return c.fetchall()
