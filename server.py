import os
import flask
import telebot
from flask import request
from flask import redirect
from utils import parse_web_app_data
from utils import validate_web_app_data
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InputTextMessageContent
from telebot.types import InlineQueryResultArticle

API_TOKEN = os.getenv("API_TOKEN")

app = flask.Flask(__name__)
bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

@app.route('/')
def index():
	return "Collection of Web Apps"


@app.errorhandler(404)
def error_404(e):
	return flask.render_template("error-404.html")


@app.route('/demo-form')
def demo_form():
	return flask.render_template("demo-form.html")


@app.route('/demo-form-response', methods=["POST"])
def demo_form_response():
	raw_data = request.json
	name = raw_data["name"]
	date = raw_data["date"]
	email = raw_data["email"]
	country = raw_data["country"]
	initData = raw_data["initData"]

	isValid = validate_web_app_data(API_TOKEN, initData)

	if isValid:
		web_app_data = parse_web_app_data(API_TOKEN, initData)
		query_id = web_app_data["query_id"]
		print(web_app_data['user'].id)	# Test - 1
		bot.answer_web_app_query(query_id, InlineQueryResultArticle(
					id=query_id, title="VERIFICATION FAILED!",
					input_message_content=InputTextMessageContent(
						f"<b><i>Demo Form:\n\nName: {name}\n\nBorn: {date}\n\
							\nEmail: {email}\n\nCountry: {country}</i></b>", parse_mode="HTML"),
					reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(
						"CLICK TO CONFIRM ✅", callback_data="confirm"))))

	return redirect("/")

if __name__ == '__main__':
	app.run(debug=True)
