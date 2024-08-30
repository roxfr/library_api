from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Modèle de base pour un lecteur avec les informations essentielles
class ReaderBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

# Modèle utilisé pour créer un nouveau lecteur
class ReaderCreate(ReaderBase):
    password: str

# Modèle de lecture d'un lecteur avec un identifiant unique
class Reader(ReaderBase):
    id: int

# Modèle de base pour un livre avec les informations essentielles
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Titre du livre")
    author: str = Field(..., min_length=1, description="Auteur du livre")
    isbn: str = Field(..., min_length=1, description="ISBN du livre")

# Modèle utilisé pour créer un nouveau livre
class BookCreate(BookBase):
    pass

# Modèle de lecture d'un livre avec un identifiant unique
class Book(BookBase):
    id: int

# Réponse retournée pour indiquer la disponibilité d'un livre
class BookAvailabilityResponse(BaseModel):
    title: str
    message: str

# Modèle de base pour un emprunt avec les dates d'emprunt et de retour
class BorrowingBase(BaseModel):
    borrow_date: date
    return_date: Optional[date] = None

# Modèle utilisé pour créer un nouvel emprunt
class BorrowingCreate(BorrowingBase):
    reader_id: int
    book_id: int

# Modèle de lecture d'un emprunt avec des détails complets
class Borrowing(BorrowingBase):
    id: int
    reader: Reader
    book: Book