# -*- coding: utf-8 -*-
# author: Chan

import requests
import time
import telegram
import logging
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Updater, MessageHandler
from NewjwxtInfo import newjwxt, Weekday, Weekday_num, weekday_alpha, class_num, num, user_data
from config import TOKEN, START_TIME


def help_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="使用方法:"+'\n' +
                     "登录教务系统(登录一次即可):"+'\n'+"/regist <学号> <密码>"+'\n'+"删除数据: /del"+'\n'+"当日课表: /class"+'\n'+"明日课表: /tomorrow"+'\n'+"本周课表: /thisweek"+'\n'+"下周课表: /nextweek"+'\n'+"查看周数: /week"+'\n'+"查看帮助: /help")


def regist_command(bot, update):
    chat_id = update.message.chat_id
    b = ''
    c = ''
    try:
        # 数组形式保存账号密码
        user_data[chat_id] = [
            update.message.text.split()[1], update.message.text.split()[2]]
        new = newjwxt()
        new.login(chat_id)

        # 对密码进行加密
        password = user_data[chat_id][1]
        for byte in range(1, len(password)-1):
            c = c+password[byte].replace(password[byte], '*')
        b = password[0]+c+password[len(password)-1]
        text = new.info(chat_id).split('(')[0]
        bot.send_message(chat_id=chat_id, text="姓名:"+text+'\n'+"学号:" +
                         user_data[chat_id][0]+'\n'+"密码:"+b)
    except:
        bot.send_message(chat_id=chat_id, text="登录失败,请检查账密 /help")


def del_command(bot, update):
    # 删除登录信息
    chat_id = update.message.chat_id
    del user_data[chat_id]
    bot.send_message(chat_id=chat_id, text="数据已删除")


def dailyclass_command(bot, update):
    # 获取当日课表
    chat_id = update.message.chat_id
    localtime = time.localtime()
    delta = int(
        (((localtime[1]-START_TIME[1])*30+(localtime[2]-START_TIME[2]))/7)+1)
    weekday = Weekday[time.strftime("%a")]
    try:
        s = ''
        new = newjwxt()
        new.login(chat_id)
        dic = new.get_classes(delta, weekday)
        if dic == {}:
            bot.send_message(chat_id=chat_id, text="今天没有课!")
        elif dic != {}:
            dic = list(dic.values())
            for i in dic:
                s = s+i+'\n'
            bot.send_message(chat_id=chat_id,
                             text="今日课程:\n"+s)
    except:
        bot.send_message(chat_id=chat_id, text="获取失败,请先登录 /help")


def get_week_num(bot, update):
    localtime = time.localtime()
    delta = int(
        (((localtime[1]-START_TIME[1])*30+(localtime[2]-START_TIME[2]))/7)+1)
    bot.send_message(chat_id=update.message.chat_id,
                     text="本周为第"+repr(delta)+"周")


def thisweek_command(bot, update):
    localtime = time.localtime()
    delta = int(
        (((localtime[1]-START_TIME[1])*30+(localtime[2]-START_TIME[2]))/7)+1)
    chat_id = update.message.chat_id
    S = ''
    # bot.send_message(chat_id=chat_id,text="查询中,请稍等...")
    message_id = bot.send_message(
        chat_id=chat_id, text="查询中,请稍等...").message_id
    for num in range(1, 8):
        weekday = Weekday_num[str(num)]
        try:
            s = ''
            new = newjwxt()
            new.login(chat_id)
            dic = new.get_classes(delta, weekday)
            if dic == {}:
                s = s+weekday_alpha[str(num)]+'\n'+"没有课"+'\n'
                S = S+s
                # bot.send_message(chat_id=chat_id, text=s)
            elif dic != {}:
                dic = list(dic.values())
                S = S+weekday_alpha[str(num)]+'\n'
                # s = s+'\n'
                for i in dic:
                    S = S+i+'\n'
                    # S=S+s
                # bot.send_message(chat_id=chat_id,
                #                  text=s)
        except:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text="获取失败 /help")
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=S)


def nextweek_command(bot, update):
    localtime = time.localtime()
    delta = int(
        (((localtime[1]-START_TIME[1])*30+(localtime[2]-START_TIME[2]))/7)+2)
    chat_id = update.message.chat_id
    S = ''
    # bot.send_message(chat_id=chat_id,text="查询中,请稍等...")
    message_id = bot.send_message(
        chat_id=chat_id, text="查询中,请稍等...").message_id
    for num in range(1, 8):
        weekday = Weekday_num[str(num)]
        try:
            s = ''
            new = newjwxt()
            new.login(chat_id)
            dic = new.get_classes(delta, weekday)
            if dic == {}:
                s = s+weekday_alpha[str(num)]+'\n'+"没有课"+'\n'
                S = S+s
                # bot.send_message(chat_id=chat_id, text=s)
            elif dic != {}:
                dic = list(dic.values())
                S = S+weekday_alpha[str(num)]+'\n'
                # s = s+'\n'
                for i in dic:
                    S = S+i+'\n'
                    # S=S+s
                # bot.send_message(chat_id=chat_id,
                #                  text=s)
        except:
            bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text="获取失败 /help")
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=S)


def tomorrowclass_command(bot, update):
    chat_id = update.message.chat_id
    localtime = time.localtime()
    delta = int(
        (((localtime[1]-START_TIME[1])*30+(localtime[2]-START_TIME[2]))/7)+1)
    weekday = Weekday[time.strftime("%a")]
    weekday = str(int(weekday.split('-')[0])+1)+'-2'
    if (time.strftime("%a") == "Sun"):
        weekday = "1-2"
        delta = delta+1
    try:
        s = ''
        new = newjwxt()
        new.login(chat_id)
        dic = new.get_classes(delta, weekday)
        if dic == {}:
            bot.send_message(chat_id=chat_id, text="明天没有课!")
        elif dic != {}:
            # print(dic)
            dic = list(dic.values())
            # print (dic)
            for i in dic:
                s = s+i+'\n'
            # print(s)
            bot.send_message(chat_id=chat_id,
                             text="明日课程:\n"+s)
    except:
        bot.send_message(chat_id=chat_id, text="获取失败,请先登录 /help")


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    dispatcher.add_handler(CommandHandler('start', help_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('regist', regist_command))
    dispatcher.add_handler(CommandHandler('del', del_command))
    dispatcher.add_handler(CommandHandler('class', dailyclass_command))
    dispatcher.add_handler(CommandHandler('thisweek', thisweek_command))
    dispatcher.add_handler(CommandHandler('nextweek', nextweek_command))
    dispatcher.add_handler(CommandHandler('tomorrow', tomorrowclass_command))
    dispatcher.add_handler(CommandHandler('week', get_week_num))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
