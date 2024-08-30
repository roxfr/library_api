from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import func
from datetime import datetime
from models import Borrowing as DBBorrowing, Book, Reader
from schemas import BorrowingCreate

def create_borrowing(db: Session, borrowing: BorrowingCreate) -> DBBorrowing:
    # Vérifier si le livre existe
    book_exists = db.query(Book).filter(Book.id == borrowing.book_id).first()
    if not book_exists:
        raise ValueError("Le livre demandé n'existe pas.")
    
    # Vérifier si le lecteur existe
    reader_exists = db.query(Reader).filter(Reader.id == borrowing.reader_id).first()
    if not reader_exists:
        raise ValueError("Le lecteur demandé n'existe pas.")
    
    # Vérifier si un emprunt avec les mêmes paramètres existe déjà
    existing_borrowing_count = db.query(DBBorrowing).filter(
        func.date(DBBorrowing.borrow_date) == borrowing.borrow_date,
        func.date(DBBorrowing.return_date) == borrowing.return_date,
        DBBorrowing.reader_id == borrowing.reader_id,
        DBBorrowing.book_id == borrowing.book_id
    ).count()
    
    # print(f"existing_borrowing_count : {existing_borrowing_count}")
    
    if existing_borrowing_count > 0:
        raise ValueError("Un emprunt avec ces paramètres existe déjà.")
    
    # Vérifier que la date de retour est après la date d'emprunt
    if borrowing.return_date and borrowing.return_date < borrowing.borrow_date:
        raise ValueError("La date de retour ne peut pas être antérieure à la date d'emprunt.")
    
    # Optionnel : Vérifier que la date d'emprunt est dans le futur (si nécessaire)
    if borrowing.borrow_date < datetime.now().date():
        raise ValueError("La date d'emprunt ne peut pas être dans le passé.")
    
    # Créer l'enregistrement de l'emprunt
    db_borrowing = DBBorrowing(
        reader_id=borrowing.reader_id,
        book_id=borrowing.book_id,
        borrow_date=borrowing.borrow_date,
        return_date=borrowing.return_date
    )
    
    try:
        db.add(db_borrowing)
        db.commit()
        db.refresh(db_borrowing)
        return db_borrowing
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError("Une erreur est survenue lors de l'enregistrement de l'emprunt.") from e

def get_borrowings_by_reader(db: Session, reader_id: int):
    return db.query(DBBorrowing).filter(DBBorrowing.reader_id == reader_id).all()