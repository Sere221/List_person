from django import forms

WORKING_POSITION = (
    ('', 'Любой'),
    ('Employee', 'Сотрудник'),
    ('Senior', 'Старший сотрудник'),
    ('Master', 'Мастер'),
    ('Director', 'Директор'),
    ('Admin', 'Администратор')
)

FILIAL = (
    ('', 'Любой'),
    ('Moscow', 'Москва'),
    ('Smolensk', 'Смоленск'),
    ('Petersburg', 'Санкт-Петербург'),
    ('Novgorod', 'Нижний Новгород'),
    ('Kaliningrad', 'Калининград')
)

DEPARTMENT = (
    ('', 'Любой'),
    ('Designer', 'Дизайнер'),
    ('Backend', 'Серевная'),
    ('Developers', 'Разработчики'),
    ('Researchers', 'Исследователи')
)


class ProfileSearchForm(forms.Form):
    query = forms.CharField(label='ФИО', max_length=100)
    filial = forms.ChoiceField(choices=FILIAL, required=False, label='Филиал')
    account_type = forms.ChoiceField(choices=WORKING_POSITION, required=False, label='Должность')
    department = forms.ChoiceField(choices=DEPARTMENT, required=False, label='Отделение')
