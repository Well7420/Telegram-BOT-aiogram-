#.venv\Scripts\activate
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import UP_Router
from handlers.admin_private import AP_Router
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message, edited_message'] # Список ключових типів, які Бот оброблює. Щоб не обробляв усе підряд.

async def main():
    #await async_main()
    bot = Bot(token=os.getenv('TOKEN')) # Токен Бота
    dp = Dispatcher() # Диспетчер, щоб Бот міг приймати команди
    dp.include_router(UP_Router)
    dp.include_router(AP_Router)
    await bot.delete_webhook(drop_pending_updates=True) # Щоб Бот не відповідав на ті запити, які надходили, коли Бот був у вимкнутому стані
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) # commands=private - команди з файлу bot_cmds_list.py
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

# V Додаткова конструкція для def main(). Потрібна для того, щоб виконання функції було тільки якщо запуск був безпосередньо з файлу botmain.py
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнуто')