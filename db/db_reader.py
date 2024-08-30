from sqlalchemy.orm import Session
from schemas import ReaderCreate
from models import Reader
from db.hash import Hash

def create_reader(db: Session, reader: ReaderCreate):
    if get_reader_by_email(db, reader.email):
        return None
    hashed_password = Hash.hash_password(reader.password)
    db_reader = Reader(
        first_name=reader.first_name,
        last_name=reader.last_name,
        email=reader.email,
        password=hashed_password
    )
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def get_reader_by_email(db: Session, email: str) -> Reader:
    return db.query(Reader).filter(Reader.email == email).first()

def get_reader_by_id(db: Session, reader_id: int) -> Reader:
    return db.query(Reader).filter(Reader.id == reader_id).first()