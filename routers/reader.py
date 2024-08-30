from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_reader import create_reader, get_reader_by_id
from schemas import ReaderCreate, Reader
from auth.authentication import get_current_reader

router = APIRouter()

@router.post("/readers/", response_model=Reader)
def register_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    db_reader = create_reader(db=db, reader=reader)
    if db_reader is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà utilisé")
    return db_reader

@router.get("/readers/{reader_id}", response_model=Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db), current_user: Reader = Depends(get_current_reader)):
    db_reader = get_reader_by_id(db=db, reader_id=reader_id)
    if db_reader is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    # if current_user.id != reader_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
    return db_reader