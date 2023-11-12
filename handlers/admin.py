from aiogram import types, Dispatcher
from create_bot import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove
from keyboards import kb_admin, kb_client

from motor.motor_asyncio import AsyncIOMotorClient

Coll = None


class AdminData(StatesGroup):
	adminName = State()
	adminPass = State()


async def dataIn(message: types.Message):
	await AdminData.adminName.set()
	await message.answer("Введіть логін:")


async def load_adminName(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['adminName'] = message.text
	await AdminData.next()
	await message.answer("Введіть пароль:")


async def admin_start(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['adminPass'] = message.text
			linkdb = "mongodb+srv://" + data['adminName'] + ":" + data[
				'adminPass'] + "@myclaster.wv6cw.mongodb.net/onua_time_table?retryWrites=true&w=majority"
			await message.delete()

		cluster = AsyncIOMotorClient(linkdb)
		global Coll
		Coll = cluster.onua_time_table
		test = Coll.lessonTimes
		await test.find_one({'_id': {'$eq': 1}})
		await bot.send_message(message.from_user.id, "Вітаю, мій господар.", reply_markup=kb_admin)

	except:
		await bot.send_message(message.from_user.id, "Помилка admin_start", reply_markup=kb_client)
	finally:
		await state.finish()


def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(dataIn, commands=['Адміністратор', 'Назад'], state=None)

	dp.register_message_handler(load_adminName, state=AdminData.adminName)
	dp.register_message_handler(admin_start, state=AdminData.adminPass)
