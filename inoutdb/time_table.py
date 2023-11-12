from aiogram import types, Dispatcher
from create_bot import dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from datetime import datetime
from handlers import admin
import motor.motor_asyncio

from keyboards import kb_tt


class TimeData(StatesGroup):
	maxLesson = State()
	startTime = State()
	endTime = State()


maxCount = 0
lessonStartTime = []
lessonEndTime = []


async def getLessonStartTimes():
	Collection = admin.Coll.lessonTimes
	lessonStartTime.clear()
	i = 1
	while await Collection.find_one({'_id': {'$eq': i}}) is not None:
		a = await Collection.find_one({'_id': {'$eq': i}})
		lessonStartTime.append(a['lessonStart'])
		i += 1
	return lessonStartTime


async def getLessonEndTimes():
	Collection = admin.Coll.lessonTimes
	lessonEndTime.clear()
	i = 1
	while await Collection.find_one({'_id': {'$eq': i}}) is not None:
		a = await Collection.find_one({'_id': {'$eq': i}})
		lessonEndTime.append(a['lessonEnd'])
		i += 1
	return lessonEndTime


async def inpuTime(message: types.Message):
	lessonStartTime.clear()
	lessonEndTime.clear()
	await TimeData.maxLesson.set()
	await message.answer("Введіть максимальну кількість занять:")


async def inputMany(message: types.Message, state: FSMContext):
	try:
		global maxCount
		async with state.proxy() as data:
			data['maxLesson'] = message.text
			maxCount = int(data['maxLesson'])
		await state.finish()
		await bot.send_message(message.from_user.id, "***Введення часів***", reply_markup=kb_tt)

	except:
		await message.answer("Невірно введені дані:")


async def startInput(message: types.Message):
	await TimeData.startTime.set()

	await message.answer("Дані часу занять вводяться у форматі HH:MM")
	await message.answer(f"Початок {len(lessonStartTime)+1}-ї пари:")


async def inStart(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['startTime'] = message.text
		try:
			lessonStartTime.append(datetime.time(datetime.strptime(data['startTime'] + ":00", "%H:%M:%S")))
		except:
			await message.answer("Невірний формат вводу часу.\nСпробуйте ввести це заняття знову.")

	await TimeData.next()
	await message.answer(f"Кінець {len(lessonEndTime)+1}-ї пари:")


async def inEnd(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['endTime'] = message.text
		try:
			lessonEndTime.append(datetime.time(datetime.strptime(data['endTime'] + ":00", "%H:%M:%S")))
		except:
			await message.answer("Невірний формат вводу часу.\nСпробуйте ввести це заняття знову.")

		if len(lessonStartTime) > len(lessonEndTime):
			await message.answer("Дані введено не повністю.\nВведені дані було видалено, спробуйте ввести час знову.")
			lessonStartTime.pop(len(lessonStartTime) - 1)

		elif len(lessonStartTime) < len(lessonEndTime):
			await message.answer("Дані введено не повністю.\nВведені дані було видалено, спробуйте ввести час знову.")
			lessonEndTime.pop(len(lessonEndTime) - 1)

		elif len(lessonEndTime) == maxCount:
			await message.answer("Ввод даних часу закінчено!")

		elif len(lessonEndTime) > maxCount:
			await message.answer(
				"Зайвий час було видалено!\nДля збільшення кількості пар перезайдіть у меню правки часу і заповніть форму знову.")

			lessonStartTime.pop(len(lessonStartTime) - 1)
			lessonEndTime.pop(len(lessonEndTime) - 1)
	await state.finish()


async def timeInDB(message: types.Message):
	try:
		Coll = admin.Coll.lessonTimes
		Coll.delete_many({})
		for i in range(len(lessonStartTime)):
			Coll.insert_one({
				"_id": i + 1,
				"lessonStart": str(lessonStartTime[i]),
				"lessonEnd": str(lessonEndTime[i])
			})
		await message.answer("Дані збережено!")
	except:
		await message.answer("У вас немає доступу до цієї операції!")


def register_handlers_time_table(dp: Dispatcher):
	dp.register_message_handler(inpuTime, commands=['Правити_Часи'], state=None)
	dp.register_message_handler(inputMany, state=TimeData.maxLesson)


def register_handlers_time_table_input(dp: Dispatcher):
	dp.register_message_handler(startInput, commands=['Додати_час'], state=None)
	dp.register_message_handler(inStart, state=TimeData.startTime)
	dp.register_message_handler(inEnd, state=TimeData.endTime)


def register_handlers_time_table_indb(dp: Dispatcher):
	dp.register_message_handler(timeInDB, commands=['Вставити_часи'])
