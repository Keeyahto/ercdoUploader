import sqlite3
from datetime import datetime

import openpyxl
import pandas as pd

from student_base import Student, Module


class StudentsExtractor:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.students = []

    def extract_students(self):
        self.cursor.execute(
            "SELECT fio1, fio2, fio3, birthDate, professionCode, professionName, issueDate, qual, "
            " previousEducation, isExcellent, decisionDate, totalCount, customTotalCount, customAuditCount, practiceTotalCount, attestationTotalCount, spoID "
            " FROM SpoDocuments WHERE isTemplate != 1 AND isDuplicate != 1;")
        students_rows = self.cursor.fetchall()
        for row in students_rows:
            current_student = Student()
            row = list(row)
            current_student.surname = row[0]
            current_student.name = row[1]
            current_student.middle_name = row[2]
            current_student.birth_date = row[3]
            current_student.specialty_code = row[4]
            current_student.profession = row[5]
            current_student.issue_date = row[6]
            current_student.qualify = row[7]
            current_student.previous_document = row[8]
            current_student.document_type = row[9]
            current_student.decision_date = row[10]
            current_student.study_duration = row[11]
            current_student.teoretical_study_duration = row[12]
            current_student.auditor_study_duration = row[13]
            current_student.practice_study_duration = row[14]
            current_student.attestation_total_count = row[15]
            current_student.spoId = row[16]
            self.extract_disciplines(current_student)
            self.extract_modules(current_student)
            self.extract_practices(current_student)
            self.students.append(current_student)

    def extract_disciplines(self, current_student):
        query = "SELECT disciplineName, disciplineCount, disciplineRate FROM DisciplineDetails WHERE spoID = ?"
        self.cursor.execute(query, (current_student.spoId,))
        discipline_details = self.cursor.fetchall()
        for details in discipline_details:
            details = list(details)
            current_student.discipline_details = details

    def extract_modules(self, current_student):
        query = 'SELECT moduleName, moduleCount, moduleRate, moduleID FROM ModuleDetails WHERE spoID = ?'
        self.cursor.execute(query, (current_student.spoId,))
        modules_details = self.cursor.fetchall()
        for details in modules_details:
            details = list(details)
            module = Module()
            module.header = details[0]
            module.int_total_rate = details[1]
            module.str_total_rate = details[2]
            query = 'SELECT dmName, dmCount, dmRate FROM DMDetails WHERE moduleID = ? AND spoID = ?'
            self.cursor.execute(query, (details[3], current_student.spoId))
            submodules_details = self.cursor.fetchall()
            for submodule_details in submodules_details:
                submodule_details = list(submodule_details)
                module.submodules = submodule_details
            current_student.module_details.append(module)

    def extract_practices(self, current_student):
        query = "SELECT practiceName, practiceCount, practiceRate FROM PracticeDetails WHERE spoID = ?"
        self.cursor.execute(query, (current_student.spoId,))
        practices_details = self.cursor.fetchall()
        for details in practices_details:
            details = list(details)
            current_student.practice_details = details

    def run(self):
        self.extract_students()
        self.process_students()
        self.finish()

    def finish(self):
        self.connection.close()

    def process_students(self):
        while self.students:
            current_specialty_code = self.students[0].specialty_code
            current_students = [student for student in self.students if student.specialty_code == current_specialty_code]
            self.export_students(current_students)
            self.students = [student for student in self.students if student not in current_students]

    def export_students(self, students: list[Student]):


        header1 = ['Срок освоения образовательной программы по очной форме обучения',
                           'ВСЕГО часов теоретического обучения,', 'в том числе аудиторных часов:',
                           'Практики', 'Государственная итоговая аттестация']

        writer = pd.ExcelWriter(f"{students[0].specialty_code}.xlsx", engine='openpyxl')
        wb = writer.book
        df = pd.DataFrame({'ФАМИЛИЯ': [x.surname for x in students],
                           'ИМЯ': [x.name for x in students],
                           'ОТЧЕСТВО': [x.middle_name for x in students],
                           'ДАТА РОЖДЕНИЯ': [x.birth_date for x in students],
                           'ГОД ОКОНЧАНИЯ': [x.graduate_year for x in students],
                           'КОД СПЕЦИАЛЬНОСТИ': [x.specialty_code for x in students],
                           'СПЕЦИАЛЬНОСТЬ': [x.profession for x in students],
                           'ДАТА ВЫДАЧИ': [x.issue_date for x in students],
                           'Квалификация': [x.qualify for x in students],
                           'ПОЛ': ['' for x in students],
                           'СНИЛС': ['' for x in students],
                           'НА ЕПГУ': ['ДА' for x in students],
                           'Гражданство': ['RU' for x in students],
                           'На бланке': ['да' for x in students],
                           'Основание выдачи документа': ['' for x in students],
                           'Основание приема на обучение': ['' for x in students],
                           'Адрес электронной почты (email)': ['' for x in students],
                           'Председатель Государственной экзаменационной комиссии': ['' for x in students],
                           'Предыдущий документ об образовании или об образовании и о квалификации': [x.previous_document for x in students],
                           'Вид документа': [x.document_type for x in students],
                           'Решение Государственной экзаменационной комиссии': [x.decision_date for x in students],
                          })
        self.set_disciplines(students, df)
        df['ВСЕГО часов теоретического обучения,'] = [x.teoretical_study_duration for x in students]
        df['в том числе аудиторных часов:'] = [x.auditor_study_duration for x in students]
        df = self.set_modules(students, df)
        self.set_practices(students, df)
        df.to_excel(writer, index=False)
        wb.save(f"{students[0].specialty_code}.xlsx")


    def set_disciplines(self, students, df):
        disciplines_dicts = [student.discipline_details for student in students]
        # Извлекаем ключи всех словарей в массив
        list_of_disciplines = []
        for d in disciplines_dicts:
            list_of_disciplines.extend(d.keys())

        # Делаем массив уникальных ключей
        disciplines_header = list(set(list_of_disciplines))

        for discipline in disciplines_header:
            df[discipline] = [disciplines_dict.get(discipline, '') for disciplines_dict in disciplines_dicts]

    def set_modules(self, students, df):
        students_modules = [student.module_details for student in students]  # list[Module]
        data = []
        for student_modules in students_modules:
            student_row = {}
            for module in student_modules:
                student_row.update(module.get_module_row())
            data.append(student_row)
        new_data = pd.DataFrame(data)

        return pd.concat([df, new_data], axis=1)

    def set_practices(self, students, df):
        practices_dicts = [student.practice_details for student in students]
        # Извлекаем ключи всех словарей в массив
        list_of_practices = []
        for d in practices_dicts:
            list_of_practices.extend(d.keys())

        # Делаем массив уникальных ключей
        practices_header = list(set(list_of_practices))
        df['Практика +в том числе:'] = [student.practice_study_duration for student in students]
        for practice in practices_header:
            df['Практика' + practice] = [practice_dict.get(practice, '') for practice_dict in practices_dicts]



if __name__ == "__main__":
    db_name = "KtSpo-backup-2023-09-19.db"  # Замените на имя вашей базы данных
    extractor = StudentsExtractor(db_name)
    extractor.run()



