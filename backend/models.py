from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Vetement(Base):
    __tablename__ = "vetements"

    id        = Column(Integer, primary_key=True, index=True)
    nom       = Column(String, nullable=False)
    categorie = Column(String, nullable=False)  # haut, bas, chaussures...
    couleur   = Column(String)
    style     = Column(String)                  # casual, sport, élégant...
    photo_url = Column(String)
    nb_ports  = Column(Integer, default=0)
    dernier_port = Column(Date, nullable=True)

class Tenue(Base):
    __tablename__ = "tenues"

    id         = Column(Integer, primary_key=True, index=True)
    date       = Column(Date, nullable=False)
    haut_id    = Column(Integer)
    bas_id     = Column(Integer)
    chaussures_id = Column(Integer)