from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_reader
from schemas import Reader
from .oauth2 import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_reader(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Reader:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        email = decode_token(token)
        if email is None:
            raise credentials_exception
        reader = db_reader.get_reader_by_email(db, email)
        if reader is None:
            raise credentials_exception
        return reader
    except HTTPException:
        raise credentials_exception