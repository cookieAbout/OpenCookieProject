from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.crud import create_book, get_books, get_book, delete_book, create_quote, get_quotes_by_book, delete_quote
from database.session import get_db


# Состояния для FSM
class BookState(StatesGroup):
    waiting_for_title = State()
    waiting_for_author = State()


class QuoteState(StatesGroup):
    waiting_for_book = State()
    waiting_for_text = State()


# Обработчик команды /start
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для сохранения цитат из книг. Используйте /help для списка команд.")


# Обработчик команды /help
async def cmd_help(message: types.Message):
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом
    /help - Показать справку
    /add_book - Добавить новую книгу
    /list_books - Показать список книг
    /book_info - Показать информацию о книге
    /add_quote - Добавить цитату
    /delete_book - Удалить книгу
    /delete_quote - Удалить цитату
    """
    await message.answer(help_text)


# Обработчик команды /add_book
async def cmd_add_book(message: types.Message):
    await BookState.waiting_for_title.set()
    await message.answer("Введите название книги:")


# Обработчик ввода названия книги
async def process_book_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await BookState.waiting_for_author.set()
    await message.answer("Введите автора книги (или пропустите):")


# Обработчик ввода автора книги
async def process_book_author(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['author'] = message.text
        db = next(get_db())
        book = create_book(db, data['title'], data['author'])
        await message.answer(f"Книга '{book.title}' успешно добавлена!")
    await state.finish()


# Обработчик команды /list_books
async def cmd_list_books(message: types.Message):
    db = next(get_db())
    books = get_books(db)
    if not books:
        await message.answer("У вас пока нет книг.")
        return
    books_list = "\n".join([f"{book.id}. {book.title} - {book.author or 'Автор не указан'}" for book in books])
    await message.answer(f"Ваши книги:\n{books_list}")


# Обработчик команды /book_info
async def cmd_book_info(message: types.Message):
    await message.answer("Введите ID книги:")


# Обработчик ввода ID книги
async def process_book_id(message: types.Message):
    try:
        book_id = int(message.text)
        db = next(get_db())
        book = get_book(db, book_id)
        if not book:
            await message.answer("Книга не найдена.")
            return
        quotes = get_quotes_by_book(db, book_id)
        quotes_text = "\n".join([f"- {quote.text}" for quote in quotes]) if quotes else "Нет цитат."
        await message.answer(f"Книга: {book.title}\nАвтор: {book.author or 'Не указан'}\n\nЦитаты:\n{quotes_text}")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID книги.")


# Обработчик команды /add_quote
async def cmd_add_quote(message: types.Message):
    await QuoteState.waiting_for_book.set()
    await message.answer("Введите ID книги:")


# Обработчик ввода ID книги для цитаты
async def process_quote_book(message: types.Message, state: FSMContext):
    try:
        book_id = int(message.text)
        db = next(get_db())
        book = get_book(db, book_id)
        if not book:
            await message.answer("Книга не найдена.")
            await state.finish()
            return
        async with state.proxy() as data:
            data['book_id'] = book_id
        await QuoteState.waiting_for_text.set()
        await message.answer("Введите текст цитаты:")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID книги.")


# Обработчик ввода текста цитаты
async def process_quote_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        db = next(get_db())
        quote = create_quote(db, data['book_id'], message.text)
        await message.answer(f"Цитата успешно добавлена к книге!")
    await state.finish()


# Обработчик команды /delete_book
async def cmd_delete_book(message: types.Message):
    await message.answer("Введите ID книги для удаления:")


# Обработчик ввода ID книги для удаления
async def process_delete_book(message: types.Message):
    try:
        book_id = int(message.text)
        db = next(get_db())
        if delete_book(db, book_id):
            await message.answer("Книга успешно удалена.")
        else:
            await message.answer("Книга не найдена.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID книги.")


# Обработчик команды /delete_quote
async def cmd_delete_quote(message: types.Message):
    await message.answer("Введите ID цитаты для удаления:")


# Обработчик ввода ID цитаты для удаления
async def process_delete_quote(message: types.Message):
    try:
        quote_id = int(message.text)
        db = next(get_db())
        if delete_quote(db, quote_id):
            await message.answer("Цитата успешно удалена.")
        else:
            await message.answer("Цитата не найдена.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID цитаты.")


# Регистрация обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(cmd_help, commands=["help"])
    dp.register_message_handler(cmd_add_book, commands=["add_book"])
    dp.register_message_handler(process_book_title, state=BookState.waiting_for_title)
    dp.register_message_handler(process_book_author, state=BookState.waiting_for_author)
    dp.register_message_handler(cmd_list_books, commands=["list_books"])
    dp.register_message_handler(cmd_book_info, commands=["book_info"])
    dp.register_message_handler(process_book_id)
    dp.register_message_handler(cmd_add_quote, commands=["add_quote"])
    dp.register_message_handler(process_quote_book, state=QuoteState.waiting_for_book)
    dp.register_message_handler(process_quote_text, state=QuoteState.waiting_for_text)
    dp.register_message_handler(cmd_delete_book, commands=["delete_book"])
    dp.register_message_handler(process_delete_book)
    dp.register_message_handler(cmd_delete_quote, commands=["delete_quote"])
    dp.register_message_handler(process_delete_quote)
