import sqlite3
from datetime import datetime

import openpyxl

from datetime import datetime

def convert_date(date_str):
    # Конвертация строки с датой в формат datetime
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def export_to_excel(database_path, excel_path):
    # Подключение к базе данных SQLite
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Выборка данных из базы данных
    cursor.execute("SELECT fio1, fio2, fio3, birthDate, professionCode, professionName, issueDate, qual, previousEducation, customTotalCount, customAuditCount, practiceTotalCount, attestationTotalCount FROM SpoDocuments WHERE isTemplate != 1 AND isDuplicate != 1;")
    data = cursor.fetchall()

    # Создание нового Excel-файла
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Заголовки столбцов
    sheet.append(['ФАМИЛИЯ', 'ИМЯ', 'ОТЧЕСТВО', 'ДАТА РОЖДЕНИЯ', 'ГОД ОКОНЧАНИЯ', 'КОД СПЕЦИАЛЬНОСТИ', 'СПЕЦИАЛЬНОСТЬ', 'ДАТА ВЫДАЧИ', 'Квалификация', 'Предыдущий документ об образовании или об образовании и о квалификации', 'ВСЕГО часов теоретического обучения,', 'в том числе аудиторных часов:', 'Практики', 'Государственная итоговая аттестация'])

    # Заполнение данными
    for row in data:
        row = list(row)
        row[3] = convert_date(row[3]).strftime('%d.%m.%Y')
        row.insert(4, convert_date(row[6]).year)
        row[7] = convert_date(row[7]).strftime('%d.%m.%Y')
        sheet.append(row)
        print(row)

    # Сохранение Excel-файла
    workbook.save(excel_path)

    # Закрытие соединения с базой данных
    connection.close()

if __name__ == "__main__":
    # Путь к базе данных SQLite
    database_path = "KtSpo-backup-2023-09-19.db"

    # Путь к Excel-файлу для экспорта
    excel_path = "output.xlsx"

    # Вызов функции экспорта
    export_to_excel(database_path, excel_path)
