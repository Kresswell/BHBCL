import asyncio
import random

import aiogram
from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

import button
import config
import db

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot activated')
    db.start_db()


class TakeInt(StatesGroup):
    take1 = State()
    take2 = State()


class MassSend(StatesGroup):
    new_message = State()


@dp.message_handler(commands='start')
async def strt(message: types.Message):
    if message.from_user.id in config.ADMIN_ID:
        await bot.send_message(message.from_user.id, text=f"Вы администратор!",
                               reply_markup=button.admin_menu())
    elif message.from_user.id in db.all_user():
        await bot.send_message(message.from_user.id, text=f"Hi, {message.from_user.first_name}\n"
                                                          f"My name is AVIATOR SIGNALS BOT 😎\n"
                                                          f"I will give you signals to play AVIATOR 🍀\n"
                                                          f"If you're ready, press 👇🏻👇🏻👇🏻",
                               reply_markup=button.start_button())
        await TakeInt.take1.set()
    else:
        db.add_user_db(message.from_user.id)
        await bot.send_message(message.from_user.id, text=f"Hi, {message.from_user.first_name}\n"
                                                          f"My name is AVIATOR SIGNALS BOT 😎\n"
                                                          f"I will give you signals to play AVIATOR 🍀\n"
                                                          f"If you're ready, press 👇🏻👇🏻👇🏻",
                               reply_markup=button.start_button())
        await TakeInt.take1.set()


@dp.callback_query_handler(text='strt', state=TakeInt.take1)
async def strt_answer(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f"To synchronize with the bot, "
                                                   f"send me your AVIATOR account id 🫶🏻")
    await TakeInt.next()


@dp.message_handler(state=TakeInt.take2)
async def strt_state(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, text=f"Synchronization is in progress\n"
                                                      f"Please wait... ⌛️")
    await asyncio.sleep(6)
    await bot.send_message(message.from_user.id, text=f"Synchronization completed\n"
                                                      f"Status: ✅")
    await bot.send_message(message.from_user.id, text=f'*How to use signals?🤔\n\n'
                                                      f'Signals for AVIATOR will be issued when you click on'
                                                      f' the "Get Signal ✅" button\n\n'
                                                      f'After that, the bot will start picking up the time for'
                                                      f' you when you need to place a bet.😉\n\n'
                                                      f'Be ready🫡\n\n'
                                                      f'the bot will notify you with a signal at the moment'
                                                      f' when you need to place a bet.\n'
                                                      f'The coefficients can be different 🤑*',
                           reply_markup=button.menu(), parse_mode="Markdown")


@dp.callback_query_handler(text='instr')
async def instructions(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'*1. Press "New Signal" ✅\n'
                                                   f'2. Open the game and be ready to place a bet❤️‍🔥\n'
                                                   f'3. Wait for a message from the bot containing the '
                                                   f'bet time and auto cashout coefficient 📝\n'
                                                   f'4. Place a bet 💸\n'
                                                   f'5. Take the win💰💰💰\n'
                                                   f'6. Then repeat from the beginning♻\n\n'
                                                   f'️ ‼️‼️‼️The bot accuracy is 90%‼️‼️‼️*',
                           reply_markup=button.get_signal(), parse_mode="Markdown")


@dp.callback_query_handler(text='gtsgn')
async def get_signal(call: types.CallbackQuery):
    time = random.randint(20, 35)
    number = random.uniform(1.4, 2.25)
    coeff = (round(number, 2))
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Command accepted ✅\n'
                                                   f'The signal will be given within 2 minutes ⌛\n'
                                                   f'Don`t turn off bot notifications 📣')
    await asyncio.sleep(35)
    await bot.send_message(call.from_user.id, text=f'Signal found ❇')
    await bot.send_message(call.from_user.id, text=f'Bet in {time} seconds!✅\n'
                                                   f'Autocashout at {coeff} ❌', reply_markup=button.get_signal())


#######################################################################################################################
@dp.callback_query_handler(text='mssndd')
async def mass_send(call: types.CallbackQuery):
    if call.from_user.id in config.ADMIN_ID:
        print('true')
        await MassSend.new_message.set()
        await bot.send_message(call.from_user.id, text='Отправьте сообщение которое будет разослано',
                               reply_markup=button.cancel())


@dp.message_handler(text='Отмена', state=MassSend.new_message)
async def mass_send(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, text='Отменено!',
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=aiogram.types.ContentType.ANY,
                    state=MassSend.new_message)
async def mass_send(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, text='Отправка сообщения запущена!',
                           reply_markup=button.admin_menu())

    for i in db.all_user():
        try:
            await bot.copy_message(i,
                                   message.chat.id,
                                   message.message_id,
                                   caption=message.caption,
                                   reply_markup=message.reply_markup)

        except Exception as e:
            print(f'Username: {i}  Error: {e}')


#######################################################################################################################


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
