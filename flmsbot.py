#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot;
from telebot import types
from telebot import types # для указание типов
import mysql.connector 
import json
import datetime
from datetime import datetime

bot = telebot.TeleBot()


pictures = ["pictures/pict1.jpg", "pictures/protean.jpg","pictures/pict2.png","pictures/search.jpg", "pictures/iden.png"]


@bot.message_handler(commands = ['start'])
def url(message):

        markup = types.InlineKeyboardMarkup()

        button1 = types.InlineKeyboardButton('ПРОДОЛЖИТЬ ➡️', callback_data='button1')

        markup.add(button1)

        today = datetime.now()
        	
        bot.send_message(message.chat.id, '🥤 Все фильмы в одном боте Жми на кнопку чтобы узнать названия фильмов ⤵️', reply_markup=markup)


        json_file = 'newsubs.json'
        data =     {"id": str(message.chat.id)}
        with open(json_file, 'r') as file:
            python_object = json.load(file)


        if  data in python_object['subs']:
            print("user in json")
        else:
            python_object['subs'].append(data)
            with open(json_file, 'w') as f:
                json.dump(python_object, f, indent=2)
        new_user()
        


def check(id):
        try:
            json_file = 'newsubs.json'
            with open(json_file, 'r') as file:
                data = json.load(file)
                return id in data['subs']
        except FileNotFoundError:
            print(f"Файл не найден.")
            return False
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле")
            return False


@bot.message_handler(commands = ['br'])
def url(message):

        json_file = 'newsubs.json'

        with open('news.json', 'r') as fl:
            news = json.load(fl)
        start_markup = telebot.types.InlineKeyboardMarkup()

        textHTML = news[0]['html']
        textIMG = news[0]['img']
        textBUTTON = news[0]['button']
        textURL = news[0]['URL']


        bot1 = telebot.types.InlineKeyboardButton(textBUTTON, url=textURL)
        start_markup.row(bot1)
        with open(json_file, 'r') as file:
            python_object = json.load(file)

            for element in python_object['subs']:
                
                    img = open(textIMG, 'rb')
                    bot.send_photo(element['id'], img, caption=textHTML,parse_mode='HTML',reply_markup=start_markup)
                   # bot.send_message(element['id'], textHTML,parse_mode='HTML',reply_markup=start_markup)

#@bot.message_handler(commands = ['list'])
def new_user():
    json_file = 'newsubs.json'
    with open(json_file, 'r') as file:
        python_object = json.load(file)
    len = 0
    for element in python_object['subs']:
        len = len + 1
    bot.send_message('', "У нас новый " + str(len) + "-й пользователь!")
    

@bot.message_handler(func=lambda message: True)
def ChatGPT_meeting(message):
        markupTWO = types.InlineKeyboardMarkup()
        user_channel_status = bot.get_chat_member(chat_id="@filmology_top", user_id=message.chat.id)
        user_channel_status_two = bot.get_chat_member(chat_id="@by_n1ght", user_id=message.chat.id)

        if (user_channel_status.status != 'left' and user_channel_status_two.status != 'left'):
            json_file = 'films.json'

            with open(json_file, 'r') as file:
                python_object = json.load(file)

                for element in python_object:
                    if(message.text == str(element['id'])):
                        bot.send_message('-4111037342', "Пользователь ввел фильм под номером: " + str(element['id']) + " под названием: " + element['name_film'])
                        if(len(element['film_url']) > 1):
                            watch  = types.InlineKeyboardButton('🔸СМОТРЕТЬ🔸',url=element['film_url'])
                            search  = types.InlineKeyboardButton('🔎 ВСЕ ФИЛЬМЫ', url="https://t.me/filmology_top")

                            markupTWO.add(watch, search)
                        else:
                            search  = types.InlineKeyboardButton('🔎 ВСЕ ФИЛЬМЫ', url="https://t.me/filmology_top")

                            markupTWO.add(search)

                        img = open(element['name_image'], 'rb')
                        bot.send_photo(message.chat.id, img,parse_mode='HTML', caption=element['name_film'],reply_markup=markupTWO)
        else:
            markup = types.InlineKeyboardMarkup()

            button1 = types.InlineKeyboardButton('ПРОДОЛЖИТЬ ➡️', callback_data='button1')

            markup.add(button1)
        	
            bot.send_message(message.chat.id, 'Сначала подпишитесь на наши каналы! ⤵️', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'button1')
def button1_handler(call):
    # Здесь можно указать любую логику обработки нажатия на кнопку 'Кнопка 1'

        user_channel_status = bot.get_chat_member(chat_id="@filmology_top", user_id=call.message.chat.id)
        user_channel_status_two = bot.get_chat_member(chat_id="@by_n1ght", user_id=call.message.chat.id)
        markup = types.InlineKeyboardMarkup()

        if (user_channel_status.status == 'left' and user_channel_status_two.status == 'left'):
            add1  = types.InlineKeyboardButton('Фильмология 🍿',url='https://t.me/filmology_top', callback_data='button1')
            add3  = types.InlineKeyboardButton('Уголок программиста ☘️',url='https://t.me/by_n1ght', callback_data='button2')
            add2  = types.InlineKeyboardButton('Я ПОДПИСАЛСЯ 👍', callback_data='add2')
            print("Человел не подписался на группы! ")
            markup.add(add1, add2, add3)
            bot.send_message(call.message.chat.id, '📝 Для использования бота, вы должны быть подписаны на наши каналы:', reply_markup=markup)
        elif user_channel_status.status == 'left':
            add1  = types.InlineKeyboardButton('Фильмология 🍿',url='https://t.me/filmology_top', callback_data='button1')
            add2  = types.InlineKeyboardButton('Я ПОДПИСАЛСЯ 👍', callback_data='add2')
            markup.add(add2, add1)
            bot.send_message(call.message.chat.id, '📝 Для использования бота, вы должны быть подписаны на наши каналы:', reply_markup=markup)
        elif user_channel_status_two.status == 'left':
            add3  = types.InlineKeyboardButton('Уголок программиста ☘️',url='https://t.me/by_n1ght', callback_data='button2')
            add2  = types.InlineKeyboardButton('Я ПОДПИСАЛСЯ 👍', callback_data='add2')
            markup.add(add3, add2)
            bot.send_message(call.message.chat.id, '📝 Для использования бота, вы должны быть подписаны на наши каналы:', reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, '🍿 Введите код фильма:')

@bot.callback_query_handler(func=lambda call: call.data == 'add2')
def button2_handler(call):
    # Здесь можно указать любую логику обработки нажатия на кнопку 'Кнопка 1'
        user_channel_status = bot.get_chat_member(chat_id="@filmology_top", user_id=call.message.chat.id)
        user_channel_status_two = bot.get_chat_member(chat_id="@by_n1ght", user_id=call.message.chat.id)

        if (user_channel_status.status != 'left' and user_channel_status_two.status != 'left'):
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message('', '🔥 Пользователь подписался на каналы!')
            bot.send_message(call.message.chat.id, '👍 Спасибо, что подписались на наши каналы!')
            bot.send_message(call.message.chat.id, '🍿 Введите код фильма:')
        else:
            bot.delete_message(call.message.chat.id,call.message.id)
            button1_handler(call)
            
bot.infinity_polling()
