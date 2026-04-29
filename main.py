import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot("8734845651:AAHdHINPlLF2H-Whh5iEbERrzEYZWHwXglY")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Go to the website')
    btn2 = types.KeyboardButton('Instagram')
    markup.add(btn1,btn2)
    bot.send_message(message.chat.id,'Hello',reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Go to the website':
        bot.send_message(message.chat.id,'SBS')
    elif message.text == 'Instagram':
        bot.send_message(message.chat.id,'Instagram')

@bot.message_handler(commands=['website','site'])
def website(message):
    webbrowser.open_new('https://www.instagram.com/sxodim.astana?igsh=MWxnbXg1Z3M3OWpnNA==')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to the website', url='https://2gis.ru/geo/9570771978420226/71.443112,51.129547')
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton('Delete picture', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Edit picture', callback_data='edit')
    markup.add(btn2,btn3)
    file = open('./SBSlogo.jpeg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)


    bot.reply_to(message,'What a great picture?',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)



@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,'Welcome to Step By Step Astana!')

@bot.message_handler(commands=['hello'])
def main(message):
    bot.send_message(message.chat.id,f'Hello, {message.from_user.first_name}')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'id':
        bot.reply_to(message, f' ID: {message.from_user.id}')


bot.polling(none_stop=True)