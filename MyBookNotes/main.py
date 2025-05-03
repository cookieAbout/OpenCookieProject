import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from bot.handlers import register_handlers
from database.models import Base
from database.session import engine

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
register_handlers(dp)


# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
