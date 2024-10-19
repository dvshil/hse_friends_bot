import asyncio
import os
import sys

from app.database.orm import SyncORM

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from aiogram import Bot, Dispatcher, F
from app.handlers import router

# SyncORM.create_tables()

async def main():

    bot = Bot(token='7126231479:AAHILyOiKMIHEBN58Dq7IXViiXXUf4r0q-E')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')
