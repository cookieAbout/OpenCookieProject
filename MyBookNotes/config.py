from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


class Settings(BaseSettings):
    # Токен Telegram-бота
    BOT_TOKEN: str

    # Путь к базе данных SQLite
    DATABASE_URL: str = "sqlite:///books.db"

    class Config:
        env_file = ".env"


# Создаем экземпляр настроек
settings = Settings()
