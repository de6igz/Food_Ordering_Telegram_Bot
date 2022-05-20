import time

import telebot
from telebot import types
from telebot.types import LabeledPrice

import gitignore.token2
import menu
from menu import *
from gitignore.token2 import *
import re

bot = telebot.TeleBot(token=token)
bank_token = ' '
users_orders = {}
users_prices = {}
zakaz_nomer = 0
numbers_and_orders = {}
cashier = gitignore.token2.cashier_id
zakaz_nomer_and_userID = {}
last_time_message = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    last_time_message[message.from_user.id] = int(time.time() // 1)
    users_orders[message.from_user.id] = []
    users_prices[message.from_user.id] = ''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Меню🍔🍟🍕🥟🫕🥗🌮🌯")
    markup.add(button1)
    if message.from_user.id == cashier:
        bot.send_message(cashier, 'Ожидаю заказов🍿🍿🍿')
    else:
        bot.send_message(message.chat.id, "Привет, с помощью этого бота ты сможешь заказать еду!", reply_markup=markup),


@bot.message_handler(content_types='text')
def message_reply(message):
    global markup_menu_categories
    global bank_token
    markup_menu_categories = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Салаты🥗")
    button2 = types.KeyboardButton("Супы🥘")
    button3 = types.KeyboardButton("Напитки🧃")
    button4 = types.KeyboardButton("Корзина🛒")
    markup_menu_categories.add(button1, button2, button3, button4)
    if message.text == "Меню🍔🍟🍕🥟🫕🥗🌮🌯":
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup_menu_categories)
    if message.text == 'Салаты🥗':
        if int(time.time() // 1) - last_time_message[message.from_user.id] < 2:
            return 0
        else:
            last_time_message[message.from_user.id] = int(time.time() // 1)
            salads_menu_updating()
            salads_buttons(message)
    if message.text == '🔙Назад':
        if int(time.time() // 1) - last_time_message[message.from_user.id] < 2:
            return 0
        else:
            last_time_message[message.from_user.id] = int(time.time() // 1)
            bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup_menu_categories)
    if message.text == 'Супы🥘':
        if int(time.time() // 1) - last_time_message[message.from_user.id] < 2:
            return 0
        else:
            last_time_message[message.from_user.id] = int(time.time() // 1)
            soups_menu_updating()
            soups_buttons(message)
    if message.text == 'Напитки🧃':
        if int(time.time() // 1) - last_time_message[message.from_user.id] < 2:
            return 0
        else:
            last_time_message[message.from_user.id] = int(time.time() // 1)
            drinks_menu_updating()
            drinks_buttons(message)
    if message.text == 'Корзина🛒':
        if int(time.time() // 1) - last_time_message[message.from_user.id] < 2:
            return 0
        else:
            last_time_message[message.from_user.id] = int(time.time() // 1)
            show_cart(message)
    if re.search("Удалить", str(message.text)):
        delete_from_cart(message)
    if message.text == 'Оплатить💸💸💸':
        choosing_payment_operator(message)


def choosing_payment_operator(message):
    try:
        tmp_price = int(users_prices[message.from_user.id]) * 100
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button1 = types.KeyboardButton("Сбербанк🟢")
        button2 = types.KeyboardButton("ЮКасса🟡⚫️")
        button3 = types.KeyboardButton("PayMaster")
        button4 = types.KeyboardButton("ПСБ")
        button5 = types.KeyboardButton("Bank 131")
        markup.add(button1, button2, button3, button4, button5)
        msg = bot.send_message(message.chat.id, 'Какой платёжной системой вы хотели бы воспользоваться?',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, making_bank_token)
    except Exception as e:
        bot.send_message(message.chat.id, 'В корзине пусто ⭕')


def making_bank_token(message):
    global bank_token
    if message.text == 'Сбербанк🟢':
        bank_token = sber_token
    elif message.text == 'ЮКасса🟡⚫️':
        bank_token = YandexKassa_token
    elif message.text == 'PayMaster':
        bank_token = payMaster_token
    elif message.text == 'ПСБ':
        bank_token = PSB_token
    elif message.text == 'Bank 131':
        bank_token = bank131_token
    pay_order(message)


def pay_order(message):
    markup = types.ReplyKeyboardRemove()
    key = int(message.from_user.id)
    try:
        tmp_price = int(users_prices[message.from_user.id]) * 100
        price = [LabeledPrice(label='Заказ в "НЕСТОЛОВАЯ UPGRADE"', amount=tmp_price)]
        formatted_user_cart = '\n -'.join(users_orders[key])
        msg = bot.send_message(message.chat.id, 'Настраиваем кассу...', reply_markup=markup)
        bot.send_animation(message.chat.id, open('media/mr_krabs_counting_money.gif', 'rb'))
        time.sleep(1)
        bot.send_invoice(message.chat.id, title='Оплата заказа',
                         photo_url='https://cdn-icons-png.flaticon.com/512/2927/2927347.png', photo_size=128,
                         photo_width=128,
                         photo_height=128,
                         invoice_payload='Оплатить заказ', currency='RUB', prices=price,
                         description=f'-{formatted_user_cart}', provider_token=bank_token)
    except Exception as e:
        bot.send_message(message.chat.id, 'В корзине пусто ⭕')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Оплата не прошла❌"
                                                "Попробуйте позже")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    global zakaz_nomer
    zakaz_nomer += 1
    numbers_and_orders[zakaz_nomer] = users_orders[message.from_user.id]
    zakaz_nomer_and_userID[zakaz_nomer] = message.from_user.id
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,
                     f'Оплата прошла успешно, ожидай свой заказ!✅\n⏳Номер вашего заказа : {zakaz_nomer}'.format(
                         message.successful_payment.total_amount, message.successful_payment.currency),
                     reply_markup=markup)
    bot.send_animation(message.chat.id, open('media/sponge_bob_cooking_burger.gif', 'rb'))
    send_admin_order(zakaz_nomer)


def send_admin_order(nomer_zakaza):
    inline_markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(f"Заказ номер {nomer_zakaza} готов✅", callback_data='Готово')
    inline_markup.add(button)
    formatted_user_cart = '\n -'.join(numbers_and_orders[zakaz_nomer])
    bot.send_message(cashier, f'Заказ номер {nomer_zakaza}\n\n-{formatted_user_cart}', reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def inline_awnser(call):
    if call.message:
        zakaz_nomer = int(re.search(r"\d+", str(call.message.text)).group(0))
        client = zakaz_nomer_and_userID[zakaz_nomer]
        bot.answer_callback_query(call.id, "Готов")
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_animation(client, open('media/garfield-hungry.gif', 'rb'))
        bot.send_message(client,
                         f'Ваш заказ готов!🥳\nПокажите это сообщение на кассе \nНомер заказа: <i><b>{zakaz_nomer}</b></i>\n\nЕсли хотите сделать еще один заказ, то напишите /start',
                         parse_mode='HTML')


def delete_from_cart(message):
    key = int(message.from_user.id)
    cart_massiv_before_formatted = []
    cart_massiv_after_formatted = []
    template = str
    for position in users_orders[key]:
        if position != []:
            cart_massiv_before_formatted.append(position)
            if position in str(message.text):
                template = position
    current_price = int(users_prices[key])
    price_from_template = int(re.search(r"\d+", template).group(0))
    current_price = current_price - price_from_template
    users_prices[key] = current_price
    users_orders[key].remove(template)
    show_cart(message)


def show_cart(message):
    cart_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔙Назад')
    button2 = types.KeyboardButton('Оплатить💸💸💸')
    cart_markup.add(button1, button2)
    cart_massiv = []
    key = int(message.from_user.id)
    for poistion in users_orders[key]:
        if poistion != []:
            cart_massiv.append(poistion)
    for poistion1 in cart_massiv:
        formatted_position = f"❌Удалить '{poistion1}' "
        cart_markup.add(formatted_position)
    if users_orders[message.from_user.id] == []:
        bot.send_message(message.chat.id, 'В корзине пусто ⭕', reply_markup=cart_markup)
    else:
        formatted_user_cart = '\n -'.join(users_orders[key])
        bot.send_message(message.chat.id,
                         f'Ваш заказ на сумму {users_prices[message.from_user.id]} {define_declension_of_rubles(int(users_prices[message.from_user.id]))}:\n- {formatted_user_cart} ',
                         reply_markup=cart_markup)


def salads_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙Назад")
    for salad in salads_list:
        markup.add(salad)
    formatted_salads_list = '\n -'.join(salads_list)
    msg = bot.send_message(message.chat.id, f"Список салатов:\n -{formatted_salads_list}", reply_markup=markup)
    bot.register_next_step_handler(msg, adding_order_price_salads)


def adding_order_price_salads(message):
    if not str(message.text) == '🔙Назад':
        try:
            if int(salads_dictionary[str(message.text)]) > 0:
                if menu.salads_dictionary.__contains__(str(message.text)):
                    tmp = menu.salads_dictionary[str(message.text)]
                    menu.salads_dictionary[str(message.text)] = int(tmp) - 1
                    update_users_cart(message)
                bot.send_message(message.chat.id, f'"{message.text}" добавлен в заказ ✅',
                                 reply_markup=markup_menu_categories)
            else:
                salads_list.remove(str(message.text))
                bot.send_message(message.chat.id, 'К сожалению данная позиция закончилась',
                                 reply_markup=markup_menu_categories)
        except Exception as e:
            bot.reply_to(message, 'Такой позиции в меню нет')
            salads_buttons(message)
    else:
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup_menu_categories)


def soups_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙Назад")
    for soup in soups_list:
        markup.add(soup)
    formatted_soups_list = '\n -'.join(soups_list)
    msg = bot.send_message(message.chat.id, f"Список супов:\n -{formatted_soups_list}", reply_markup=markup)
    bot.register_next_step_handler(msg, adding_order_price_soups)


def adding_order_price_soups(message):
    if not str(message.text) == '🔙Назад':
        try:
            if int(soups_dictionary[str(message.text)]) > 0:
                if menu.soups_dictionary.__contains__(str(message.text)):
                    tmp = menu.soups_dictionary[str(message.text)]
                    menu.soups_dictionary[str(message.text)] = int(tmp) - 1
                    update_users_cart(message)
                bot.send_message(message.chat.id, f'"{message.text}" добавлен в заказ ✅',
                                 reply_markup=markup_menu_categories)
            else:
                soups_list.remove(str(message.text))
                bot.send_message(message.chat.id, 'К сожалению данная позиция закончилась',
                                 reply_markup=markup_menu_categories)
        except Exception as e:
            bot.reply_to(message, 'Такой позиции в меню нет')
            soups_buttons(message)
    else:
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup_menu_categories)


def drinks_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔙Назад")
    for drink in drinks_list:
        markup.add(drink)
    formatted_drinks_list = '\n -'.join(drinks_list)
    msg = bot.send_message(message.chat.id, f"Список напитков:\n -{formatted_drinks_list}", reply_markup=markup)
    bot.register_next_step_handler(msg, adding_order_price_drinks)


def adding_order_price_drinks(message):
    if not str(message.text) == '🔙Назад':
        try:
            if int(drinks_dictionary[str(message.text)]) > 0:
                if menu.drinks_dictionary.__contains__(str(message.text)):
                    tmp = menu.drinks_dictionary[str(message.text)]
                    menu.drinks_dictionary[str(message.text)] = int(tmp) - 1
                    update_users_cart(message)
                bot.send_message(message.chat.id, f'"{message.text}" добавлен в заказ ✅',
                                 reply_markup=markup_menu_categories)
            else:
                drinks_list.remove(str(message.text))
                bot.send_message(message.chat.id, 'К сожалению данная позиция закончилась',
                                 reply_markup=markup_menu_categories)
        except Exception as e:
            bot.reply_to(message, 'Такой позиции в меню нет')
            drinks_buttons(message)
    else:
        bot.send_message(message.chat.id, 'Выбери категорию', reply_markup=markup_menu_categories)


def update_users_cart(message):
    key = int(message.from_user.id)
    tmp_massiv = []
    tmp_massiv.clear()
    tmp_massiv = (users_orders[key])
    tmp_massiv.append(str(message.text))
    users_orders[key] = tmp_massiv
    if users_prices[key] == '':
        tmp_price = int(re.search(r"\d+", str(message.text)).group(0))
    else:
        tmp_price = int(users_prices[key]) + int(re.search(r"\d+", str(message.text)).group(0))
    users_prices[key] = str(tmp_price)


bot.infinity_polling()
