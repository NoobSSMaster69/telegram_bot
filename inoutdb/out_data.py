from aiogram import types, Dispatcher
from create_bot import dp, bot, cluster

from datetime import datetime
from handlers import admin
import motor.motor_asyncio


async def timeOutDB(message: types.Message):
    try:
        Coll = admin.Coll.lessonTimes
        i = 1
        while await Coll.find_one({'_id': {'$eq': i}}) is not None:
            a = await Coll.find_one({'_id': {'$eq': i}})
            await message.answer(f"{a['_id']}\t"
                                 f"|\t{a['lessonStart']}\t"
                                 f"|\t{a['lessonEnd']}")
            i += 1
    except:
        await message.answer("У вас немає доступу до цієї операції!")


async def lessonOutDB(message: types.Message):
    dayWeek = datetime.today().weekday()
    Coll = None
    if dayWeek == 0:
        Coll = cluster.onua_time_table.mon
    elif dayWeek == 1:
        Coll = cluster.onua_time_table.tue
    elif dayWeek == 2:
        Coll = cluster.onua_time_table.wed
    elif dayWeek == 3:
        Coll = cluster.onua_time_table.thu
    elif dayWeek == 4:
        Coll = cluster.onua_time_table.fri
    elif dayWeek == 5:
        Coll = cluster.onua_time_table.sat
    elif dayWeek == 6:
        Coll = cluster.onua_time_table.sun

    i = 1
    while await Coll.find_one({'_id': {'$eq': i}}) is not None:
        a = await Coll.find_one({'_id': {'$eq': i}})
        await message.answer(f"{a['_id']}\t"
                             f"|\t{a['lessonStart']}\t"
                             f"|\t{a['lessonEnd']}\t"
                             f"|\t{a['Lesson']}\t"
                             f"|\t{a['Link']}")
        i += 1


async def lessonOutNow(message: types.Message):
    dayWeek = datetime.today().weekday()
    timeNow = datetime.today().time()
    Coll = None
    if dayWeek == 0:
        Coll = cluster.onua_time_table.mon
    elif dayWeek == 1:
        Coll = cluster.onua_time_table.tue
    elif dayWeek == 2:
        Coll = cluster.onua_time_table.wed
    elif dayWeek == 3:
        Coll = cluster.onua_time_table.thu
    elif dayWeek == 4:
        Coll = cluster.onua_time_table.fri
    elif dayWeek == 5:
        Coll = cluster.onua_time_table.sat
    elif dayWeek == 6:
        Coll = cluster.onua_time_table.sun

    i = 1
    b = None
    while True:
        if await Coll.find_one({'_id': {'$eq': i}}) is None:
            await message.answer("Пари закінчились, відпочивайте)")
            break

        a = await Coll.find_one({'_id': {'$eq': i}})
        if datetime.time(datetime.strptime(a['lessonStart'], "%H:%M:%S")) > timeNow and i == 1:
            await message.answer("Пари ще не розпочались.\nНаступна пара:")
            await message.answer(f"{a['_id']}\t"
                                 f"|\t{a['lessonStart']}\t"
                                 f"|\t{a['lessonEnd']}\t"
                                 f"|\t{a['Lesson']}\t"
                                 f"|\t{a['Link']}")
            break

        elif datetime.time(datetime.strptime(a['lessonStart'], "%H:%M:%S")) <= timeNow <= datetime.time(datetime.strptime(a['lessonEnd'], "%H:%M:%S")):
            await message.answer("Зараз:")
            await message.answer(f"{a['_id']}\t"
                                 f"|\t{a['lessonStart']}\t"
                                 f"|\t{a['lessonEnd']}\t"
                                 f"|\t{a['Lesson']}\t"
                                 f"|\t{a['Link']}")
            break

        elif b is not None:
            if datetime.time(datetime.strptime(b['lessonEnd'], "%H:%M:%S")) < timeNow < datetime.time(datetime.strptime(a['lessonStart'], "%H:%M:%S")):
                await message.answer("Зараз перерва.\nНаступна пара:")
                await message.answer(f"{a['_id']}\t"
                                     f"|\t{a['lessonStart']}\t"
                                     f"|\t{a['lessonEnd']}\t"
                                     f"|\t{a['Lesson']}\t"
                                     f"|\t{a['Link']}")
                break

        b = a
        i += 1


def register_handlers_out_data_outTime(dp: Dispatcher):
    dp.register_message_handler(timeOutDB, commands=['Часи_занять'])
    dp.register_message_handler(lessonOutDB, commands=['Розклад'])
    dp.register_message_handler(lessonOutNow, commands=['Зараз'])

