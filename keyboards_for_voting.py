import logging
import telegram  
import random
import time
import os
import sys
from datetime import datetime
from telegram.ext import Updater  
from telegram.ext import CommandHandler
from telegram.ext import BaseFilter
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import ParseMode, Message, Chat, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, \
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler

updater = Updater("530028839:AAH9_R2TS9rPi2eYMKwO1TC8V2j1wkYuO08")

def vote(bot, update):
	
    keyboard = [[InlineKeyboardButton("Assign", callback_data='1'),
                InlineKeyboardButton("Start Meeting", callback_data='2'),
                InlineKeyboardButton("Stop Meeting", callback_data='3'),
                InlineKeyboardButton("Verbose Mode", callback_data='4'),
                InlineKeyboardButton("Debug Mode", callback_data='5'),
                InlineKeyboardButton("Placeholder", callback_data='6')],
                [InlineKeyboardButton("Placeholder2", callback_data='7')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button_vote(bot, update):
    query = update.callback_query
    print(query)

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

updater.dispatcher.add_handler(CommandHandler('vote', vote))
updater.dispatcher.add_handler(CallbackQueryHandler(button_vote))

