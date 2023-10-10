import os
import dotenv
dotenv.load_dotenv()

import telebot
from telebot.types import WebAppInfo
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

bot = telebot.TeleBot(os.getenv('API_TOKEN'), parse_mode="HTML")

web_apps = [
	{"label" : "Demo Forms", "link" : "https://your-server.domain/demoForm"},
	{"label" : "CAPTCHA", "link" : "https://your-server.domain/captcha"},
	{"label" : "QR Code", "link" : "https://your-server.domain/qrCode"},
	{"label" : "re-CAPTCHA", "link" : "https://your-server.domain/captchav2"},
]

@bot.message_handler(commands=["start"])
def start(message):

	markup = InlineKeyboardMarkup()
	markup.row(InlineKeyboardButton(web_apps[0]["label"],
		web_app=WebAppInfo(web_apps[0]["link"])))
	markup.row(
		InlineKeyboardButton("⬅️", callback_data="web-app:0"),
		InlineKeyboardButton("➡️", callback_data="web-app:2")
	)

	bot.send_message(message.chat.id, "<i>Hey there! "
		"Wanna see some cool Telegram Web Apps? 🔥\n\n"
		"Browse using the butons below 👇🏻</i>", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call): 

	_id, data = call.id, call.data

	if data[:7] == "web-app":
		index = int(data[8:])

		if index == 0:
			bot.answer_callback_query(_id, "Oops! Start of list!", show_alert=True)
		elif index > len(web_apps):
			bot.answer_callback_query(_id, "Oops! End of list!", show_alert=True)
		else:
			prev_button = InlineKeyboardButton("⬅️", callback_data=f"web-app:{index-1}")
			next_button = InlineKeyboardButton("➡️", callback_data=f"web-app:{index+1}")
			web_app_btn = InlineKeyboardButton(web_apps[index-1]["label"],
				web_app=WebAppInfo(web_apps[index-1]["link"]))		

			markup = InlineKeyboardMarkup()
			markup.row(web_app_btn)
			markup.row(prev_button, next_button)

			bot.edit_message_reply_markup(
				call.message.chat.id,
					call.message.id, reply_markup=markup)
				
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

if __name__ == "__main__":
	print(f'@{bot.get_me().username} is up and running! 🚀')
	bot.infinity_polling(skip_pending=True)
