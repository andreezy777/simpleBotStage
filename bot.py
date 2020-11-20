# v0.5
#
#

import re
import config
import telebot
from SQLite3 import SQLighter
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)
day = ''
day_delete = ''



# @bot.message_handler(content_types=["text"])
# def gotostart(message):
#     msg = bot.reply_to(message, "/start")


@bot.message_handler(commands=['start'])
def start(message):
    # if str.lower(message.text) == '/cancel':
    #     msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
    #     bot.register_next_step_handler(msg, start)
    # elif str.lower(message.text) == '/add_date':
    #     msg = bot.reply_to(message, "Пиши день и дату, в которую ты планируешь встречу")
    #     bot.register_next_step_handler(msg, walk_get_day)
    # elif str.lower(message.text) == '/schedule':
    #     msg = bot.reply_to(message,"С кем хотите просмотреть расписание? Отправь контакт или укажи Username с указанием @, например @username")
    #     bot.register_next_step_handler(msg, schedule_read)
    # elif str.lower(message.text) == '/delete':
    #     msg = bot.reply_to(message,
    #                    "С кем отменяете прогулку? Отправь контакт или укажи Username с указанием @, например @username")
    #     bot.register_next_step_handler(msg, reply_to_another_user_about_delete)
    # elif str.lower(message.text) == '/start':
        msg = bot.reply_to(message, """\
        Я бот-ассистент, напиши день, на который тебе назначить встречу, я его запомню
Посмотри /help
        """)
    #     bot.register_next_step_handler(msg, start)
    # elif str.lower(message.text) == '/help':
    #     help('/help')
    # else:
    #     start('/start')



@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """\
Поддерживаемые комманды :
/schedule - посмотреть расписание
/cancel - вернуться в начало, отменить любое действие
/delete - удалить запись
/add_date - добавить запись
""")



@bot.message_handler(commands=['add_date'])
def add_date(message):
    if str.lower(message.text) == '/cancel':
        msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
        bot.register_next_step_handler(msg, start)
    msg = bot.reply_to(message, "Пиши день и дату, в которую ты планируешь встречу")
    bot.register_next_step_handler(msg, walk_get_day)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
    bot.register_next_step_handler(msg, start)

@bot.message_handler(commands=['delete'])
def delete(message):
    if str.lower(message.text) == '/cancel':
        msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
        bot.register_next_step_handler(msg, start)
    msg = bot.reply_to(message, "какой день удалить?")
    bot.register_next_step_handler(msg, delete_day_select_day)



@bot.message_handler(commands=['schedule'])
def schedule(message):
    if str.lower(message.text) == '/cancel':
        msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
        bot.register_next_step_handler(msg, start)
    username = message.from_user.username
    msg = bot.reply_to(message,
                       "С кем хотите просмотреть расписание? Отправь контакт или укажи Username с указанием @, например @username")
    bot.register_next_step_handler(msg, schedule_read)


@bot.message_handler(content_types=['contact'])
def schedule_read(message):
    try:
        if (message.content_type == 'contact'):
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username
            db_worker = SQLighter(config.database)
            userID = message.contact.user_id
            get_ID = db_worker.getID(userID)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            read_from_DB = db_worker.read_my_data(username, get_ID)
            bot.send_message(message.chat.id,
                         "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                             message.contact.first_name,
                             message.contact.last_name)[:-2],
                         ''.join(str(x) for x in read_from_DB).
                         replace('(', '').replace(')', '').
                         replace('\'', '').replace(',', ', ')[:-2],
                         )
            db_worker.close()
        elif (message.content_type == 'text') & (message.text.startswith('@')):
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username
            username_to = message.text
            username_to = username_to[1:]
            db_worker = SQLighter(config.database)
            get_ID = db_worker.getChatID(username_to)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            getUserID = db_worker.getUserID(get_ID)
            getUserID = "{}".format(
                ''.join(str(x) for x in getUserID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            read_from_DB = db_worker.read_my_data(username, get_ID)
            user_with = bot.get_chat_member(get_ID, getUserID)
            bot.send_message(message.chat.id,
                         "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                             user_with.user.first_name, user_with.user.last_name,
                             ''.join(str(x) for x in read_from_DB).
                                 replace('(', '').replace(')', '').
                                 replace('\'', '').replace(',', ', ')[:-2]))
            db_worker.close()
        elif (message.content_type != 'contact') & (message.text != '/cancel') & (message.text.startswith('@') == False):
            chat_id = message.chat.id
            msg = bot.reply_to(message, "Отправь файл контакта!")
            bot.register_next_step_handler(msg, reply_to_another_user)
        elif str.lower(message.text) == '/cancel':
            msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
            bot.register_next_step_handler(msg, start)
    except Exception as e:
        bot.register_next_step_handler((bot.reply_to(message, 'oooops, попробуй еще раз ввести username')), schedule_read)


#@bot.message_handler(content_types=["text"])
def walk_get_day(message):  # Название функции не играет никакой роли, в принципе
        global day
        day = message.text.title()
        name = message.from_user.first_name
        chat_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username
        db_worker = SQLighter(config.database)
        user_with = 0
        write_to_DB = db_worker.write_to(chat_id, user_id, username, day, user_with)
        if (str.lower(message.text) != "/delete") & (str.lower(message.text) != "/cancel"):
            bot.send_message(message.chat.id,
                          "{}({}) планирует прогулку в эту/это/этот: {}".format(name, username, message.text))
            msg = bot.reply_to(message,
                           "С кем планируете прогулку? Отправь контакт или укажи Username с указанием @, например @username")
            bot.register_next_step_handler(msg, reply_to_another_user)

        elif str.lower(message.text) == "/delete":
            msg = bot.reply_to(message, "какой день удалить?")
            bot.register_next_step_handler(msg, delete_day_select_day)
        elif str.lower(message.text) == '/cancel':
            msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
            bot.register_next_step_handler(msg, start)
        db_worker.close()
    # else:
    #     msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
    #     bot.register_next_step_handler(msg, start)


# add
@bot.message_handler(content_types=['contact'])
def reply_to_another_user(message):
    try:
        if (message.content_type == 'contact'):
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username
            db_worker = SQLighter(config.database)
            userID = message.contact.user_id
            get_ID = db_worker.getID(userID)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            write_to_DB = db_worker.write_to(chat_id, user_id, username, day, get_ID)
            db_worker.clear(user_id)
            read_from_DB = db_worker.read_my_data(username, get_ID)
            bot.send_message(get_ID,
                             "У вас новая прогулка с {} {} в {}".format(message.from_user.first_name, message.from_user.
                                                                        last_name, day))
            bot.send_message(message.chat.id,
                             "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                                 message.contact.first_name,
                                 message.contact.last_name)[:-2],
                             ''.join(str(x) for x in read_from_DB).
                             replace('(', '').replace(')', '').
                             replace('\'', '').replace(',', ', ')[:-2]
                             )
            db_worker.close()
        elif (message.content_type == 'text') & (message.text.startswith('@')):
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username
            username_to = message.text
            username_to = username_to[1:]
            db_worker = SQLighter(config.database)
            get_ID = db_worker.getChatID(username_to)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            getUserID = db_worker.getUserID(get_ID)
            getUserID = "{}".format(
                ''.join(str(x) for x in getUserID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            write_to_DB = db_worker.write_to(chat_id, user_id, username, day, get_ID)
            db_worker.clear(user_id)
            read_from_DB = db_worker.read_my_data(username, get_ID)
            bot.send_message(get_ID,
                             "У вас новая прогулка с {} {} в {}".format(message.from_user.first_name, message.from_user.
                                                                        last_name, day))
            user_with = bot.get_chat_member(get_ID, getUserID)
            bot.send_message(message.chat.id,
                             "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                                 user_with.user.first_name, user_with.user.last_name,
                                 ''.join(str(x) for x in read_from_DB).
                                     replace('(', '').replace(')', '').
                                     replace('\'', '').replace(',', ', ')[:-2]
                             ))
            db_worker.close()
        elif (message.content_type != 'contact') & (message.text != '/cancel') & (message.text.startswith('@') == False):
            chat_id = message.chat.id
            msg = bot.reply_to(message, "Отправь файл контакта!")
            bot.register_next_step_handler(msg, reply_to_another_user)
        elif str.lower(message.text) == '/cancel':
            msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
            bot.register_next_step_handler(msg, start)
    except Exception as e:
        bot.register_next_step_handler((bot.reply_to(message, 'oooops, попробуй еще раз ввести username')),
                                   reply_to_another_user)

# delete
#@bot.message_handler(content_types=["text"])
def delete_day_select_day(message):
    if str.lower(message.text) == '/cancel':
        msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
        bot.register_next_step_handler(msg, walk_get_day)
    global day_delete
    day_delete = message.text.title()
    msg = bot.reply_to(message,
                       "С кем отменяете прогулку? Отправь контакт или укажи Username с указанием @, например @username")
    bot.register_next_step_handler(msg, reply_to_another_user_about_delete)


@bot.message_handler(content_types=['contact'])
def reply_to_another_user_about_delete(message):
    try:
        if (message.content_type == 'contact'):
            username = message.from_user.username
            user_id = message.from_user.id
            db_worker = SQLighter(config.database)
            userID = message.contact.user_id
            get_ID = db_worker.getID(userID)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            check_row = db_worker.check_row(day_delete, user_id, get_ID)
            if check_row == 0:
                bot.register_next_step_handler((bot.reply_to(message, 'oooops, в такой день прогулки нету, попробуй еще')),
                                               cancel)
            delete_from_db = db_worker.delete_row(day_delete, user_id, get_ID)
            db_worker.clear(user_id)
            bot.send_message(get_ID,
                         "У вас отменяется прогулка с {} {}  в {}".format(message.from_user.first_name,
                                                                          message.from_user.
                                                                          last_name, day_delete))
            read_from_DB = db_worker.read_my_data(username, get_ID)
            bot.send_message(message.chat.id,
                         "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                             message.contact.first_name,
                             message.contact.last_name)[:-2],
                         ''.join(str(x) for x in read_from_DB).
                         replace('(', '').replace(')', '').
                         replace('\'', '').replace(',', ', ')[:-2]
                         )
            db_worker.close()
        elif (message.content_type == 'text') & (message.text.startswith('@')):
            chat_id = message.chat.id
            user_id = message.from_user.id
            username = message.from_user.username
            username_to = message.text
            username_to = username_to[1:]
            db_worker = SQLighter(config.database)
            get_ID = db_worker.getChatID(username_to)
            get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            getUserID = db_worker.getUserID(get_ID)
            getUserID = "{}".format(''.join(str(x) for x in getUserID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
            check_row = db_worker.check_row(day_delete, user_id, get_ID)
            if check_row == 0:
                bot.register_next_step_handler((bot.reply_to(message, 'oooops, на такой день прогулки не запланировано')), cancel)
            else:
                delete_from_db = db_worker.delete_row(day_delete, user_id, get_ID)
                db_worker.clear(user_id)
                bot.send_message(get_ID,
                         "У вас отменяется прогулка с {} {}  в {}".format(message.from_user.first_name,
                                                                          message.from_user.
                                                                          last_name, day_delete))
                read_from_DB = db_worker.read_my_data(username, get_ID)
                user_with = bot.get_chat_member(get_ID, getUserID)
                bot.send_message(message.chat.id,
                         "У вас запланированы прогулки с {} {} на следующие дни: {}  ".format(
                         user_with.user.first_name, user_with.user.last_name,
                             ''.join(str(x) for x in read_from_DB).
                                 replace('(', '').replace(')', '').
                                 replace('\'', '').replace(',', ', ')[:-2]))
                db_worker.close()
        elif (message.content_type != 'contact') & (message.text != '/cancel') & (message.text.startswith('@') == False):
            chat_id = message.chat.id
            msg = bot.reply_to(message, "Отправь файл контакта!")
            bot.register_next_step_handler(msg, reply_to_another_user_about_delete)
        elif str.lower(message.text) == '/cancel':
            msg = bot.reply_to(message, "Отправляю в начало, воспользуйся /start")
            bot.register_next_step_handler(msg, start)
    except Exception as e:
        bot.register_next_step_handler((bot.reply_to(message, 'oooops, попробуй еще раз ввести username')), reply_to_another_user_about_delete)


# @bot.message_handler(commands=['getid'])
# def getuserid(ID):  # Название функции не играет никакой роли, в принципе
#     userid = ID.chat.id


if __name__ == '__main__':
    bot.polling(none_stop=True)
