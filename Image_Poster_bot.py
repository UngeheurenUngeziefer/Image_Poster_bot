from telepot.loop import MessageLoop
from time import sleep
import telepot
import glob
import os

token = 'token'
url = 'https://api.telegram.org/bot{}/'.format(token)
# proxies = {'https': '169.51.80.228:3128', 'http': '159.203.82.173:3128'}
# telepot.api.set_proxy('https://169.51.80.228:3128')
PosterBot = telepot.Bot(token)

def answer_to_start():
    global message_pm
    global chat_id
    message_pm = (PosterBot.getUpdates()[-1]['message']['text'])
    name = (PosterBot.getUpdates()[-1]['message']['from']['first_name'])
    chat_id = (PosterBot.getUpdates()[-1]['message']['from']['id'])
    start_message = f"Hello {name}! I'm PosterBot!\n" \
                    "I'm post all images from directory to telegram channel!\n\n" \
                    "Now I need You to add me to the channel as an administrator.\n" \
                    "And then post key message on the channel (for example 'HERE')." \
                    "\nLater you may delete the message.\n\n"
    if message_pm == '/start':
        PosterBot.sendMessage(chat_id, start_message)

def get_channel_id():
    global channel_id
    channel_id = ((PosterBot.getUpdates())[-1]['channel_post']['chat']['id'])
    channel_name = ((PosterBot.getUpdates())[-1]['channel_post']['chat']['title'])
    channel_id_message = 'Channel \'{}\' admitted you may delete key message!\n\n' \
                         'Finally, send me a directory with your images like this:\n' \
                         '/dir C:\\Users\\User\\Memes\n\n' \
                         'Make sure that you have only images in folder!'.format(channel_name)
    if channel_id:
        PosterBot.sendMessage(chat_id, channel_id_message)

def answer_to_dir():
    dir_address = message_pm[5:]
    if message_pm[:4] == '/dir' and len(message_pm) > 6:
        PosterBot.sendMessage(chat_id, r"'" + dir_address + r"'" + ' - address admitted')
        PosterBot.sendMessage(chat_id, 'Now You may start /start_posting!')
        global saved_dir_address
        saved_dir_address = str(dir_address)

def img_poster():
    img_list = []
    addresses_list = []
    os.chdir(saved_dir_address)
    for file in glob.glob("*.*"):
        img_list.append(file)
    for img in img_list:
        addresses_list.append(
            saved_dir_address + '\\' + img)  # addresses list contain ['address_1', 'address_N' ...]
    for path in addresses_list:
        if message_pm == '/start_posting':
            PosterBot.sendPhoto(channel_id, photo=open(path, 'rb'))
            sleep(3)  # sleep for 3 sec - telegram limit 20 per minute

def other_messages():
    if message_pm[:5] != '/dir ':
        if message_pm != '/start' and message_pm != '/start_posting':
            PosterBot.sendMessage(chat_id, "I can help you post images from directory on your PC "
                                       "to telegram channel.\n\n<b>Bot commands</b>\n/start - first instructions\n/start_posting"
                                       " - start posting images to channel\n/dir C:\\Users\\User"
                                       "\\Example - submit your directory in this format\n\n"
                                       "Any other messages call this topic!", parse_mode="HTML")
        else:
            pass

def handler(message):
    content_type, chat_type, chat_id_console = telepot.glance(message)
    print(content_type, chat_type, chat_id_console)
    if content_type == 'text' and chat_type == 'private':
        try:
            answer_to_start()
        except (KeyError, IndexError):
            print('tried to run answer_to_start!')
        try:
            answer_to_dir()
        except NameError:
            print('tried to get DIR!')
        try:
            img_poster()
        except NameError:
            print('tried to get img_poster!')
        try:
            other_messages()
        except NameError:
            pass
    elif content_type == 'text' and chat_type == 'channel':
        try:
            get_channel_id()
        except (KeyError, IndexError):
            print('tried to get channel_id!')

MessageLoop(PosterBot, handler).run_as_thread()
print('Listening ...')

while 1:
    sleep(10)
