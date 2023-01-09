from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton("ПРОФИЛЬ")
btnsub = KeyboardButton("РЕФЕРАЛ")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnsub)

btnTopUp = InlineKeyboardButton(text='Использовать', callback_data='top_up')
topUpMenu = InlineKeyboardMarkup(row_width=1)
topUpMenu.insert(btnTopUp)