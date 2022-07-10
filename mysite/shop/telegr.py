import requests
import telebot

API_KEY = 'your_API_key_here'
CHAT_ID = 'Your_chat_ID_here'

def tel_bot_send_text(msg):
    """Working using requests library. Test example"""
    send_text = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + msg

    res = requests.get(send_text)

    return res.json()

bot = telebot.TeleBot(API_KEY)

def telbot_send_msg(msg):
    """Working using pytelegrambotapi. Sending msg to selected chat."""
    bot.send_message(CHAT_ID, msg)