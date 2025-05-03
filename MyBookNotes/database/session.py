from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаём движок SQLAlchemy для SQLite
engine = create_engine('sqlite:///books.db', echo=True)

# Создаём сессию
SessionLocal = sessionmaker(bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 