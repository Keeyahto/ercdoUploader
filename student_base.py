from datetime import datetime



class Module:
    header: str
    int_total_rate: int
    str_total_rate: str
    @property
    def total_rate(self):
        if not self.int_total_rate or not self.str_total_rate:
            print(f'У студента остутствует int_total_rate или str_total_rate')
            return ''
        return self.pipe_join((self.int_total_rate, self.str_total_rate))

    @property
    def submodules(self):
        if not self._submodules:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует _submodules')
            return ''
        return self._submodules

    @submodules.setter
    def submodules(self, x):
        if not hasattr(self, '_submodules') or self._submodules is None:
            self._submodules = {}
        self._submodules[x[0]] = self.pipe_join((x[1], x[2]))

    def get_module_header(self):
        header = [self.header + '+в том числе:']
        for submodule_name in self.submodules.keys():
            header.append(self.header + "|" + submodule_name)
        return header
    def get_module_row(self):
        data = {self.header + ' | ' + '+в том числе:': self.total_rate}
        for submodule_name, value in self.submodules.items():
            data[self.header + " | " + submodule_name] = value
        return data

    def pipe_join(self, lst):
        return ' | '.join(list(map(lambda x: str(x), lst)))



class Student:
    spoId: int
    name: str
    "SpoDocuments.fio2, Имя"
    surname: str
    "SpoDocuments.fio1, Фамилия"
    middle_name: str
    "SpoDocuments.fio3, Отчество"
    @property
    def birth_date(self):
        if not self._birth_date:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует дата рождения')
            return ''
        return self._birth_date.strftime('%d.%m.%Y')
    @birth_date.setter
    def birth_date(self, date_str):
        self._birth_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    graduate_year: int
    "Формируется на основе issueDate, Год окончания"

    specialty_code: str
    "SpoDocuments professionCode, Код специальности"
    profession: str
    'SpoDocuments professionName'
    @property
    def issue_date(self):
        if not self._issue_date:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует дата выдачи диплома')
            return ''
        return self._issue_date.strftime('%d.%m.%Y')
    @issue_date.setter
    def issue_date(self, date_str):
        self._issue_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        self.graduate_year = self._issue_date.year

    qualify: str
    "SpoDocuments qual, Квалификация"

    gender: str = ''

    SNILS: str = ''

    EPGU: str = 'ДА'

    citizenship: str = 'RU'

    by_blank: str = 'да'

    document_issuance: str = ''

    admission_basis: str = ''

    email: str = ''

    exam_commission: str = ''

    previous_document: str
    "SpoDocuments previousEducation, Предыдущий документ"

    @property
    def document_type(self):
        if not self._document_type:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует вид документа (is_excellent не указан, используеться значение по умолчанию)')
            return ''
        return self._document_type
    @document_type.setter
    def document_type(self, is_excellent):
        self._document_type = 'с отличием' if is_excellent else ''

    @property
    def decision_date(self):
        if not self._decision_date:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует дата Решения Государственной экзаменационной комиссии')
            return ''
        return 'от ' + self._decision_date.strftime('%d.%m.%Y')
    @decision_date.setter
    def decision_date(self, date_str):
        self._decision_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    study_duration: str
    "SpoDocuments totalCount"


    @property
    def teoretical_study_duration(self):
        if not self._teoretical_study_duration:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует ВСЕГО часов теоретического обучения  customTotalCount')
            return ''
        t = f'{self._teoretical_study_duration} час.'
        lst = [t, 'x']
        return self.pipe_join(lst)

    @teoretical_study_duration.setter
    def teoretical_study_duration(self, x):
        self._teoretical_study_duration = x

    @property
    def auditor_study_duration(self):
        if not self._auditor_study_duration:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует часов аудиторных обучения  customAuditCount')
            return ''
        t = f'{self._auditor_study_duration} час.'
        lst = [t, 'x']
        return self.pipe_join(lst)

    @auditor_study_duration.setter
    def auditor_study_duration(self, x):
        self._auditor_study_duration = x

    @property
    def practice_study_duration(self):
        if not self._practice_study_duration:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует practiceTotalCount')
            return ''
        t = f'{self._practice_study_duration} час.'
        lst = [t, 'x']
        return self.pipe_join(lst)

    @practice_study_duration.setter
    def practice_study_duration(self, x):
        self._practice_study_duration = x


    @property
    def attestation_total_count(self):
        if not self._attestation_total_count:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует attestation_total_count')
            return ''
        lst = [self._attestation_total_count, 'x']
        return self.pipe_join(lst)

    @attestation_total_count.setter
    def attestation_total_count(self, x):
        self._attestation_total_count = x

    @property
    def discipline_details(self):
        if not self._discipline_details:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует _disipline_details')
            return ''
        return self._discipline_details

    @discipline_details.setter
    def discipline_details(self, x):
        if not hasattr(self, '_discipline_details') or self._discipline_details is None:
            self._discipline_details = {}
        self._discipline_details[x[0]] = self.pipe_join((x[1], x[2]))

    module_details: list[Module] = []


    @property
    def practice_details(self):
        if not self._practice_details:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует _practice_details')
            return ''
        return self._practice_details

    @practice_details.setter
    def practice_details(self, x):
        if not hasattr(self, '_practice_details') or self.practice_details is None:
            self._practice_details = {}
        self._practice_details[x[0]] = self.pipe_join((x[1], x[2]))

    @property
    def attestation_details(self):
        if not self._attestation_details:
            print(f'У студента {self.name} {self.surname} {self.middle_name} остутствует _attestation_details')
            return ''
        return self._attestation_details

    @attestation_details.setter
    def attestation_details(self, x):
        if not hasattr(self, '_attestation_details') or self._attestation_details is None:
            self._attestation_details = []
        self._attestation_details.append(self.pipe_join((x[0], x[1], 'x')))

    course_works_details: dict = {}


    def pipe_join(self, lst):
        return ' | '.join(list(map(lambda x: str(x), lst)))
