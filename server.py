import re
import os
import json
import flask
import base64
import telebot
from PIL import Image
from io import BytesIO
from io import StringIO
from flask import request
from flask import redirect
from flask import send_file
from utils import parse_web_app_data
from utils import validate_web_app_data
from telebot.types import InputMediaPhoto
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InputTextMessageContent
from telebot.types import InlineQueryResultArticle
from telebot.types import InlineQueryResultPhoto

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


@app.route('/captcha')
def captcha():
	return flask.render_template("captcha.html")


@app.route('/paint')
def paint():
	return flask.render_template("paint.html")


@app.route('/qrCode')
def qrCode():
	return flask.render_template("qrCode.html")


@app.route('/qrCode-response', methods=["POST"])
def qrCode_response():
	raw_data = flask.request.json
	initData = raw_data["initData"]

	isValid = validate_web_app_data(API_TOKEN, initData)

	if isValid:
		web_app_data = parse_web_app_data(API_TOKEN, initData)

		query_id = web_app_data["query_id"]

		bot.answer_web_app_query(query_id, InlineQueryResultArticle(
			id=query_id, title="QR DETECTED!",
			input_message_content=InputTextMessageContent(
				f"<i><b>QR Code scanned successfully! 👇🏻</b>\n\
				\n{web_app_data['data']}</i>", parse_mode="HTML"),
					reply_markup=InlineKeyboardMarkup().row(
					InlineKeyboardButton("CLICK TO CONTINUE ✅",
						callback_data=f"confirm-{web_app_data['user']['id']}"))))		

@app.route('/paint-response', methods=["POST"])
def paint_response():
	raw_data = flask.request.json
	imageData = raw_data["imageData"]
	initData = raw_data["initData"]

	isValid = validate_web_app_data(API_TOKEN, initData)

	if isValid:
		web_app_data = parse_web_app_data(API_TOKEN, initData)
		query_id = web_app_data["query_id"]
		bot.answer_web_app_query(query_id, InlineQueryResultPhoto(
					id=query_id, photo_url=InputMediaPhoto(BytesIO(base64.b64decode(imageData))),
					reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(
						"CLICK TO CONTINUE ✅", callback_data=f"confirm-{web_app_data['user']['id']}"))))		
	
	return base64.encode(base64.b64decode(imageData))	# TODO: Fix download from client side!


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
		bot.answer_web_app_query(query_id, InlineQueryResultArticle(
					id=query_id, title="VERIFICATION FAILED!",
					input_message_content=InputTextMessageContent(
						f"<b><i>Demo Form:\n\nName: {name}\n\nBorn: {date}\n\
							\nEmail: {email}\n\nCountry: {country}</i></b>", parse_mode="HTML"),
					reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(
						"CLICK TO CONTINUE ✅", callback_data=f"confirm-{web_app_data['user']['id']}"))))

	return redirect("/")


@app.route('/captcha-response', methods=['POST'])
def captcha_response():
	raw_data = flask.request.json
	isbot = raw_data["isbot"]
	initData = raw_data["initData"]
	attempts = raw_data["attempts"]

	isValid = validate_web_app_data(API_TOKEN, initData)

	if isValid:		
		if not isbot:
			web_app_data = parse_web_app_data(API_TOKEN, initData)
			query_id = web_app_data["query_id"]
			bot.answer_web_app_query(query_id, InlineQueryResultArticle(
				id=query_id, title="VERIFICATION PASSED!",
				input_message_content=InputTextMessageContent(
					"<b><i>Captcha verification passed ✅\n\
					\nIt seems that you're indeed a human! 😉</i></b>",
					parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
						InlineKeyboardButton("CLICK TO CONTINUE ✅",
							callback_data=f"confirm-{web_app_data['user']['id']}"))))
		else:
			if attempts == 3:
				web_app_data = parse_web_app_data(API_TOKEN, initData)
				query_id = web_app_data["query_id"]
				bot.answer_web_app_query(query_id, InlineQueryResultArticle(
					id=query_id, title="VERIFICATION FAILED!",
					input_message_content=InputTextMessageContent(
						"<b><i>Captcha verification failed ❌\n\
							\nI don't trust your human side! 🤔</i></b>",
					parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
						InlineKeyboardButton("CLICK TO CONTINUE ✅",
							callback_data=f"confirm-{web_app_data['user']['id']}"))))

	return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT")))
