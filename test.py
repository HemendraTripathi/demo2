import telegram

bot = telegram.Bot(token='1051367701:AAHoGDs8rQzMmKpeaduSBOpMvzyB6RcDils')
buttons = [[telegram.InlineKeyboardButton("Approve",callback_data="--approve"),telegram.InlineKeyboardButton("Disapprove",callback_data="--disapprove"),telegram.InlineKeyboardButton("Cancel",callback_data="--cancel")]]
mark =  telegram.InlineKeyboardMarkup(buttons)
bot.send_message(chat_id=1107873730,text="test",reply_markup=mark)
