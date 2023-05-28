import os
import telebot
from telebot.types import WebAppInfo
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

web_apps = [
	{"label" : "Demo Forms", "link" : "https://telegram-web-apps.tk/demo-form"},
	{"label" : "Captcha", "link" : "https://telegram-web-apps.tk/captcha"},
	{"label" : "Paint", "link" : "https://telegram-web-apps.tk/paint"},
	{"label" : "QR Scanner", "link" : "https://telegram-web-apps.tk/qrCode"},
]

@bot.message_handler(commands=["start"])
def start(message):

	prev_button = InlineKeyboardButton("⬅️", callback_data="web-app:0")
	next_button = InlineKeyboardButton("➡️", callback_data="web-app:2")
	web_app_btn = InlineKeyboardButton(web_apps[0]["label"],
		web_app=WebAppInfo(web_apps[0]["link"]))

	bot.send_message(message.chat.id, "<b><i>Hey there! 😉\n\
		\nWanna see some cool Telegram Web Apps? 😎\n\
		\nBrowse using the butons below 👇🏻</i></b>",
		reply_markup=InlineKeyboardMarkup().row(
			prev_button, web_app_btn, next_button))


@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):

	_id, data = call.id, call.data

	if data[:7] == "web-app":
		index = int(data[8:])

		if index == 0:
			bot.answer_callback_query(_id, "⚠️  Start of list  ⚠️", show_alert=True)
		elif index > len(web_apps):
			bot.answer_callback_query(_id, "⚠️  End of list  ⚠️", show_alert=True)
		else:
			prev_button = InlineKeyboardButton("⬅️", callback_data=f"web-app:{index-1}")
			next_button = InlineKeyboardButton("➡️", callback_data=f"web-app:{index+1}")
			web_app_btn = InlineKeyboardButton(web_apps[index-1]["label"],
				web_app=WebAppInfo(web_apps[index-1]["link"]))		

			bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
				reply_markup=InlineKeyboardMarkup().row(
					prev_button, web_app_btn, next_button))
				
	elif data[:7] == "confirm":
		bot.send_message(int(data[8:]), "<b><i>Thanks for trying out the WebApp.\n\
			\nIn case you liked it, kindly star ⭐ the project on\
 <a href='https://github.com/TECH-SAVVY-GUY/telegram-web-apps'>GitHub</a>.\n\
			\nContributions are welcome! 😇</i></b>")
		bot.edit_message_reply_markup(inline_message_id=call.inline_message_id)

@bot.message_handler(commands=["help"])
def help(message):
	bot.send_message(message.chat.id, 
		"<b><i>To report a bug, please visit the\
 <a href='https://github.com/TECH-SAVVY-GUY/telegram-web-apps/issues'>issues</a> page on\
 <a href='https://github.com/TECH-SAVVY-GUY/telegram-web-apps'>GitHub</a>.\n\
			\nFor any other questions, contact developer ➜ @tech_savvy_guy</i></b>")

bot.infinity_polling(skip_pending=True)
