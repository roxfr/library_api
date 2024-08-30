from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    borrowings = relationship("Borrowing", back_populates="reader")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, nullable=False)

    borrowings = relationship("Borrowing", back_populates="book")

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)

   # Contrainte d'unicité
    __table_args__ = (
        UniqueConstraint('reader_id', 'book_id', 'borrow_date', 'return_date', name='unique_borrowing'),
    )

    reader = relationship("Reader", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
    
    def __repr__(self):
        return f"<Borrowing(id={self.id}, reader_id={self.reader_id}, book_id={self.book_id}, borrow_date={self.borrow_date}, return_date={self.return_date})>"