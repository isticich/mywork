import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
import pyqrcode as pq
from db import Database
import config as cfg

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if(not db.user_exists(message.from_user.id)):
            start_command = message.text
            referrer_id = str(start_command[7:])
            if str(referrer_id) != '':
                if str(referrer_id) != str(message.from_user.id):
                    db.add_user(message.from_user.id, referrer_id)
                    try:
                        await bot.send_message(referrer_id, 'По вашей ссылке зарегистрировался новый пользователь!')
                        bonus = db.user_bonus(referrer_id) + 1000
                        db.set_bonus(referrer_id, bonus)
                        await bot.send_message(referrer_id, 'За нового пользователя вам начислено: 1000 бонусов')
                    except:
                        pass
                else:
                    db.add_user(message.from_user.id)
                    await bot.send_message(message.from_user.id, 'Нельзя регистрироваться по своей ссылки!')
            else:
                db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, 'Укажите ваш ник')
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!', reply_markup=nav.mainMenu)


@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 1991898175:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(message.from_user.id, 'Успешная рассылка')


@dp.callback_query_handler(text='top_up')
async def top_up(callback: types.CallbackQuery):
    if db.user_bonus(callback.from_user.id) == 0:
        await callback.answer('Ошибка')
        await bot.send_message(callback.from_user.id, 'Нельзя использовать бонусы, если у вас их нет!')
    else:
        await callback.answer('Идет обработка ваших бонусов.\n Подождите пожалуйста')

        qr_code = pq.create(f'{db.user_bonus(callback.from_user.id)}')
        qr_code.png('code.png', scale=6)

        with open('code.png', 'rb') as photo:
            await bot.send_photo(callback.from_user.id, photo)
            await bot.send_message(callback.from_user.id, f'Ваш QRCODE готов!\n Покажите его менеджеру!')
        db.set_bonus(callback.from_user.id, 0)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'ПРОФИЛЬ':
            user_nickname = 'Ваш ник:' + db.get_nickname(message.from_user.id)
            await bot.send_message(message.from_user.id, user_nickname)
            await bot.send_message(message.from_user.id, f"Количество бонусов: {db.user_bonus(message.from_user.id)}", reply_markup=nav.topUpMenu)
        elif message.text == 'РЕФЕРАЛ':
            await bot.send_message(message.from_user.id, f'ID: {message.from_user.id}\nhttps://t.me/{cfg.BOT_NICKNAME}?start={message.from_user.id}\nКол-во рефе ралов: {db.count_reeferals(message.from_user.id)}')

        else:
            if db.get_signup(message.from_user.id) == 'setnickname':
                if(len(message.text)) > 15:
                    await bot.send_message(message.from_user.id, 'Никнейм не должен превышать 15 символов')
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, 'Вы вели запрещеный символ')
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, 'done')
                    await bot.send_message(message.from_user.id, 'Регистрация прошла успешно!!', reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, 'Что?')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)