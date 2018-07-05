# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types
import urllib3
import re
import requests
import time
from time import sleep
import datetime
from datetime import datetime
import _thread
import random


# ======================================================================================================================
tkn = '617835554:AAHTqC39hgIGOSvaGEqrr8wDCGArB5EZwpA'
bot = telebot.TeleBot(tkn)

idMe = 396978030
idAdmin1 = 396978030
idAdmin2 = 396978030
idChatDevelopment = -1001309670055

NBOT = 'C' + 'h' + 'a' + 't' + 'W' + 'a' + 'r' + 's' + 'B' + 'o' + 't'
# ======================================================================================================================


def g_token(key, list):
    global sheet1
    global sheet2
    global sheet3
    global sheet4
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    if key == 1:
        creds1 = ServiceAccountCredentials.from_json_keyfile_name('person1.json', scope)
        client1 = gspread.authorize(creds1)
        sheet1 = client1.open('Time-mashine').worksheet(list)
    elif key == 2:
        creds2 = ServiceAccountCredentials.from_json_keyfile_name('person2.json', scope)
        client2 = gspread.authorize(creds2)
        sheet2 = client2.open('Time-mashine').worksheet(list)
    elif key == 3:
        creds3 = ServiceAccountCredentials.from_json_keyfile_name('person3.json', scope)
        client3 = gspread.authorize(creds3)
        sheet3 = client3.open('Time-mashine').worksheet(list)
    elif key == 4:
        creds4 = ServiceAccountCredentials.from_json_keyfile_name('person4.json', scope)
        client4 = gspread.authorize(creds4)
        sheet4 = client4.open('Time-mashine').worksheet(list)


g_token(1, 'main')
g_names = sheet1.col_values(1)
g_ids = sheet1.col_values(2)
bot.send_message(idMe, '🤤')


def rawtime(stamp):
    rtime = []
    weekday = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%a')
    if weekday == 'Mon':
        weekday = 'Пн'
    elif weekday == 'Tue':
        weekday = 'Вт'
    elif weekday == 'Wed':
        weekday = 'Ср'
    elif weekday == 'Thu':
        weekday = 'Чт'
    elif weekday == 'Fri':
        weekday = 'Пт'
    elif weekday == 'Sat':
        weekday = 'Сб'
    elif weekday == 'Sun':
        weekday = 'Вс'
    day = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%d')
    month = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%m')
    year = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%Y')
    hours = datetime.utcfromtimestamp(int(stamp + 3 * 60 * 60)).strftime('%H')
    minutes = datetime.utcfromtimestamp(int(stamp)).strftime('%M')
    seconds = datetime.utcfromtimestamp(int(stamp)).strftime('%S')
    rtime.append(weekday)
    rtime.append(day)
    rtime.append(month)
    rtime.append(year)
    rtime.append(hours)
    rtime.append(minutes)
    rtime.append(seconds)
    return rtime


@bot.message_handler(commands=['time'])
def handle_time_command(message):
    time = rawtime(int(datetime.now().timestamp()))
    text = 'Время: ' + str(time[4]) + ':' + str(time[5]) + ':' + str(time[6]) + \
        ' <code>(' + str(time[0]) + ' ' + str(time[1] + '.' + str(time[2]) + '.' + \
        str(time[3])) + ', GMT+3)</code>'
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=['id'])
def handle_id_command(message):
    text = 'Твой ID: <code>' + str(message.from_user.id) + '</code>\n'
    if message.chat.id < 0:
        text = text + 'Group ID: <code>' + str(message.chat.id) + '</code>'
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=['update'])
def handle_start_command(message):
    global g_names
    if message.chat.id == idMe or message.chat.id == idAdmin1 or message.chat.id == idAdmin2:
        g_names = sheet1.row_values(1)
        bot.send_message(message.chat.id, '✅Исполнено')


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if message.chat.id > 0:
        bot.send_message(message.chat.id, 'Привет 😛')


@bot.message_handler(content_types=["new_chat_members"])
def get_new_member(message):
    if message.chat.title:
        title = str(message.chat.title) + ' ('
    else:
        title = ' ('
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)
    if message.from_user.username:
        chat_user = '@' + str(message.from_user.username) + ' / '
    else:
        if message.from_user.first_name:
            firstname = str(message.from_user.first_name)
        else:
            firstname = ''
        if message.from_user.last_name:
            lastname = str(message.from_user.last_name) + ' '
        else:
            lastname = ''
        chat_user = firstname + ' ' + lastname

    if message.new_chat_member is not None and message.new_chat_member.username == 'korovan_time_bot':
        bot.send_message(idChatDevelopment,
                         chat_user + user_id + ': Добавил бота в чат: ' + title + chat_id + ')')


@bot.message_handler(func=lambda message: message.text)
def repeat_all_messages(message):
    if message.forward_date is not None:
        if str(message.forward_from.username) == NBOT:
            search = re.search('.*Он пытается.*', message.text)
            if search:
                if str(message.from_user.id) in g_ids:
                    time = rawtime(message.forward_date)
                    row = [str(time[1]) + '.' + str(time[2]) + '.' + str(time[3]) + ' ' + \
                           str(time[4]) + ':' + str(time[5]) + ':' + str(time[6]) + '#' + str(message.forward_date)]
                    try:
                        g_token(1, g_names[g_ids.index(str(message.from_user.id))])
                        g = sheet1.col_values(1)
                    except:
                        try:
                            g_token(2, g_names[g_ids.index(str(message.from_user.id))])
                            g = sheet2.col_values(1)
                        except:
                            try:
                                g_token(3, g_names[g_ids.index(str(message.from_user.id))])
                                g = sheet3.col_values(1)
                            except:
                                g = 0
                    if not g:
                        g_token(4, g_names[g_ids.index(str(message.from_user.id))])
                        sheet4.insert_row(['начало'])
                        g.append('0')
                    if g != 0:
                        marker = 2
                        for i in g:
                            splited = i.split('#')
                            splited.append(1)
                            splited[1] = int(splited[1])
                            if message.forward_date == splited[1]:
                                text = '😒 Повторяемся значит? Я всё помню.'
                                if message.chat.id < 0:
                                    bot.send_message(message.from_user.id, text, parse_mode='HTML')
                                else:
                                    bot.send_message(message.from_user.id, text,
                                                     reply_to_message_id=message.message_id, parse_mode='HTML')
                                break
                            elif len(g) == 0 or g.index(i) == (len(g) - 1):
                                try:
                                    g_token(1, g_names[g_ids.index(str(message.from_user.id))])
                                    sheet1.insert_row(row, g.index(i) + 1)
                                    marker = 1
                                except:
                                    try:
                                        g_token(2, g_names[g_ids.index(str(message.from_user.id))])
                                        sheet2.insert_row(row, g.index(i) + 1)
                                        marker = 1
                                    except:
                                        try:
                                            g_token(3, g_names[g_ids.index(str(message.from_user.id))])
                                            sheet3.insert_row(row, g.index(i) + 1)
                                            marker = 1
                                        except:
                                            text = 'Не удалось записать время, ' \
                                                   'попробуй отправить чуть позже и <b>НЕ ТАКОЙ ЕБАНОЙ ПАЧКОЙ</b>'
                                            if message.chat.id < 0:
                                                bot.send_message(message.from_user.id, text, parse_mode='HTML')
                                            else:
                                                bot.send_message(message.from_user.id, text,
                                                                 reply_to_message_id=message.message_id,
                                                                 parse_mode='HTML')
                                            marker = 0
                                break
                            elif message.forward_date > splited[1]:
                                try:
                                    g_token(1, g_names[g_ids.index(str(message.from_user.id))])
                                    sheet1.insert_row(row, g.index(i) + 1)
                                    marker = 1
                                except:
                                    try:
                                        g_token(2, g_names[g_ids.index(str(message.from_user.id))])
                                        sheet2.insert_row(row, g.index(i) + 1)
                                        marker = 1
                                    except:
                                        try:
                                            g_token(3, g_names[g_ids.index(str(message.from_user.id))])
                                            sheet3.insert_row(row, g.index(i) + 1)
                                            marker = 1
                                        except:
                                            text = 'Не удалось записать время, ' \
                                                   'попробуй отправить чуть позже и <b>НЕ ТАКОЙ ЕБАНОЙ ПАЧКОЙ</b>'
                                            if message.chat.id < 0:
                                                bot.send_message(message.from_user.id, text, parse_mode='HTML')
                                            else:
                                                bot.send_message(message.from_user.id, text,
                                                                 reply_to_message_id=message.message_id,
                                                                 parse_mode='HTML')
                                            marker = 0
                                break
                        if marker == 1:
                            time = rawtime(int(datetime.now().timestamp()) + 57600)
                            good = str(time[1]) + '.' + str(time[2]) + '.' + str(time[3]) + ' ' + \
                                str(time[4]) + ':' + str(time[5]) + ':' + str(time[6])
                            now = 'По моим подсчетам, следующий твой корован будет, примерно <i>' + good + '</i>'
                            if (int(datetime.now().timestamp()) - message.forward_date) < (24 * 60 * 60):
                                very = '🤤 <b>Принято</b>\n' + now
                            else:
                                very = '🤤 <b>Принято</b>'
                            bot.send_message(message.from_user.id, very, parse_mode='HTML')

                    else:
                        text = 'Не удалось записать время, ' \
                               'попробуй отправить чуть позже и <b>НЕ ТАКОЙ ЕБАНОЙ ПАЧКОЙ</b>'
                        if message.chat.id < 0:
                            bot.send_message(message.from_user.id, text, parse_mode='HTML')
                        else:
                            bot.send_message(message.from_user.id, text,
                                             reply_to_message_id=message.message_id, parse_mode='HTML')

                else:
                    try:
                        bot.send_message(message.from_user.id, 'Тебя нет в моей базе, напиши кому-нибудь, '
                                                               'что бы тебя добавили 🤤')
                    except:
                        temp = 0


def telepol():
    try:
        bot.polling(none_stop=True, timeout=60)
    except:
        bot.stop_polling()
        sleep(0.5)
        telepol()


if __name__ == '__main__':
    telepol()