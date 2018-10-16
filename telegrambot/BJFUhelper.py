# -*- coding: utf-8 -*-
# author: Chan

import requests
import time
import datetime
import telegram
import logging
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Updater, MessageHandler
from NewjwxtInfo import newjwxt, Weekday, Weekday_num, weekday_alpha, class_num, num, user_data
from pingjiao import JXPJ
# from qq_login import qqLogin
from config import TOKEN, START_TIME

starttime = datetime.datetime(START_TIME[0], START_TIME[1], START_TIME[2])


def help_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='使用方法:\n登录教务系统(登录一次即可):\n/login <学号> <密码>\n退出登录: /logout\n当日课表: /today\n明日课表: /tomorrow\n本周课表: /thisweek\n下周课表: /nextweek\n查看周数: /week\n查看实验实习安排: /extracourse\n查看帮助: /help\n测试功能:\n一键评教: /evaluate\n查看二课堂: /qqact')


def login_command(bot, update):
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


def logout_command(bot, update):
    # 删除登录信息
    chat_id = update.message.chat_id
    del user_data[chat_id]
    bot.send_message(chat_id=chat_id, text="数据已删除")


def get_week_num(bot, update):
    localtime = datetime.datetime.today()
    delta = int((localtime-starttime).days/7+1)
    bot.send_message(chat_id=update.message.chat_id,
                     text="本周为第"+repr(delta)+"周")


def dailyclass_command(bot, update):
    # 获取当日课表
    chat_id = update.message.chat_id
    localtime = datetime.datetime.today()
    delta = int((localtime-starttime).days/7+1)

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


def thisweek_command(bot, update):
    localtime = datetime.datetime.today()
    delta = int((localtime-starttime).days/7+1)

    chat_id = update.message.chat_id
    S = ''
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
    localtime = datetime.datetime.today()
    delta = int(((localtime-starttime).days-1)/7)+2

    chat_id = update.message.chat_id
    S = ''
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
    localtime = datetime.datetime.today()
    delta = int((localtime-starttime).days/7+1)

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

# 测试功能
# def qqact_command(bot, update):
#     chat_id = update.message.chat_id
#     try:
#         qq = qqLogin()
#         qq.login()
#         info = qq.get_info()
#         bot.send_message(chat_id=chat_id, text=info)
#     except:
#         bot.send_message(chat_id=chat_id, text="Error, try again please.")


def extracourse_command(bot, update):
    # 获取当日课表
    chat_id = update.message.chat_id
    try:
        new = newjwxt()
        new.login(chat_id)
        text = new.get_extracourses()
        update.message.reply_text("实验实习安排:\n{}".format(text))
    except:
        bot.send_message(chat_id=chat_id, text="获取失败,请先登录 /help")


# 测试功能
# def evaluate_command(bot, update):
#     chat_id = update.message.chat_id
#     try:
#         result = JXPJ(chat_id).evaluate()
#         update.message.reply_text(result)
#     except:
#         update.message.reply_text("操作失败, 请重试")



def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    dispatcher.add_handler(CommandHandler('start', help_command))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('login', login_command))
    dispatcher.add_handler(CommandHandler('logout', logout_command))
    dispatcher.add_handler(CommandHandler('today', dailyclass_command))
    dispatcher.add_handler(CommandHandler('thisweek', thisweek_command))
    dispatcher.add_handler(CommandHandler('nextweek', nextweek_command))
    dispatcher.add_handler(CommandHandler('tomorrow', tomorrowclass_command))
    dispatcher.add_handler(CommandHandler('week', get_week_num))
    # dispatcher.add_handler(CommandHandler('qqact', qqact_command))
    dispatcher.add_handler(CommandHandler('extracourse', extracourse_command))
    # dispatcher.add_handler(CommandHandler('evaluate', evaluate_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
