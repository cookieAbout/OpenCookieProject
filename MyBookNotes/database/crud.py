from sqlalchemy.orm import Session
from .models import Book, Quote


# CRUD для Book
def create_book(db: Session, title: str, author: str = None):
    book = Book(title=title, author=author)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session):
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False


# CRUD для Quote
def create_quote(db: Session, book_id: int, text: str):
    quote = Quote(book_id=book_id, text=text)
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def get_quotes_by_book(db: Session, book_id: int):
    return db.query(Quote).filter(Quote.book_id == book_id).all()


def delete_quote(db: Session, quote_id: int):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote:
        db.delete(quote)
        db.commit()
        return True
    return False
