from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура для основных команд
def get_main_keyboard():
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


# Инлайн-клавиатура для выбора книги
def get_books_inline_keyboard(books):
    keyboard = InlineKeyboardMarkup()
    for book in books:
        keyboard.add(
            InlineKeyboardButton(
                f"{book.title} - {book.author or 'Автор не указан'}", callback_data=f"book_{book.id}"
            )
        )
    return keyboard


# Инлайн-клавиатура для выбора цитаты
def get_quotes_inline_keyboard(quotes):
    keyboard = InlineKeyboardMarkup()
    for quote in quotes:
        keyboard.add(InlineKeyboardButton(f"Цитата {quote.id}", callback_data=f"quote_{quote.id}"))
    return keyboard
