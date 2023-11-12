from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client

UserID = None


async def command_start(message: types.Message):
	try:
		global UserID
		UserID = message.from_user.id
		await bot.send_message(message.from_user.id, "Вітаю, студенте.", reply_markup=kb_client)
	except:
		await message.reply('Общение с ботом в ЛС, напишите ему:\nhttps://t.me/ONUA_Time_Table_Bot')


def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
