from src.reports import spending_by_weekday
from src.services import search_transfers_individuals
from src.views import home_page
from src.utils import get_data_from_file
import datetime


print('Выберите пункт для начала работы:')
print('1. Веб-страницы: Главная')
print('2. Сервисы: Поиск переводов физическим лицам')
print('3. Отчеты: Средние траты по дням недели')
input_user = input()
if input_user == '1':
    user_input_date = input('Введите дату в формате YYYY-MM-DD HH:MM:SS: ')
    date = datetime.datetime.strptime(user_input_date, '%Y-%m-%d %H:%M:%S')
    print(home_page(date))
elif input_user == '2':
    print(search_transfers_individuals())
elif input_user == '3':
    df = get_data_from_file()
    user_input_date = input('Введите дату в формате YYYY-MM-DD HH:MM:SS: ')
    if not user_input_date:
        print(spending_by_weekday(df))
    else:
        print(spending_by_weekday(df, user_input_date))
else:
    print('Некорректный ввод')





# user_input = input('Введите дату в формате YYYY-MM-DD HH:MM:SS: ')
# if not user_input:
#     date = datetime.datetime.now()
# else:
#     date = datetime.datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
