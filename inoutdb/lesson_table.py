from aiogram import types, Dispatcher
from create_bot import dp, bot

from inoutdb import time_table

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from inoutdb import time_table
from handlers import admin

import motor.motor_asyncio

from keyboards import kb_lt


class LessonData(StatesGroup):
	weekDay = State()
	maxLesson = State()
	Lesson = State()
	Link = State()


dayWeek = ''
maxCount = 0
Lessons = []
Links = []


async def startWeekMax(message: types.Message):
	Lessons.clear()
	Links.clear()
	await LessonData.weekDay.set()
	await message.answer("Формат вводу:(mon, tue, wed, thu, fri, sat, sun)\nВведіть день тижня:")


async def inputWeek(message: types.Message, state: FSMContext):
	global dayWeek
	async with state.proxy() as data:
		data['weekDay'] = message.text
		dayWeek = data['weekDay']
	await LessonData.next()
	await message.answer('Введіть кількість пар враховуючи "вікна" (підрахунок вести з першої пари):')


async def inputMaxLesson(message: types.Message, state: FSMContext):
	try:
		global maxCount
		async with state.proxy() as data:
			data['maxLesson'] = message.text
			maxCount = int(data['maxLesson'])
		await state.finish()
		await bot.send_message(message.from_user.id,
							   '***Введення занять***\nЯкщо "вікно", тоді введіть замість\nЗаняття:"-"\nКабінету:"0"',
							   reply_markup=kb_lt)
	except:
		await message.answer("Невірно введені дані")


async def startLessonInput(message: types.Message):
	await LessonData.Lesson.set()

	await message.answer(f"** Ввод {len(Lessons)+1}-ї пари **")
	await message.answer("Назва заняття:")


async def inLesson(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['Lesson'] = message.text
		Lessons.append(data['Lesson'])

	await LessonData.next()
	await message.answer("Кабінет:")


async def inCab(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		try:
			data['Link'] = message.text
			Links.append(data['Link'])
		except:
			await message.answer("Невірно введені дані")

		if len(Lessons) > len(Links):
			await message.answer("Дані введено не повністю.\nВведені дані було видалено, спробуйте ввести пару знову.")
			Lessons.pop(len(Lessons) - 1)

		elif len(Lessons) < len(Links):
			await message.answer("Дані введено не повністю.\nВведені дані було видалено, спробуйте ввести пару знову.")
			Links.pop(len(Links) - 1)

		elif len(Lessons) == maxCount:
			await message.answer("Ввод занять закінчено!")

		elif len(Lessons) > maxCount:
			await message.answer(
				"Зайві пари було видалено!\nДля збільшення кількості пар перезайдіть у меню правки розкладу і заповніть форму знову.")

			Lessons.pop(len(Lessons) - 1)
			Links.pop(len(Links) - 1)
	await state.finish()


async def lessonInDB(message: types.Message):
	try:
		Coll = None

		if dayWeek == "mon":
			Coll = admin.Coll.mon
		elif dayWeek == "tue":
			Coll = admin.Coll.tue
		elif dayWeek == "wed":
			Coll = admin.Coll.wed
		elif dayWeek == "thu":
			Coll = admin.Coll.thu
		elif dayWeek == "fri":
			Coll = admin.Coll.fri
		elif dayWeek == "sat":
			Coll = admin.Coll.sat
		elif dayWeek == "sun":
			Coll = admin.Coll.sun
		else:
			await message.answer("Невірно введено день тижня!")

		lessonStart = await time_table.getLessonStartTimes()
		lessonEnd = await time_table.getLessonEndTimes()
		Coll.delete_many({})
		for i in range(len(Lessons)):
			Coll.insert_one({
				"_id": i + 1,
				"lessonStart": lessonStart[i],
				"lessonEnd": lessonEnd[i],
				"Lesson": Lessons[i],
				"Link": Links[i]
			})
		await message.answer("Дані збережено!")
	except:
		await message.answer("У вас немає доступу до цієї операції!")


def register_handlers_lesson_table(dp: Dispatcher):
	dp.register_message_handler(startWeekMax, commands=['Правити_Розклад', 'Наступний_день'], state=None)
	dp.register_message_handler(inputWeek, state=LessonData.weekDay)
	dp.register_message_handler(inputMaxLesson, state=LessonData.maxLesson)


def register_handlers_lesson_table_input(dp: Dispatcher):
	dp.register_message_handler(startLessonInput, commands=['Додати_пару'], state=None)
	dp.register_message_handler(inLesson, state=LessonData.Lesson)
	dp.register_message_handler(inCab, state=LessonData.Link)


def register_handlers_lesson_table_indb(dp: Dispatcher):
	dp.register_message_handler(lessonInDB, commands=['Вставити_пари'])
