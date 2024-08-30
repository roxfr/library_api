from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base, get_db
from models import Reader, Book, Borrowing
from schemas import ReaderCreate, BookCreate, BorrowingCreate
from datetime import date

# Configurer une base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./db/library_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables pour la base de données de test
Base.metadata.create_all(bind=engine)

# Fonction de dépendance pour utiliser la session de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Remplacer la dépendance de la base de données avec la version de test
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue à la bibliothèque API"}

def test_create_reader():
    reader_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "secret"
    }
    response = client.post("/readers/", json=reader_data)
    assert response.status_code == 200
    assert response.json()["email"] == reader_data["email"]
    assert "id" in response.json()

def test_create_book():
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "1234567890123"
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert "id" in response.json()

def test_create_borrowing():
    # Créer d'abord un lecteur
    reader_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "secret"
    }
    reader_response = client.post("/readers/", json=reader_data)
    reader_id = reader_response.json()["id"]

    # Créer un livre
    book_data = {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "isbn": "9876543210987"
    }
    book_response = client.post("/books/", json=book_data)
    book_id = book_response.json()["id"]

    # Créer un emprunt
    borrowing_data = {
        "borrow_date": str(date.today()),
        "reader_id": reader_id,
        "book_id": book_id
    }
    response = client.post("/borrowings/", json=borrowing_data)
    assert response.status_code == 200
    assert response.json()["reader"]["id"] == reader_id
    assert response.json()["book"]["id"] == book_id

def test_get_reader():
    response = client.get("/readers/1")
    assert response.status_code == 200
    assert response.json()["email"] == "john.doe@example.com"

def test_get_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "1984"

def test_get_borrowing():
    response = client.get("/borrowings/1")
    assert response.status_code == 200
    assert "reader" in response.json()
    assert "book" in response.json()