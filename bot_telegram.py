from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from inoutdb import lesson_table, time_table, out_data


async def on_startup(_):
	print("Бот вышел в онлайн ")


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

time_table.register_handlers_time_table(dp)
time_table.register_handlers_time_table_input(dp)
time_table.register_handlers_time_table_indb(dp)

lesson_table.register_handlers_lesson_table(dp)
lesson_table.register_handlers_lesson_table_input(dp)
lesson_table.register_handlers_lesson_table_indb(dp)

out_data.register_handlers_out_data_outTime(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


