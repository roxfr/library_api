from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_book import create_book as create_book_db, get_books as get_books_db
from schemas import Book, BookAvailabilityResponse, BookCreate
import models as mod

router = APIRouter()

@router.post("/books/", response_model=Book)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        db_book = create_book_db(db=db, book=book)
        return Book(id=db_book.id, title=db_book.title, author=db_book.author, isbn=db_book.isbn)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Une erreur est survenue lors de la création du livre"
                            )

@router.get("/books/list", response_model=List[Book])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        db_books = get_books_db(db, skip=skip, limit=limit)
        books = [Book(id=db_book.id, title=db_book.title, author=db_book.author, isbn=db_book.isbn) for db_book in db_books]
        return books
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(f"Une erreur s'est produite : {e}")
        print(f"Traceback : {traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Une erreur est survenue lors de la récupération des livres"
        )

@router.get("/book/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(mod.Book).filter(mod.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return Book(id=book.id, title=book.title, author=book.author, isbn=book.isbn)

@router.get("/books/{book_id}/availability", response_model=BookAvailabilityResponse)
def check_book_availability(book_id: int, db: Session = Depends(get_db)):
    book = db.query(mod.Book).filter(mod.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé"
        )    
    active_borrowing = db.query(mod.Borrowing).filter(
        mod.Borrowing.book_id == book_id,
        mod.Borrowing.return_date.is_(None)
    ).first()
    message = "Le livre est disponible" if active_borrowing is None else "Le livre est actuellement emprunté"    
    return BookAvailabilityResponse(title=book.title, message=message)