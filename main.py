import asyncio

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from fastapi import FastAPI

from app.api import data_router, check_router, bot_router, master_router, event_router
from app.db.base import Base
from app.db.session import engine

from app.telegram_bot.config import API_TOKEN
from app.telegram_bot.handlers import router

app = FastAPI()

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage, bot=bot)

@app.on_event("startup")
async def on_startup():
    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Авторизация"),
        BotCommand(command="plan", description="Показать план проверок"),
        BotCommand(command="route", description="Получить маршрут до точки"),
    ])

    asyncio.create_task(dp.start_polling(bot))

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

Base.metadata.create_all(bind=engine)

app.include_router(data_router.router)
app.include_router(event_router.router)
app.include_router(check_router.router)
app.include_router(bot_router.router)
app.include_router(master_router.router)

if __name__ == '__main__':
    uvicorn.run(app)
