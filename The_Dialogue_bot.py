import random
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

token = 'token'
url = 'https://api.telegram.org/bot{}/'.format(token)
updater = Updater(token=token, use_context=True)

article_en = 'http://www.the-dialogue.com/en/en'       # 98
article_by = 'http://www.the-dialogue.com/by/by'       # 98
article_ru = 'http://www.the-dialogue.com/ru'          # 98
article_ua = 'http://www.the-dialogue.com/ua/ua'       # 13

def start(update, context):
    user_name = update.message.from_user['first_name']
    start_message = f"Hi {user_name}!\n\n" \
                    "I'm The Dialogue bot, I will send you a random article!\n" \
                    "Try /help for list of commands."
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)

def help(update, context):
    help_message = "I can send you a random article from <a href='the-dialogue.com'>The Dialogue</a> website.\n\n" \
                   "<b>List of commands</b>\n" \
                   "/start - start message\n" \
                   "/lang - choose language of article\n" \
                   "/help - list of commands\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message, parse_mode='HTML')

def lang(update, context):
    kb = [[KeyboardButton('/ru 🇷🇺'),
           KeyboardButton('/by 🇧🇾'),
           KeyboardButton('/ua 🇺🇦'),
           KeyboardButton('/en 🇬🇧')]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Choose language!',
                             reply_markup=kb_markup, parse_mode='HTML')

def by(update, context):
    bel_message = "Ваш выпадковы артыкул на беларускай мове:\n\n" \
                  f"{article_by + str(random.randint(1, 98))}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=bel_message)

def ru(update, context):
    rus_message = "Ваша случайная статья на русском языке:\n\n" \
                  f"{article_ru + str(random.randint(1, 98))}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=rus_message)

def ua(update, context):
    ukr_message = "Ваша випадкова стаття українською мовою:\n\n" \
                      f"{article_ua + str(random.randint(1, 13))}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=ukr_message)

def en(update, context):
    eng_message = "Your random article in english:\n\n" \
                  f"{article_en + str(random.randint(1, 98))}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=eng_message)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
lang_handler = CommandHandler('lang', lang)
by_handler = CommandHandler('by', by)
ru_handler = CommandHandler('ru', ru)
ua_handler = CommandHandler('ua', ua)
en_handler = CommandHandler('en', en)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(lang_handler)
updater.dispatcher.add_handler(by_handler)
updater.dispatcher.add_handler(ru_handler)
updater.dispatcher.add_handler(ua_handler)
updater.dispatcher.add_handler(en_handler)
updater.start_polling()
