from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models as mod
from schemas import BookCreate

def create_book(db: Session, book: BookCreate):
    # Vérifier si l'ISBN existe déjà
    existing_book = db.query(mod.Book).filter(mod.Book.isbn == book.isbn).first()
    if existing_book:
        raise ValueError("Un livre avec cet ISBN existe déjà")
    db_book = mod.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )
    db.add(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Une erreur s'est produite lors de l'ajout du livre à la base de données")
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    books = db.query(mod.Book).offset(skip).limit(limit).all()
    return books