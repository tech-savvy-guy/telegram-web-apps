import os
import dotenv
import requests
dotenv.load_dotenv()

import flask
from flask import request
from flask import redirect
from flask import render_template

import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InputTextMessageContent
from telebot.types import InlineQueryResultArticle

from telebot.util import parse_web_app_data
from telebot.util import validate_web_app_data

app = flask.Flask(__name__, static_url_path="/static")
bot = telebot.TeleBot(os.getenv("API_TOKEN"), parse_mode="HTML")

@app.route('/')
def index():
    return "A collection of Telegram Mini Apps"

# ------------------- Demo Form ------------------- #

@app.route('/demoForm')
def demoForm():
    return flask.render_template("demoForm.html")

@app.route('/demoFormResponse', methods=["POST"])
def demoFormResponse():
    raw_data = request.json
    name = raw_data["name"]
    date = raw_data["date"]
    email = raw_data["email"]
    country = raw_data["country"]
    initData = raw_data["initData"]

    isValid = validate_web_app_data(bot.token, initData)

    if isValid:
        web_app_data = parse_web_app_data(bot.token, initData)
        query_id = web_app_data["query_id"]
        bot.answer_web_app_query(query_id, InlineQueryResultArticle(
            id=query_id, title="VERIFICATION FAILED!",
            	input_message_content=InputTextMessageContent(
                	f"<i>Demo Form:\n\nName: {name}\n\nBorn: {date}\n\
					\nEmail: {email}\n\nCountry: {country}</i>", parse_mode="HTML"),
            			reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(
                			"CLICK TO CONTINUE ✅", callback_data=f"confirm-{web_app_data['user']['id']}"))))

    return redirect("/")

# ------------------- Demo Form ------------------- #


# ------------------- Text Captcha ------------------- #

@app.route('/captcha')
def captcha():
    return flask.render_template("captcha.html")

@app.route('/captchaResponse', methods=['POST'])
def captchaResponse():
    raw_data = flask.request.json
    isbot = raw_data["isbot"]
    initData = raw_data["initData"]
    attempts = raw_data["attempts"]

    isValid = validate_web_app_data(bot.token, initData)

    if isValid:
        if not isbot:
            web_app_data = parse_web_app_data(bot.token, initData)
            query_id = web_app_data["query_id"]
            bot.answer_web_app_query(query_id, InlineQueryResultArticle(
                id=query_id, title="VERIFICATION PASSED!",
                input_message_content=InputTextMessageContent(
                    "<i>Captcha verification passed ✅\n\
					\nIt seems that you're indeed a human! 😉</i>",
                    parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
                        InlineKeyboardButton("CLICK TO CONTINUE ✅",
                            callback_data=f"confirm-{web_app_data['user']['id']}"))))
        else:
            if attempts == 3:
                web_app_data = parse_web_app_data(bot.token, initData)
                query_id = web_app_data["query_id"]
                bot.answer_web_app_query(query_id, InlineQueryResultArticle(
                    id=query_id, title="VERIFICATION FAILED!",
                    input_message_content=InputTextMessageContent(
                        "<i>Captcha verification failed ❌\n\
							\nI don't trust your human side! 🤔</i>",
                        parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
                        InlineKeyboardButton("CLICK TO CONTINUE ✅",
                            callback_data=f"confirm-{web_app_data['user']['id']}"))))

    return redirect("/")

# ------------------- Text Captcha ------------------- #


# ------------------- QR Code Scanner ------------------- #

@app.route('/qrCode')
def qrCode():
    return flask.render_template("qrCode.html")

@app.route('/qrCodeResponse', methods=["POST"])
def qrCodeResponse():
    raw_data = flask.request.json
    initData = raw_data["initData"]

    isValid = validate_web_app_data(bot.token, initData)

    if isValid:
        web_app_data = parse_web_app_data(bot.token, initData)

        query_id = web_app_data["query_id"]

        bot.answer_web_app_query(query_id, InlineQueryResultArticle(
            id=query_id, title="QR DETECTED!",
            input_message_content=InputTextMessageContent(
                f"<i>QR Code scanned successfully! 👇🏻\n\
				\n{raw_data['qr']}</i>", parse_mode="HTML"),
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("CLICK TO CONTINUE ✅",
                                     callback_data=f"confirm-{web_app_data['user']['id']}"))))

    return redirect("/")

# ------------------- QR Code Scanner ------------------- #


# ------------------- Google re-CAPTCHA ------------------- #

@app.route('/captchav2', methods=["GET", "POST"])
def captchaV2():

    if request.method == 'POST':

        recaptcha_response = request.form.get('g-recaptcha-response')

        data = {
            'secret': os.getenv("SECRET_KEY"),
            'response': recaptcha_response
        }
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        raw_data = request.form
        initData = raw_data["initData"]

        isValid = validate_web_app_data(bot.token, initData)

        if isValid:

            web_app_data = parse_web_app_data(bot.token, initData)
            query_id = web_app_data["query_id"]

            if result['success']:
                bot.answer_web_app_query(query_id, InlineQueryResultArticle(
                    id=query_id, title="VERIFICATION PASSED!",
                    input_message_content=InputTextMessageContent(
                        "<b><i>Captcha verification passed ✅\n\
					        \nIt seems that you're indeed a human! 😉</i></b>",
                        parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
                        InlineKeyboardButton("CLICK TO CONTINUE ✅",
                                             callback_data=f"confirm-{web_app_data['user']['id']}"))))
            else:

                bot.answer_web_app_query(query_id, InlineQueryResultArticle(
                    id=query_id, title="VERIFICATION FAILED!",
                    input_message_content=InputTextMessageContent(
                        "<b><i>Captcha verification failed ❌\n\
							\nI don't trust your human side! 🤔</i></b>",
                        parse_mode="HTML"), reply_markup=InlineKeyboardMarkup().row(
                        InlineKeyboardButton("CLICK TO CONTINUE ✅",
                                             callback_data=f"confirm-{web_app_data['user']['id']}"))))

        return redirect("/")

    return render_template('captchav2.html')

# ------------------- Google re-CAPTCHA ------------------- #


if __name__ == '__main__':
    app.run(host='0.0.0.0')
