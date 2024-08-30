# FastAPI - Swagger UI => http://localhost:8000/docs

from fastapi import FastAPI
from db.database import engine
import models
from routers import book, borrowing, reader, auth

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclure les routeurs
app.include_router(auth.router, tags=["Authentification"])
app.include_router(book.router, tags=["Livres"])
app.include_router(borrowing.router, tags=["Emprunts"])
app.include_router(reader.router, tags=["Utilisateurs"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue à la bibliothèque API ;-)"}