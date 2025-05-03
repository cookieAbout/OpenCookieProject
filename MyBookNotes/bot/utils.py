from aiogram import types
from database.crud import get_book_list, get_quotes_by_book
from .keyboards import get_books_inline_keyboard, get_quotes_inline_keyboard
from database.session import get_db


# Функция для отправки списка книг с инлайн-клавиатурой
async def send_books_list(message: types.Message):
    db = next(get_db())
    books = get_book_list(db)
    if not books:
        await message.answer("У вас пока нет книг.")
        return
    keyboard = get_books_inline_keyboard(books)
    await message.answer("Выберите книгу:", reply_markup=keyboard)


# Функция для отправки списка цитат с инлайн-клавиатурой
async def send_quotes_list(message: types.Message, book_id: int):
    db = next(get_db())
    quotes = get_quotes_by_book(db, book_id)
    if not quotes:
        await message.answer("У этой книги пока нет цитат.")
        return
    keyboard = get_quotes_inline_keyboard(quotes)
    await message.answer("Выберите цитату:", reply_markup=keyboard)
