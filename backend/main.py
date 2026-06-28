from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ← ajoute ça
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from pydantic import BaseModel
from typing import Optional
from datetime import date
import requests
import os
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# --- Schémas ---
class VetementCreate(BaseModel):
    nom: str
    categorie: str
    couleur: Optional[str] = None
    style: Optional[str] = None
    photo_url: Optional[str] = None

class VetementResponse(VetementCreate):
    id: int
    nb_ports: int
    dernier_port: Optional[date] = None

    class Config:
        from_attributes = True

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Outfit of Today API 🚀"}

@app.post("/vetements", response_model=VetementResponse)
def ajouter_vetement(vetement: VetementCreate, db: Session = Depends(get_db)):
    nouveau = models.Vetement(**vetement.model_dump())
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

@app.get("/vetements")
def lister_vetements(db: Session = Depends(get_db)):
    return db.query(models.Vetement).all()

@app.delete("/vetements/{id}")
def supprimer_vetement(id: int, db: Session = Depends(get_db)):
    vetement = db.query(models.Vetement).filter(models.Vetement.id == id).first()
    if not vetement:
        raise HTTPException(status_code=404, detail="Vêtement introuvable")
    db.delete(vetement)
    db.commit()
    return {"message": "Vêtement supprimé"}

@app.get("/meteo/{ville}")
def get_meteo(ville: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric&lang=fr"
    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Ville introuvable")
    data = res.json()
    return {
        "ville": ville,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icone": data["weather"][0]["icon"]
    }