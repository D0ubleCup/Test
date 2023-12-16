from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
import asyncio

from handlers import bot_messages, commands

load_dotenv()




async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
            commands.router,
            bot_messages.router
        )
        
        
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())





    

    






    




