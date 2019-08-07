from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import settings
import requests
import datetime
from fantasy import get_info
from bs4 import BeautifulSoup

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

subscribers = set()

def main():
	mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(CommandHandler("get_table", get_table))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	dp.add_handler(CommandHandler("subscribe", callback_timer, pass_job_queue=True))
	dp.add_handler(CommandHandler("trash_talk", trash_talk))
	mybot.start_polling()
	mybot.idle()

def greet_user(bot, update):
	logging.info("User: %s: вызван /start", update.message.chat.username)
	user_text = "Привет, {}! Это бот, с помощью которого ты сможешь смотреть свой прогресс в Fantasy-футболе на sports.ru\nВот что я умею делать:\n- чтобы получить таблицу лиги СУПЕРКАТКА, используй команду /get_table\n- чтобы подписаться на уведомления, используй команду /subscribe\n- если ты хочешь устроить с ботом небольшой ТРЭШ-ТОК, используй команду /trash_talk".format(update.message.chat.first_name)
	update.message.reply_text(user_text)

def talk_to_me(bot, update):
	user_text = "{}, я не понимаю, что ты мне говоришь! Но чтобы получить таблицу лиги СУПЕРКАТКА, используй команду /get_table\nЧтобы подписаться на уведомления, то используй команду /subscribe - я сообщу тебе, когда пора собирать состав".format(update.message.chat.first_name)
	logging.info("User: %s, Message: %s", update.message.chat.username, update.message.text)
	update.message.reply_text(user_text)

def get_table(bot, update):
	text = get_info('https://www.sports.ru/fantasy/football/league/140288.html')
	logging.info("User: %s: вызван /get_table", update.message.chat.username)
	update.message.reply_text(text)

def callback_timer(bot, update, job_queue):
	subscribers.add(update.message.chat_id)
	logging.info("User: %s: вызван /subscribe", update.message.chat.username)
	update.message.reply_text("Вы подписались на уведомления бота!")
	job_repeat = job_queue.run_daily(callback_alarm, time=datetime.datetime.strptime('10:00AM', '%I:%M%p').time(), days=(4,), context=update.message.chat_id)

def callback_alarm(bot, job):
	for chat_id in subscribers:
		bot.sendMessage(chat_id=chat_id, text='Братишка, пора бы собирать команду. Дедлайн близко')
		logging.info("User: %s: отправлено напоминание", update.message.chat.username)

def trash_talk(bot, update):
	logging.info("User: %s: вызван /trash_talk", update.message.chat.username)
	update.message.reply_text("Пока бот обучается устраивать ТРЭШ-ТОК. Подожди немного и скоро он покроет тебя хуями")

main()