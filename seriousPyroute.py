#!/usr/bin/env python3

import telegram
import random
import time
import os
import sys
from datetime import datetime
from keyboards_for_voting import vote, button_vote
from telegram.ext import CommandHandler
from telegram.ext import BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import ParseMode, Message, Chat, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, \
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler

#Add the ids of the admins bellow
#ADMINS = []
verbs = ['NOT ENOUGH PRIVILEGES,','YOU NEED ROOT PERMISSIONS,', 'SORRY, THE COMMAND IS FOR ADMINS ONLY', 'CONTACT AN ADMIN TO EXECUTE THAT COMMAND,']
verbs2 = ["TELL ME SIR",'AT YOUR SERVICE SIR','AT YOUR ORDERS SIR']
badwords=["pinche","puta","puto","verga","culero","culera","coño","ojete","pendejo","culo","chingado","chigada","chingar","chinga"]
TOKEN = ''
bot = telegram.Bot(token=TOKEN)
print(bot.get_me())

#Date and hour
date = datetime.now().strftime("%Y-%m-%d")
hourmeeting = datetime.now().strftime("%H:%M")

#Start meeting funkshun
def start(bot, update):  
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING)
    pin =update.message.from_user.username
    print ("STARTED: ")
    user_id = update.effective_user.id
    if user_id in ADMINS:
        print ("Meeting has started at *"+hourmeeting+"*""")
        bot.sendMessage(update.message.chat_id, text="Meeting has started at *{}*".format(hourmeeting) ,parse_mode="Markdown")
    if user_id not in ADMINS:
        uname = (random.choice(verbs))
        print("Unauthorized access denied for {}.".format(user_id))
        bot.send_message(update.message.chat_id, text= (uname))    

#Stop meeting funkshun
def stop(bot, update): 
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING) 
    print ("STARTED: ")
    user_id = update.effective_user.id
    if user_id in ADMINS:
        print ("Meeting has stopped at *"+hourmeeting+"*""")
        bot.sendMessage(update.message.chat_id, text="Meeting has stoped at *{}*".format(hourmeeting) ,parse_mode="Markdown")
    if user_id not in ADMINS:
        #random.seed = (os.urandom(1024))
        uname = (random.choice(verbs))
        print("Unauthorized access denied for {}.".format(user_id))
        bot.send_message(update.message.chat_id, text= (uname))
        
# Help funkshun
def ayuda(bot, update):
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING) 
    user_id = update.effective_user.id
    print (user_id)
    print ("PLEH")
    bot.sendMessage(chat_id=update.message.chat_id, text="*HELP MENU:*\n"+\
        "################\n"+\
        "*COMMANDS:*\n"+\
        "start: start meeting\n"\
        "stop: stop meeting",parse_mode=telegram.ParseMode.MARKDOWN)
    
# Restart BOT funkshun
def restart(bot, update):
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    #print ("BOT RESTARTED")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)
    txt =((str(pin) + (".txt")))
    #os.remove(txt)

# Assign ticket funkshun
def assign(bot, update, args):
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING)
    user_id = update.effective_user.id
    if user_id in ADMINS:
        user_says = " ".join(args)
        if (user_says.split(' ')[0]).isnumeric():
            update.message.reply_text("*Ticket* "+user_says.split(' ')[0]+" *has been assigned to: *" + user_says.split(' ')[1], parse_mode="Markdown")
            nkey = user_says.split(' ')[1]
            nvalue = user_says.split(' ')[0]
            TICKETS[nkey]=nvalue
            print(nkey)
            print(nvalue)
            with open (nvalue+".txt", "w") as file:
                file.write (date+"\n")
                file.write (hourmeeting+"\n")
                file.write (nkey+"\n")
                file.write (nvalue+"\n")
                file.write ("-----STATUS-----"+"\n")
                file.write ("OPEN")
            with open ("log.txt", "a") as file:
                file.write (date+"\n")
                file.write (hourmeeting+"\n")
                file.write (nkey+"\n")
                file.write ("CREATED "+(nvalue+".txt\n"))
                file.write ("-----EOL-----")
        else:
            update.message.reply_text("*PLEASE ASSIGN A VALID TICKET-ID*", parse_mode="Markdown")
    if user_id not in ADMINS:
        uname = (random.choice(verbs))
        print("Unauthorized access denied for {}.".format(user_id))
        bot.send_message(update.message.chat_id, text= (uname))  

# Ticket Status funkshun
def status(bot, update, args):
    bot.send_chat_action(update.message.chat_id, action=telegram.ChatAction.TYPING)
    user_id = update.effective_user.id
    user_says = " ".join(args)
    if user_id in ADMINS:
        print(user_says+".txt")
        with open (user_says+".txt", "r") as file:
            r=file.readlines()
            bot.send_message(update.message.chat_id, text="*STATUS: *"+r[5]+"\n"+"*ASSIGNED TO: *"+r[2]+"\n"+"*CREATED:* "+r[0] ,parse_mode="Markdown")
    if user_id not in ADMINS:
        uname = (random.choice(verbs))
        print("Unauthorized access denied for {}.".format(user_id))
        bot.send_message(update.message.chat_id, text= (uname))

# def kb(bot, update):
#     keyboard = [[InlineKeyboardButton("Assign", callback_data='1'),
#                 InlineKeyboardButton("Start Meeting", callback_data='2'),
#                 InlineKeyboardButton("Stop Meeting", callback_data='3'),
#                 InlineKeyboardButton("Verbose Mode", callback_data='4'),
#                 InlineKeyboardButton("Debug Mode", callback_data='5'),
#                 InlineKeyboardButton("Placeholder", callback_data='6')],
#                 [InlineKeyboardButton("Placeholder2", callback_data='7')]]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     update.message.reply_text('Please choose:', reply_markup=reply_markup)

# def button(bot, update):
#     query = update.callback_query
#     print(query)

#     bot.edit_message_text(text="Selected option: {}".format(query.data),
#                           chat_id=query.message.chat_id,
#                           message_id=query.message.message_id)
def menu(bot,update):
    print("DEBUG")
    vote()
    button_vote()

def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.getChatAdministrators(chat_id)]

def echo(bot, update):
    msg = update.message.text
    msge= msg.lower()
    msgc=msge.split(" ")
    for i in msgc: 
        if i in badwords: 
            bot.send_message(update.message.chat_id, text= ("Hey, don't talk that way! Watch your language, this is a Kids Safe Zone! "))
        if (i == "bot"):
            uname2 = (random.choice(verbs2))
            bot.send_message(update.message.chat_id, text= (uname2))

def shits_on_fire_yo(self, update, error):
    logger.warning('ATTENTION this:"%s" caused this error "%s"', update, error)

def main():
    
    #updater = Updater()
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(CommandHandler('?', ayuda)) 
    updater.dispatcher.add_handler(CommandHandler('r', restart))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CommandHandler('assign', assign, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('status', status, pass_args=True))
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_error_handler(shits_on_fire_yo)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

#unused
# query = update.callback_query
#     print(query)
#     with open ("query.txt", "a") as file:
#                 file.write (date+"\n")
#                 file.write (hourmeeting+"\n")
#                 file.write (query+"\n")
#                 file.write ("-----EOL-----")