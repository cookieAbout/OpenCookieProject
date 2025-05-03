from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    """ Клавиатура для основных команд """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/start"))
    keyboard.add(KeyboardButton("/help"))
    keyboard.add(KeyboardButton("/add_book"))
    keyboard.add(KeyboardButton("/list_books"))
    keyboard.add(KeyboardButton("/book_info"))
    keyboard.add(KeyboardButton("/add_quote"))
    keyboard.add(KeyboardButton("/delete_book"))
    keyboard.add(KeyboardButton("/delete_quote"))
    return keyboard


def get_books_inline_keyboard(books):
    """ Инлайн-клавиатура для выбора книги """
    keyboard = InlineKeyboardMarkup()
    for book in books:
        keyboard.add(
            InlineKeyboardButton(
                f"{book.title} - {book.author or 'Автор не указан'}", callback_data=f"book_{book.id}"
            )
        )
    return keyboard


def get_quotes_inline_keyboard(quotes):
    """ Инлайн-клавиатура для выбора цитаты """
    keyboard = InlineKeyboardMarkup()
    for quote in quotes:
        keyboard.add(InlineKeyboardButton(f"Цитата {quote.id}", callback_data=f"quote_{quote.id}"))
    return keyboard
