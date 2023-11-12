from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

linkDB = "mongodb+srv://FCIT:2022fcit2022@myclaster.wv6cw.mongodb.net/onua_time_table?retryWrites=true&w=majority"
cluster = AsyncIOMotorClient(linkDB)
