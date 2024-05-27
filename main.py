import tkinter as tk
from tkinter import ttk
import re
import sqlite3
import openpyxl


# Подключение к базе данных
conn = sqlite3.connect('kursach.db')
c = conn.cursor()

# Создание таблицы, если она не существует
c.execute('''CREATE TABLE IF NOT EXISTS departments
             (code INTEGER PRIMARY KEY, name TEXT, address TEXT, contact TEXT)''')
conn.commit()


c.execute('''CREATE TABLE IF NOT EXISTS teachers
             (code INTEGER PRIMARY KEY, surname TEXT, name TEXT, patronymic TEXT, subject TEXT)''')
conn.commit()


c.execute('''CREATE TABLE IF NOT EXISTS students
             (code INTEGER PRIMARY KEY, surname TEXT, name TEXT, patronymic TEXT, specialty TEXT)''')
conn.commit()



c.execute('''CREATE TABLE IF NOT EXISTS exams
             (code INTEGER PRIMARY KEY, department_code INTEGER, exam_date TEXT, exam_time TEXT, teacher_code INTEGER)''')
conn.commit()



c.execute('''CREATE TABLE IF NOT EXISTS schedule
             (code INTEGER PRIMARY KEY, schedule_date TEXT, schedule_time TEXT, room TEXT, teacher_code INTEGER)''')
conn.commit()



def show_department_table():
    # Получение данных из базы данных
    c.execute("SELECT * FROM departments")
    departments = c.fetchall()

    # Создание таблицы кафедры
    department_table = tk.Toplevel(root)
    department_table.title("Кафедры")

    # Таблица с кафедрами
    tree = ttk.Treeview(department_table)
    tree["columns"] = ("1", "2", "3")
    tree.column("#0", width=100)
    tree.column("1", width=150)
    tree.column("2", width=200)
    tree.column("3", width=200)
    tree.heading("#0", text="Код кафедры")
    tree.heading("1", text="Название кафедры")
    tree.heading("2", text="Адрес кафедры")
    tree.heading("3", text="Контактные данные")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Заполнение таблицы данными
    for department in departments:
        tree.insert("", "end", text=str(department[0]), values=department[1:])

    # Кнопки для работы с таблицей
    button_frame = tk.Frame(department_table)
    button_frame.pack(side=tk.BOTTOM)

    add_button = tk.Button(button_frame, text="Добавить", command=lambda: add_department(tree))
    add_button.pack(side=tk.LEFT)

    edit_button = tk.Button(button_frame, text="Изменить", command=lambda: edit_department(tree))
    edit_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_department(tree))
    delete_button.pack(side=tk.LEFT)

def add_department(tree):
    # Создание окна для добавления кафедры
    add_window = tk.Toplevel(root)
    add_window.title("Добавить кафедру")

    # Поля для ввода данных
    code_label = tk.Label(add_window, text="Код кафедры:")
    code_entry = tk.Entry(add_window)
    name_label = tk.Label(add_window, text="Название кафедры:")
    name_entry = tk.Entry(add_window)
    address_label = tk.Label(add_window, text="Адрес кафедры:")
    address_entry = tk.Entry(add_window)
    contact_label = tk.Label(add_window, text="Контактные данные:")
    contact_entry = tk.Entry(add_window)

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    address_label.grid(row=2, column=0)
    address_entry.grid(row=2, column=1)
    contact_label.grid(row=3, column=0)
    contact_entry.grid(row=3, column=1)

    # Кнопка для добавления кафедры
    add_button = tk.Button(add_window, text="Добавить", command=lambda: save_department(tree, code_entry, name_entry, address_entry, contact_entry, add_window))
    add_button.grid(row=4, column=0, columnspan=2)

def save_department(tree, code_entry, name_entry, address_entry, contact_entry, add_window):

    # Проверка формата контактных данных
    contact_data = contact_entry.get()
    if not re.match(r'\+\d{11}', contact_data):
        # Показ сообщения об ошибке в новом окне
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Неправильный формат контактных данных. Пример: +79202153137")
        error_label.pack(padx=20, pady=20)
        return

    # Добавление кафедры в базу данных
    code = int(code_entry.get())
    c.execute("SELECT COUNT(*) FROM departments WHERE code = ?", (code,))
    count = c.fetchone()[0]
    if count > 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Код кафедры уже существует.")
        error_label.pack(padx=20, pady=20)
        return

    name = name_entry.get()
    address = address_entry.get()
    c.execute("INSERT INTO departments (code, name, address, contact) VALUES (?, ?, ?, ?)", (code, name, address, contact_data))
    conn.commit()

    # Обновление таблицы
    tree.insert("", "end", text=str(code), values=[name, address, contact_data])

    # Закрытие окна добавления
    code_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    code_entry.focus_set()
    add_window.destroy()

def edit_department(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Получение данных выбранной строки из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("SELECT * FROM departments WHERE code = ?", (code,))
    department = c.fetchone()

    # Создание окна для редактирования кафедры
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить кафедру")

    # Поля для ввода данных
    code_label = tk.Label(edit_window, text="Код кафедры:")
    code_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=str(department[0])))
    name_label = tk.Label(edit_window, text="Название кафедры:")
    name_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=department[1]))
    address_label = tk.Label(edit_window, text="Адрес кафедры:")
    address_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=department[2]))
    contact_label = tk.Label(edit_window, text="Контактные данные:")
    contact_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=department[3]))

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    address_label.grid(row=2, column=0)
    address_entry.grid(row=2, column=1)
    contact_label.grid(row=3, column=0)
    contact_entry.grid(row=3, column=1)

    # Кнопка для сохранения изменений
    save_button = tk.Button(edit_window, text="Изменить", command=lambda: update_department(tree, selected, code_entry, name_entry, address_entry, contact_entry, edit_window))
    save_button.grid(row=4, column=0, columnspan=2)

def update_department(tree, selected, code_entry, name_entry, address_entry, contact_entry, edit_window):
    # Проверка формата контактных данных
    contact_data = contact_entry.get()
    if not re.match(r'\+\d{11}', contact_data):
        # Показ сообщения об ошибке в новом окне
        error_window = tk.Toplevel(edit_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Неправильный формат контактных данных. Пример: +79202153137")
        error_label.pack(padx=20, pady=20)
        return

    # Обновление данных в базе данных
    new_code = int(code_entry.get())
    name = name_entry.get()
    address = address_entry.get()
    c.execute("UPDATE departments SET code = ?, name = ?, address = ?, contact = ? WHERE code = ?",
              (new_code, name, address, contact_data, int(tree.item(selected, "text"))))
    conn.commit()

    # Обновление таблицы
    tree.item(selected, text=str(new_code), values=[name, address, contact_data])
    edit_window.destroy()

def delete_department(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Удаление кафедры из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("DELETE FROM departments WHERE code = ?", (code,))
    conn.commit()

    # Удаление строки из таблицы
    tree.delete(selected)

def show_teacher_table():
    # Получение данных из базы данных
    c.execute("SELECT * FROM teachers")
    teachers = c.fetchall()

    # Создание таблицы преподавателей
    teacher_table = tk.Toplevel(root)
    teacher_table.title("Преподаватели")

    # Таблица с преподавателями
    tree = ttk.Treeview(teacher_table)
    tree["columns"] = ("1", "2", "3", "4")
    tree.column("#0", width=100)
    tree.column("1", width=150)
    tree.column("2", width=150)
    tree.column("3", width=150)
    tree.column("4", width=200)
    tree.heading("#0", text="Код преподавателя")
    tree.heading("1", text="Фамилия")
    tree.heading("2", text="Имя")
    tree.heading("3", text="Отчество")
    tree.heading("4", text="Предмет")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Заполнение таблицы данными
    for teacher in teachers:
        tree.insert("", "end", text=str(teacher[0]), values=teacher[1:])

    # Кнопки для работы с таблицей
    button_frame = tk.Frame(teacher_table)
    button_frame.pack(side=tk.BOTTOM)

    add_button = tk.Button(button_frame, text="Добавить", command=lambda: add_teacher(tree))
    add_button.pack(side=tk.LEFT)

    edit_button = tk.Button(button_frame, text="Изменить", command=lambda: edit_teacher(tree))
    edit_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_teacher(tree))
    delete_button.pack(side=tk.LEFT)


def add_teacher(tree):
    # Создание окна для добавления преподавателя
    add_window = tk.Toplevel(root)
    add_window.title("Добавить преподавателя")

    # Поля для ввода данных
    code_label = tk.Label(add_window, text="Код преподавателя:")
    code_entry = tk.Entry(add_window)
    surname_label = tk.Label(add_window, text="Фамилия:")
    surname_entry = tk.Entry(add_window)
    name_label = tk.Label(add_window, text="Имя:")
    name_entry = tk.Entry(add_window)
    patronymic_label = tk.Label(add_window, text="Отчество:")
    patronymic_entry = tk.Entry(add_window)
    subject_label = tk.Label(add_window, text="Предмет:")
    subject_entry = tk.Entry(add_window)

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    surname_label.grid(row=1, column=0)
    surname_entry.grid(row=1, column=1)
    name_label.grid(row=2, column=0)
    name_entry.grid(row=2, column=1)
    patronymic_label.grid(row=3, column=0)
    patronymic_entry.grid(row=3, column=1)
    subject_label.grid(row=4, column=0)
    subject_entry.grid(row=4, column=1)

    # Кнопка для добавления преподавателя
    add_button = tk.Button(add_window, text="Добавить",
                           command=lambda: save_teacher(tree, code_entry, surname_entry, name_entry, patronymic_entry,
                                                        subject_entry, add_window))
    add_button.grid(row=5, column=0, columnspan=2)


def save_teacher(tree, code_entry, surname_entry, name_entry, patronymic_entry, subject_entry, add_window):
    # Добавление преподавателя в базу данных
    code = int(code_entry.get())
    c.execute("SELECT COUNT(*) FROM teachers WHERE code = ?", (code,))
    count = c.fetchone()[0]
    if count > 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Код преподавателя уже существует.")
        error_label.pack(padx=20, pady=20)
        return

    surname = surname_entry.get()
    name = name_entry.get()
    patronymic = patronymic_entry.get()
    subject = subject_entry.get()
    c.execute("INSERT INTO teachers (code, surname, name, patronymic, subject) VALUES (?, ?, ?, ?, ?)",
              (code, surname, name, patronymic, subject))
    conn.commit()

    # Обновление таблицы
    tree.insert("", "end", text=str(code), values=[surname, name, patronymic, subject])

    # Закрытие окна добавления
    code_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    patronymic_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    code_entry.focus_set()
    add_window.destroy()


def edit_teacher(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Получение данных выбранной строки из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("SELECT * FROM teachers WHERE code = ?", (code,))
    teacher = c.fetchone()

    # Создание окна для редактирования преподавателя
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить преподавателя")

    # Поля для ввода данных
    code_label = tk.Label(edit_window, text="Код преподавателя:")
    code_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=str(teacher[0])))
    surname_label = tk.Label(edit_window, text="Фамилия:")
    surname_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=teacher[1]))
    name_label = tk.Label(edit_window, text="Имя:")
    name_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=teacher[2]))
    patronymic_label = tk.Label(edit_window, text="Отчество:")
    patronymic_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=teacher[3]))
    subject_label = tk.Label(edit_window, text="Предмет:")
    subject_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=teacher[4]))

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    surname_label.grid(row=1, column=0)
    surname_entry.grid(row=1, column=1)
    name_label.grid(row=2, column=0)
    name_entry.grid(row=2, column=1)
    patronymic_label.grid(row=3, column=0)
    patronymic_entry.grid(row=3, column=1)
    subject_label.grid(row=4, column=0)
    subject_entry.grid(row=4, column=1)

    # Кнопка для сохранения изменений
    save_button = tk.Button(edit_window, text="Изменить", command=lambda: update_teacher(tree, selected, code_entry, surname_entry, name_entry, patronymic_entry, subject_entry, edit_window))
    save_button.grid(row=5, column=0, columnspan=2)

def update_teacher(tree, selected, code_entry, surname_entry, name_entry, patronymic_entry, subject_entry, edit_window):
    # Обновление данных в базе данных
    new_code = int(code_entry.get())
    surname = surname_entry.get()
    name = name_entry.get()
    patronymic = patronymic_entry.get()
    subject = subject_entry.get()
    c.execute("UPDATE teachers SET code = ?, surname = ?, name = ?, patronymic = ?, subject = ? WHERE code = ?",
              (new_code, surname, name, patronymic, subject, int(tree.item(selected, "text"))))
    conn.commit()

    # Обновление таблицы
    tree.item(selected, text=str(new_code), values=[surname, name, patronymic, subject])
    edit_window.destroy()

def delete_teacher(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Удаление преподавателя из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("DELETE FROM teachers WHERE code = ?", (code,))
    conn.commit()

    # Удаление строки из таблицы
    tree.delete(selected)


def show_student_table():
    # Получение данных из базы данных
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    # Создание таблицы студентов
    student_table = tk.Toplevel(root)
    student_table.title("Студенты")

    # Таблица со студентами
    tree = ttk.Treeview(student_table)
    tree["columns"] = ("1", "2", "3", "4")
    tree.column("#0", width=100)
    tree.column("1", width=150)
    tree.column("2", width=150)
    tree.column("3", width=150)
    tree.column("4", width=200)
    tree.heading("#0", text="Код студента")
    tree.heading("1", text="Фамилия")
    tree.heading("2", text="Имя")
    tree.heading("3", text="Отчество")
    tree.heading("4", text="Специальность")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Заполнение таблицы данными
    for student in students:
        tree.insert("", "end", text=str(student[0]), values=student[1:])

    # Кнопки для работы с таблицей
    button_frame = tk.Frame(student_table)
    button_frame.pack(side=tk.BOTTOM)

    add_button = tk.Button(button_frame, text="Добавить", command=lambda: add_student(tree))
    add_button.pack(side=tk.LEFT)

    edit_button = tk.Button(button_frame, text="Изменить", command=lambda: edit_student(tree))
    edit_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_student(tree))
    delete_button.pack(side=tk.LEFT)

def add_student(tree):
    # Создание окна для добавления студента
    add_window = tk.Toplevel(root)
    add_window.title("Добавить студента")

    # Поля для ввода данных
    code_label = tk.Label(add_window, text="Код студента:")
    code_entry = tk.Entry(add_window)
    surname_label = tk.Label(add_window, text="Фамилия:")
    surname_entry = tk.Entry(add_window)
    name_label = tk.Label(add_window, text="Имя:")
    name_entry = tk.Entry(add_window)
    patronymic_label = tk.Label(add_window, text="Отчество:")
    patronymic_entry = tk.Entry(add_window)
    specialty_label = tk.Label(add_window, text="Специальность:")
    specialty_entry = tk.Entry(add_window)

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    surname_label.grid(row=1, column=0)
    surname_entry.grid(row=1, column=1)
    name_label.grid(row=2, column=0)
    name_entry.grid(row=2, column=1)
    patronymic_label.grid(row=3, column=0)
    patronymic_entry.grid(row=3, column=1)
    specialty_label.grid(row=4, column=0)
    specialty_entry.grid(row=4, column=1)
    # Кнопка для добавления студента
    add_button = tk.Button(add_window, text="Добавить",
                           command=lambda: save_student(tree, code_entry, surname_entry, name_entry, patronymic_entry,
                                                        specialty_entry, add_window))
    add_button.grid(row=5, column=0, columnspan=2)


def save_student(tree, code_entry, surname_entry, name_entry, patronymic_entry, specialty_entry, add_window):
    # Добавление студента в базу данных
    code = int(code_entry.get())
    c.execute("SELECT COUNT(*) FROM students WHERE code = ?", (code,))
    count = c.fetchone()[0]
    if count > 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Код студента уже существует.")
        error_label.pack(padx=20, pady=20)
        return
    surname = surname_entry.get()
    name = name_entry.get()
    patronymic = patronymic_entry.get()
    specialty = specialty_entry.get()
    c.execute("INSERT INTO students (code, surname, name, patronymic, specialty) VALUES (?, ?, ?, ?, ?)",
              (code, surname, name, patronymic, specialty))
    conn.commit()

    # Обновление таблицы
    tree.insert("", "end", text=str(code), values=[surname, name, patronymic, specialty])

    # Закрытие окна добавления
    code_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    patronymic_entry.delete(0, tk.END)
    specialty_entry.delete(0, tk.END)
    code_entry.focus_set()
    add_window.destroy()


def edit_student(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Получение данных выбранной строки из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("SELECT * FROM students WHERE code = ?", (code,))
    student = c.fetchone()

    # Создание окна для редактирования студента
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить студента")

    # Поля для ввода данных
    code_label = tk.Label(edit_window, text="Код студента:")
    code_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=str(student[0])))
    surname_label = tk.Label(edit_window, text="Фамилия:")
    surname_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=student[1]))
    name_label = tk.Label(edit_window, text="Имя:")
    name_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=student[2]))
    patronymic_label = tk.Label(edit_window, text="Отчество:")
    patronymic_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=student[3]))
    specialty_label = tk.Label(edit_window, text="Специальность:")
    specialty_entry = tk.Entry(edit_window, textvariable=tk.StringVar(value=student[4]))

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    surname_label.grid(row=1, column=0)
    surname_entry.grid(row=1, column=1)
    name_label.grid(row=2, column=0)
    name_entry.grid(row=2, column=1)
    patronymic_label.grid(row=3, column=0)
    patronymic_entry.grid(row=3, column=1)
    specialty_label.grid(row=4, column=0)
    specialty_entry.grid(row=4, column=1)

    # Кнопка для сохранения изменений
    save_button = tk.Button(edit_window, text="Изменить",
                            command=lambda: update_student(tree, selected, code_entry, surname_entry, name_entry,
                                                           patronymic_entry, specialty_entry, edit_window))
    save_button.grid(row=5, column=0, columnspan=2)


def update_student(tree, selected, code_entry, surname_entry, name_entry, patronymic_entry, specialty_entry,
                   edit_window):
    # Обновление данных в базе данных
    new_code = int(code_entry.get())
    surname = surname_entry.get()
    name = name_entry.get()
    patronymic = patronymic_entry.get()
    specialty = specialty_entry.get()
    c.execute("UPDATE students SET code = ?, surname = ?, name = ?, patronymic = ?, specialty = ? WHERE code = ?",
              (new_code, surname, name, patronymic, specialty, int(tree.item(selected, "text"))))
    conn.commit()

    # Обновление таблицы
    tree.item(selected, text=str(new_code), values=[surname, name, patronymic, specialty])
    edit_window.destroy()

def delete_student(tree):
        # Получение выбранной строки
        selected = tree.focus()
        if not selected:
            return

        # Удаление студента из базы данных
        code = int(tree.item(selected, "text"))
        c.execute("DELETE FROM students WHERE code = ?", (code,))
        conn.commit()

        # Удаление строки из таблицы
        tree.delete(selected)



def show_exam_table():
    # Получение данных из базы данных
    c.execute("SELECT e.code, e.department_code, e.exam_date, e.exam_time, e.teacher_code "
              "FROM exams e "
              "JOIN teachers t ON e.teacher_code = t.code")
    exams = c.fetchall()

    # Создание таблицы экзаменов
    exam_table = tk.Toplevel(root)
    exam_table.title("Экзамены")

    # Таблица с экзаменами
    tree = ttk.Treeview(exam_table)
    tree["columns"] = ("1", "2", "3", "4")
    tree.column("#0", width=100)
    tree.column("1", width=150)
    tree.column("2", width=150)
    tree.column("3", width=150)
    tree.column("4", width=150)
    tree.heading("#0", text="Код")
    tree.heading("1", text="Код кафедры")
    tree.heading("2", text="Дата")
    tree.heading("3", text="Время")
    tree.heading("4", text="Код преподавателя")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Заполнение таблицы данными
    for exam in exams:
        tree.insert("", "end", text=str(exam[0]), values=exam[1:])

    # Кнопки для работы с таблицей
    button_frame = tk.Frame(exam_table)
    button_frame.pack(side=tk.BOTTOM)

    add_button = tk.Button(button_frame, text="Добавить", command=lambda: add_exam(tree))
    add_button.pack(side=tk.LEFT)

    edit_button = tk.Button(button_frame, text="Изменить", command=lambda: edit_exam(tree))
    edit_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_exam(tree))
    delete_button.pack(side=tk.LEFT)

def add_exam(tree):
    # Создание окна для добавления экзамена
    add_window = tk.Toplevel(root)
    add_window.title("Добавить экзамен")

    # Поля для ввода данных
    code_label = tk.Label(add_window, text="Код:")
    code_entry = tk.Entry(add_window)
    department_code_label = tk.Label(add_window, text="Код кафедры:")
    department_code_entry = tk.Entry(add_window)
    exam_date_label = tk.Label(add_window, text="Дата:")
    exam_date_entry = tk.Entry(add_window)
    exam_time_label = tk.Label(add_window, text="Время:")
    exam_time_entry = tk.Entry(add_window)
    teacher_code_label = tk.Label(add_window, text="Код преподавателя:")
    teacher_code_entry = tk.Entry(add_window)

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    department_code_label.grid(row=1, column=0)
    department_code_entry.grid(row=1, column=1)
    exam_date_label.grid(row=2, column=0)
    exam_date_entry.grid(row=2, column=1)
    exam_time_label.grid(row=3, column=0)
    exam_time_entry.grid(row=3, column=1)
    teacher_code_label.grid(row=4, column=0)
    teacher_code_entry.grid(row=4, column=1)

    # Кнопка для добавления экзамена
    add_button = tk.Button(add_window, text="Добавить",
                           command=lambda: save_exam(tree, code_entry, department_code_entry, exam_date_entry,
                                                     exam_time_entry, teacher_code_entry, add_window))
    add_button.grid(row=5, column=0, columnspan=2)


def save_exam(tree, code_entry, department_code_entry, exam_date_entry, exam_time_entry, teacher_code_entry,
              add_window):
    # Проверка формата даты и времени
    try:
        date_parts = exam_date_entry.get().split('.')
        if len(date_parts) != 3 or len(date_parts[0]) != 2 or len(date_parts[1]) != 2 or len(date_parts[2]) != 4:
            raise ValueError("Неправильный формат даты. Используйте формат ДД.ММ.ГГГГ.")
        time_parts = exam_time_entry.get().split(':')
        if len(time_parts) != 2 or len(time_parts[0]) != 2 or len(time_parts[1]) != 2:
            raise ValueError("Неправильный формат времени. Используйте формат ЧЧ:ММ.")
    except ValueError as e:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text=str(e))
        error_label.pack(padx=20, pady=20)
        return

    # Проверка существования кода кафедры и преподавателя
    department_code = int(department_code_entry.get())
    c.execute("SELECT COUNT(*) FROM departments WHERE code = ?", (department_code,))
    count = c.fetchone()[0]
    if count > 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Код экзамена уже существует.")
        error_label.pack(padx=20, pady=20)
        return


    department_count = c.fetchone()[0]
    teacher_code = int(teacher_code_entry.get())
    c.execute("SELECT COUNT(*) FROM teachers WHERE code = ?", (teacher_code,))
    teacher_count = c.fetchone()[0]

    if department_count == 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Указанный код кафедры не существует.")
        error_label.pack(padx=20, pady=20)
        return
    if teacher_count == 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Указанный код преподавателя не существует.")
        error_label.pack(padx=20, pady=20)
        return

    # Добавление экзамена в базу данных
    code = int(code_entry.get())
    exam_date = exam_date_entry.get()
    exam_time = exam_time_entry.get()
    c.execute("INSERT INTO exams (code, department_code, exam_date, exam_time, teacher_code) VALUES (?, ?, ?, ?, ?)",
              (code, department_code, exam_date, exam_time, teacher_code))
    conn.commit()

    # Обновление таблицы
    c.execute("SELECT e.department_code, e.exam_date, e.exam_time, e.teacher_code "
              "FROM exams e "
              "WHERE e.code = ?", (code,))
    exam_data = c.fetchone()
    tree.insert("", "end", text=str(code), values=exam_data)

    # Закрытие окна добавления
    code_entry.delete(0, tk.END)
    department_code_entry.delete(0, tk.END)
    exam_date_entry.delete(0, tk.END)
    exam_time_entry.delete(0, tk.END)
    teacher_code_entry.delete(0, tk.END)
    code_entry.focus_set()
    add_window.destroy()

def edit_exam(tree):
    # Получение выбранной записи
    selected_item = tree.focus()
    if selected_item:
        # Получение данных выбранной записи
        values = tree.item(selected_item, 'values')
        code = int(tree.item(selected_item, 'text'))
        department_code = int(values[0])
        exam_date = values[1]
        exam_time = values[2]
        teacher_code = int(values[3])

        # Создание окна для редактирования экзамена
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать экзамен")

        # Поля для ввода данных
        code_label = tk.Label(edit_window, text="Код:")
        code_entry = tk.Entry(edit_window)
        department_code_label = tk.Label(edit_window, text="Код кафедры:")
        department_code_entry = tk.Entry(edit_window)
        exam_date_label = tk.Label(edit_window, text="Дата:")
        exam_date_entry = tk.Entry(edit_window)
        exam_time_label = tk.Label(edit_window, text="Время:")
        exam_time_entry = tk.Entry(edit_window)
        teacher_code_label = tk.Label(edit_window, text="Код преподавателя:")
        teacher_code_entry = tk.Entry(edit_window)

        # Заполнение полей данными
        code_entry.insert(0, str(code))
        department_code_entry.insert(0, str(department_code))
        exam_date_entry.insert(0, exam_date)
        exam_time_entry.insert(0, exam_time)
        teacher_code_entry.insert(0, str(teacher_code))

        code_label.grid(row=0, column=0)
        code_entry.grid(row=0, column=1)
        department_code_label.grid(row=1, column=0)
        department_code_entry.grid(row=1, column=1)
        exam_date_label.grid(row=2, column=0)
        exam_date_entry.grid(row=2, column=1)
        exam_time_label.grid(row=3, column=0)
        exam_time_entry.grid(row=3, column=1)
        teacher_code_label.grid(row=4, column=0)
        teacher_code_entry.grid(row=4, column=1)

        # Кнопка для обновления экзамена
        update_button = tk.Button(edit_window, text="Сохранить",
                                  command=lambda: update_exam(tree, selected_item, code_entry, department_code_entry,
                                                              exam_date_entry, exam_time_entry, teacher_code_entry,
                                                              edit_window))
        update_button.grid(row=5, column=0, columnspan=2)

def update_exam(tree, selected, code_entry, department_code_entry, exam_date_entry, exam_time_entry,
                    teacher_code_entry, edit_window):
        # Проверка формата даты и времени
        try:
            date_parts = exam_date_entry.get().split('.')
            if len(date_parts) != 3 or len(date_parts[0]) != 2 or len(date_parts[1]) != 2 or len(date_parts[2]) != 4:
                raise ValueError("Неправильный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            time_parts = exam_time_entry.get().split(':')
            if len(time_parts) != 2 or len(time_parts[0]) != 2 or len(time_parts[1]) != 2:
                raise ValueError("Неправильный формат времени. Используйте формат ЧЧ:ММ.")
        except ValueError as e:
            error_window = tk.Toplevel(edit_window)
            error_window.title("Ошибка")
            error_label = tk.Label(error_window, text=str(e))
            error_label.pack(padx=20, pady=20)
            return

        # Проверка существования кода кафедры и преподавателя
        department_code = int(department_code_entry.get())
        c.execute("SELECT COUNT(*) FROM departments WHERE code = ?", (department_code,))
        department_count = c.fetchone()[0]
        teacher_code = int(teacher_code_entry.get())
        c.execute("SELECT COUNT(*) FROM teachers WHERE code = ?", (teacher_code,))
        teacher_count = c.fetchone()[0]

        if department_count == 0:
            error_window = tk.Toplevel(edit_window)
            error_window.title("Ошибка")
            error_label = tk.Label(error_window, text="Указанный код кафедры не существует.")
            error_label.pack(padx=20, pady=20)
            return
        if teacher_count == 0:
            error_window = tk.Toplevel(edit_window)
            error_window.title("Ошибка")
            error_label = tk.Label(error_window, text="Указанный код преподавателя не существует.")
            error_label.pack(padx=20, pady=20)
            return

            # Обновление экзамена в базе данных
        code = int(code_entry.get())
        exam_date = exam_date_entry.get()
        exam_time = exam_time_entry.get()
        c.execute("UPDATE exams SET department_code = ?, exam_date = ?, exam_time = ?, teacher_code = ? WHERE code = ?",
                  (department_code, exam_date, exam_time, teacher_code, code))
        conn.commit()

        # Обновление данных в таблице
        c.execute("SELECT e.department_code, e.exam_date, e.exam_time, e.teacher_code "
                  "FROM exams e "
                  "WHERE e.code = ?", (code,))
        exam_data




def delete_exam(tree):
    # Получение выбранной строки
    selected = tree.focus()
    if not selected:
        return

    # Удаление экзамена из базы данных
    code = int(tree.item(selected, "text"))
    c.execute("DELETE FROM exams WHERE code = ?", (code,))
    conn.commit()

    # Удаление строки из таблицы
    tree.delete(selected)


def show_schedule_table():
    # Получение данных из базы данных
    c.execute("SELECT s.code, s.subject, s.schedule_date, s.schedule_time, s.teacher_code "
              "FROM schedule s "
              "JOIN teachers t ON s.teacher_code = t.code")
    schedules = c.fetchall()

    # Создание таблицы расписания
    global schedule_tree
    schedule_table = tk.Toplevel(root)
    schedule_table.title("Расписание")

    # Таблица с расписанием
    tree = ttk.Treeview(schedule_table)
    tree["columns"] = ("1", "2", "3", "4")
    tree.column("#0", width=100)
    tree.column("1", width=200)
    tree.column("2", width=150)
    tree.column("3", width=150)
    tree.column("4", width=150)
    tree.heading("#0", text="Код")
    tree.heading("1", text="Предмет")
    tree.heading("2", text="Дата")
    tree.heading("3", text="Время")
    tree.heading("4", text="Код преподавателя")
    tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Заполнение таблицы данными
    for schedule in schedules:
        tree.insert("", "end", text=str(schedule[0]), values=schedule[1:])

    # Кнопки для работы с таблицей
    button_frame = tk.Frame(schedule_table)
    button_frame.pack(side=tk.BOTTOM)

    add_button = tk.Button(button_frame, text="Добавить", command=lambda: add_schedule(tree))
    add_button.pack(side=tk.LEFT)

    edit_button = tk.Button(button_frame, text="Изменить", command=lambda: edit_schedule(tree))
    edit_button.pack(side=tk.LEFT)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_schedule(tree))
    delete_button.pack(side=tk.LEFT)



def add_schedule(tree):
    # Создание окна для добавления расписания
    add_window = tk.Toplevel(root)
    add_window.title("Добавить расписание")

    # Поля для ввода данных
    code_label = tk.Label(add_window, text="Код:")
    code_entry = tk.Entry(add_window)
    subject_label = tk.Label(add_window, text="Предмет:")
    subject_entry = tk.Entry(add_window)
    schedule_date_label = tk.Label(add_window, text="Дата:")
    schedule_date_entry = tk.Entry(add_window)
    schedule_time_label = tk.Label(add_window, text="Время:")
    schedule_time_entry = tk.Entry(add_window)
    teacher_code_label = tk.Label(add_window, text="Код преподавателя:")
    teacher_code_entry = tk.Entry(add_window)

    code_label.grid(row=0, column=0)
    code_entry.grid(row=0, column=1)
    subject_label.grid(row=1, column=0)
    subject_entry.grid(row=1, column=1)
    schedule_date_label.grid(row=2, column=0)
    schedule_date_entry.grid(row=2, column=1)
    schedule_time_label.grid(row=3, column=0)
    schedule_time_entry.grid(row=3, column=1)
    teacher_code_label.grid(row=4, column=0)
    teacher_code_entry.grid(row=4, column=1)

    # Кнопка для добавления расписания
    add_button = tk.Button(add_window, text="Добавить",
                           command=lambda: save_schedule(tree, code_entry, subject_entry, schedule_date_entry,
                                                         schedule_time_entry, teacher_code_entry, add_window))
    add_button.grid(row=5, column=0, columnspan=2)

def save_schedule(tree, code_entry, subject_entry, schedule_date_entry, schedule_time_entry, teacher_code_entry, add_window):
    # Проверка формата даты и времени
    try:
        date_parts = schedule_date_entry.get().split('.')
        if len(date_parts) != 3 or len(date_parts[0]) != 2 or len(date_parts[1]) != 2 or len(date_parts[2]) != 4:
            raise ValueError("Неправильный формат даты. Используйте формат ДД.ММ.ГГГГ.")
        time_parts = schedule_time_entry.get().split(':')
        if len(time_parts) != 2 or len(time_parts[0]) != 2 or len(time_parts[1]) != 2:
            raise ValueError("Неправильный формат времени. Используйте формат ЧЧ:ММ.")
    except ValueError as e:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text=str(e))
        error_label.pack(padx=20, pady=20)
        return

    # Проверка существования кода преподавателя
    teacher_code = int(teacher_code_entry.get())
    c.execute("SELECT COUNT(*) FROM teachers WHERE code = ?", (teacher_code,))

    teacher_count = c.fetchone()[0]

    if teacher_count == 0:
        error_window = tk.Toplevel(add_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Указанный код преподавателя не существует.")
        error_label.pack(padx=20, pady=20)
        return

    # Добавление расписания в базу данных
    code = int(code_entry.get())
    subject = subject_entry.get()
    schedule_date = schedule_date_entry.get()
    schedule_time = schedule_time_entry.get()
    c.execute("INSERT INTO schedule (code, subject, schedule_date, schedule_time, teacher_code) VALUES (?, ?, ?, ?, ?)",
              (code, subject, schedule_date, schedule_time, teacher_code))
    conn.commit()

    # Обновление таблицы
    c.execute("SELECT s.subject, s.schedule_date, s.schedule_time, s.teacher_code "
              "FROM schedule s "
              "WHERE s.code = ?", (code,))
    schedule_data = c.fetchone()
    tree.insert("", "end", text=str(code), values=schedule_data)

    # Закрытие окна добавления
    code_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    schedule_date_entry.delete(0, tk.END)
    schedule_time_entry.delete(0, tk.END)
    teacher_code_entry.delete(0, tk.END)
    code_entry.focus_set()
    add_window.destroy()

def edit_schedule(tree):
    # Получение выбранной записи
    selected_item = tree.focus()
    if selected_item:
        # Получение данных выбранной записи
        values = tree.item(selected_item, 'values')
        code = int(tree.item(selected_item, 'text'))
        subject = values[0]
        schedule_date = values[1]
        schedule_time = values[2]
        teacher_code = int(values[3])

        # Создание окна для редактирования расписания
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактировать расписание")

        # Поля для ввода данных
        code_label = tk.Label(edit_window, text="Код:")
        code_entry = tk.Entry(edit_window)
        subject_label = tk.Label(edit_window, text="Предмет:")
        subject_entry = tk.Entry(edit_window)
        schedule_date_label = tk.Label(edit_window, text="Дата:")
        schedule_date_entry = tk.Entry(edit_window)
        schedule_time_label = tk.Label(edit_window, text="Время:")
        schedule_time_entry = tk.Entry(edit_window)
        teacher_code_label = tk.Label(edit_window, text="Код преподавателя:")
        teacher_code_entry = tk.Entry(edit_window)

        # Заполнение полей данными
        code_entry.insert(0, str(code))
        subject_entry.insert(0, subject)
        schedule_date_entry.insert(0, schedule_date)
        schedule_time_entry.insert(0, schedule_time)
        teacher_code_entry.insert(0, str(teacher_code))

        code_label.grid(row=0, column=0)
        code_entry.grid(row=0, column=1)
        subject_label.grid(row=1, column=0)
        subject_entry.grid(row=1, column=1)
        schedule_date_label.grid(row=2, column=0)
        schedule_date_entry.grid(row=2, column=1)
        schedule_time_label.grid(row=3, column=0)
        schedule_time_entry.grid(row=3, column=1)
        teacher_code_label.grid(row=4, column=0)
        teacher_code_entry.grid(row=4, column=1)

        # Кнопка для обновления расписания
        update_button = tk.Button(edit_window, text="Сохранить",
                                  command=lambda: update_schedule(tree, selected_item, code_entry, subject_entry, schedule_date_entry, schedule_time_entry, teacher_code_entry, edit_window))
        update_button.grid(row=5, column=0, columnspan=2)

def update_schedule(tree, selected, code_entry, subject_entry, schedule_date_entry, schedule_time_entry, teacher_code_entry, edit_window):
    # Проверка формата даты и времени
    try:
        date_parts = schedule_date_entry.get().split('.')
        if len(date_parts) != 3 or len(date_parts[0]) != 2 or len(date_parts[1]) != 2 or len(date_parts[2]) != 4:
            raise ValueError("Неправильный формат даты. Используйте формат ДД.ММ.ГГГГ.")
        time_parts = schedule_time_entry.get().split(':')
        if len(time_parts) != 2 or len(time_parts[0]) != 2 or len(time_parts[1]) != 2:
            raise ValueError("Неправильный формат времени. Используйте формат ЧЧ:ММ.")
    except ValueError as e:
        error_window = tk.Toplevel(edit_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text=str(e))
        error_label.pack(padx=20, pady=20)
        return

    # Проверка существования кода преподавателя
    teacher_code = int(teacher_code_entry.get())
    c.execute("SELECT COUNT(*) FROM teachers WHERE code = ?", (teacher_code,))
    teacher_count = c.fetchone()[0]

    if teacher_count == 0:
        error_window = tk.Toplevel(edit_window)
        error_window.title("Ошибка")
        error_label = tk.Label(error_window, text="Указанный код преподавателя не существует.")
        error_label.pack(padx=20, pady=20)
        return

        # Обновление расписания в базе данных
    code = int(code_entry.get())
    subject = subject_entry.get()
    schedule_date = schedule_date_entry.get()
    schedule_time = schedule_time_entry.get()
    c.execute("UPDATE schedule SET subject = ?, schedule_date = ?, schedule_time = ?, teacher_code = ? WHERE code = ?",
              (subject, schedule_date, schedule_time, teacher_code, code))
    conn.commit()

    # Обновление данных в таблице
    tree.item(selected, text=str(code), values=(subject, schedule_date, schedule_time, str(teacher_code)))

    # Закрытие окна редактирования
    edit_window.destroy()


def delete_schedule(tree):
    # Получение выбранной записи
    selected_item = tree.focus()
    if selected_item:
        # Получение кода выбранной записи
        code = int(tree.item(selected_item, 'text'))

        # Удаление записи из базы данных
        c.execute("DELETE FROM schedule WHERE code = ?", (code,))
        conn.commit()

        # Удаление записи из таблицы
        tree.delete(selected_item)





# Основное окно
root = tk.Tk()
root.title("Университетская система")

# Кнопка для открытия таблицы кафедр

department_button = tk.Button(root, text="Кафедра", command=show_department_table)
department_button.pack(side=tk.TOP)


teacher_button = tk.Button(root, text="Преподаватель", command=show_teacher_table)
teacher_button.pack(side=tk.TOP)


student_button = tk.Button(root, text="Студент", command=show_student_table)
student_button.pack(side=tk.TOP)


exam_button = tk.Button(root, text="Экзамен", command=show_exam_table)
exam_button.pack(side=tk.TOP)


schedule_button = tk.Button(root, text="Расписание", command=show_schedule_table)
schedule_button.pack(side=tk.TOP)



root.mainloop()

# Закрытие соединения с базой данных
conn.close()
