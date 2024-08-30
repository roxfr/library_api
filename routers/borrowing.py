from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_borrowing import create_borrowing, get_borrowings_by_reader
from schemas import BorrowingCreate, Borrowing as BorrowingSchema, Reader
from auth.authentication import get_current_reader

router = APIRouter()

@router.post("/borrowings/", response_model=BorrowingSchema)
def create_borrowing_endpoint(borrowing: BorrowingCreate, db: Session = Depends(get_db)):
    try:
        return create_borrowing(db, borrowing)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Erreur serveur interne")

@router.get("/borrowings/me/", response_model=List[BorrowingSchema])
def list_borrowings_me(
        db: Session = Depends(get_db),
        current_reader: Reader = Depends(get_current_reader)
        ):
    borrowings = get_borrowings_by_reader(db=db, reader_id=current_reader.id)
    if not borrowings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun emprunt trouvé pour le lecteur courant")
    return borrowings
