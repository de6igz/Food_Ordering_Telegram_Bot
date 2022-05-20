import csv
import re

salads_dictionary = {}  # Словарь для салатов
soups_dictionary = {}  # Словарь для супов
drinks_dictionary = {}  # Словарь для напитков
with open('меню.csv') as File:
    reader = csv.reader(File, delimiter=';', quotechar=',',  # Считываем данные из csv файла
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        # print(row)
        salads_dictionary[row[0]] = row[1]  # Добавляем в словари
        soups_dictionary[row[4]] = row[5]
        drinks_dictionary[row[8]] = row[9]

############################################################################################
salads_list = []
for key in salads_dictionary:  # Первично добавляем позиции салата в массив салата
    if key != '':
        salads_list.append(key)


def salads_menu_updating():  # Функция обновления позиций в листе салата
    global salads_list
    salads_list.clear()
    for salad_name, amount in list(salads_dictionary.items()):
        if salad_name == '' or amount == '':  # Проверка не является ли значений пустым. Если да, то пропускаем его
            continue  # (Обработка исключения, чтобы не было ошибки) Переходит на следующий круг цикла
        else:
            if int(amount) <= 0:
                del salads_dictionary[salad_name]
    for key in salads_dictionary:
        if key != '':
            salads_list.append(key)


############################################################################################
soups_list = []         # Первично добавляем позиции супов в массив супов
for key in soups_dictionary:
    if key != '':
        soups_list.append(key)


def soups_menu_updating():  # Функция обновления позиций в листе супов
    global soups_list
    soups_list.clear()
    for soup_name, amount in list(soups_dictionary.items()):
        if soup_name == '' or amount == '':  # Проверка не является ли значений пустым. Если да, то пропускаем его
            continue  # (Обработка исключения, чтобы не было ошибки) Переходит на следующий круг цикла
        else:
            if int(amount) <= 0:
                del soups_dictionary[soup_name]
    for key in soups_dictionary:
        if key != '':
            soups_list.append(key)


############################################################################################
drinks_list = []        # Первично добавляем позиции напитков в массив напитков
for key in drinks_dictionary:
    if key != '':
        drinks_list.append(key)


def drinks_menu_updating():  # Функция обновления позиций в листе супов
    global drinks_list
    drinks_list.clear()
    for drink_name, amount in list(drinks_dictionary.items()):
        if drink_name == '' or amount == '':  # Проверка не является ли значений пустым. Если да, то пропускаем его
            continue  # (Обработка исключения, чтобы не было ошибки) Переходит на следующий круг цикла
        else:
            if int(amount) <= 0:
                del drinks_dictionary[drink_name]
    for key in drinks_dictionary:
        if key != '':
            drinks_list.append(key)


############################################################################################

def define_declension_of_rubles(order_price):
    declension_of_rubles = str  # Определяем окончание рубля
    last_number_of_order_price = int(re.search(r"\d$", str(order_price)).group(0))  #
    if last_number_of_order_price == 0:  #
        declension_of_rubles = 'рублей'  #
    elif last_number_of_order_price == 1:  #
        declension_of_rubles = 'рубль'  #
    elif 2 <= last_number_of_order_price <= 4:  #
        declension_of_rubles = 'рубля'  #
    elif 5 <= last_number_of_order_price <= 9:  #
        declension_of_rubles = 'рублей'  #
    return declension_of_rubles
