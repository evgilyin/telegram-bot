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
	mybot.job_queue.run_daily(send_updates, time=datetime.datetime.strptime('8:34PM', '%I:%M%p').time(), days=(1,))
	dp.add_handler(CommandHandler("get_table", get_table))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	dp.add_handler(CommandHandler("subscribe", subscribe))
	dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
	mybot.start_polling()
	mybot.idle()

def talk_to_me(bot, update):
	user_text = "{}, я не понимаю, что ты мне говоришь! Но чтобы получить таблицу лиги СУПЕРКАТКА, то используй команду /get_table\nЧтобы подписаться на уведомления о том, что пора бы уже собирать состав, то используй команду /subscribe".format(update.message.chat.username)
	logging.info("User: %s, Message: %s", update.message.chat.username, update.message.text)
	update.message.reply_text(user_text)

def get_table(bot, update):
	text = get_info('https://www.sports.ru/fantasy/football/league/140288.html')
	logging.info(text)
	update.message.reply_text(text)

def subscribe(bot, update):
	subscribers.add(update.message.chat_id)
	update.message.reply_text("Вы подписались на уведомления, наберите /unsubscribe чтобы отписаться")

def unsubscribe(bot, update):
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        update.message.reply_text("Ну и зачем? Забудешь сделать трансферы - проиграешь в общем зачете!")
    else:
        update.message.reply_text("Вы не подписаны, наберите /subscribe чтобы подписаться")

def send_updates(bot, job):
	for chat_id in subscribers:
		bot.sendMessage(chat_id=chat_id, text="Пора бы уже собирать состав. Скоро начнется тур!")

main()