from sqlalchemy import Column, String, Integer, Boolean, DECIMAL, Enum, TIMESTAMP, func, Text
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ConsentType(str, enum.Enum):
    gps = "gps"
    manual = "manual"
    ip = "ip"

class ConsentLog(Base):
    __tablename__ = "consent_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, index=True)
    consent_type = Column(Enum(ConsentType), nullable=False)
    purpose = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    radius_m = Column(Integer)
    ip_address = Column(String(45))
    consent_version = Column(String(10), default="1.0.0")
    created_at = Column(TIMESTAMP, server_default=func.now())
    withdrawn_at = Column(TIMESTAMP, nullable=True)


class Prestataire(Base):
    __tablename__ = "prestataires"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom_complet = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(30))
    types_services = Column(Text)  # JSON array stocké en texte
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    verifie = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())