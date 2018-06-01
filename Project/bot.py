
# -*- coding: utf-8 -*-
from telegram.ext import Updater, Filters
import telegram
from telegram.ext import MessageHandler, Filters
from telegram import (KeyboardButton)
from telegram import Bot 

updater = Updater(token='348973838:AAGsl8EojMDjcDxlin8tEtHa2MfPZlpJ4p0')
dispatcher = updater.dispatcher
'''
def echo(bot, update):
	message = update.message.text
	from teacher_get import get_teacher_name
	reply_text = get_teacher_name(message)
	bot.sendMessage(chat_id=update.message.chat_id, text=reply_text, parse_mode="Markdown")

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
updater.start_polling()
'''
import json
file = open('teacher_json.json', encoding = 'utf-8')
data = json.loads(file.read())
file.close()

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I am KBTUbot. Just send me teacher and I will show you the schedule of this room.")
from telegram.ext import CommandHandler, MessageHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
command_list_teachers = []
lite = 0
rite = lite+5
status = 0
for name in data:
		if name == '':
			continue
		command_list_teachers.append([name])
	
def teacher(bot, update):
	print(123)
	global data, status, lite, rite	
	status = 0
	name = command_list_teachers[lite:rite]
	lite+=5
	rite+=5

	print(name)
	name.append(['/teacher'])

	bot.sendMessage(chat_id = update.message.chat_id,text= 'teachers list')

	bot.sendMessage(chat_id = update.message.chat_id,text= 'teachers list', reply_markup = telegram.ReplyKeyboardMarkup(name))
	status+=1
	hand()

teacher_handler = CommandHandler('teacher', teacher)
dispatcher.add_handler(teacher_handler)

def hand(bot, update):
	global data
	global updates, updates1, status
	print('asd',status)
	comm = update.message.text
	
	if status == 1:
		updates = update.message.text
		print(updates)
		command_list_teachers_rooms = []
		for room in data[updates]:
			command_list_teachers_rooms.append([room])
		command_list_teachers_rooms.append(['/teacher'])

		bot.sendMessage(chat_id = update.message.chat_id,text = 'rooms', reply_markup=telegram.ReplyKeyboardMarkup(command_list_teachers_rooms) )
		status+=1
	if status == 2:
		updates1 = update.message.text
		print(updates1, updates)
		command_list_teachers_rooms_time = []
		print(data[updates][updates1])
		for room in data[updates][updates1]:
			print(room)
			bot.sendMessage(chat_id = update.message.chat_id, text = str(room) + '---->' + '|||'.join(data[updates][updates1][room]) )

# def join(bot, update, args):
# 	global data
# 	teacher_name = ' '.join(args)
# 	for args in :
# 	 count=0
# 	 count+=1
# 	 bot.sendMessage(chat_id = update.message.chat_id, text = count)

hand_handler = MessageHandler(Filters.text, hand)
dispatcher.add_handler(hand_handler)

updater.start_polling()