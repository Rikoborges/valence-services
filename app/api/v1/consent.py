from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import ConsentLog, ConsentType
from typing import Optional
import datetime

router = APIRouter()

class ConsentRequest(BaseModel):
    user_id: str
    consent_type: str
    purpose: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_m: Optional[int] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/consent")
def log_consent(c: ConsentRequest, request: Request, db: Session = Depends(get_db)):
    try:
        consent = ConsentLog(
            user_id=c.user_id,
            consent_type=ConsentType(c.consent_type),
            purpose=c.purpose,
            latitude=c.latitude,
            longitude=c.longitude,
            radius_m=c.radius_m,
            ip_address=request.client.host if request.client else None,
            consent_version="1.0.0"
        )
        db.add(consent)
        db.commit()
        db.refresh(consent)
        return {"statut": "succes", "consent_id": consent.id, "timestamp": consent.created_at}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement: {str(e)}")

@router.get("/consent/export/{user_id}")
def export_user_data(user_id: str, db: Session = Depends(get_db)):
    consents = db.query(ConsentLog).filter(ConsentLog.user_id == user_id).all()
    return {
        "user_id": user_id,
        "total_consents": len(consents),
        "consents": [
            {
                "id": c.id,
                "type": c.consent_type.value,
                "purpose": c.purpose,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "withdrawn_at": c.withdrawn_at.isoformat() if c.withdrawn_at else None
            }
            for c in consents
        ]
    }

@router.delete("/consent/erase/{user_id}")
def erase_user_data(user_id: str, db: Session = Depends(get_db)):
    try:
        db.query(ConsentLog).filter(
            ConsentLog.user_id == user_id,
            ConsentLog.withdrawn_at.is_(None)
        ).update({"withdrawn_at": datetime.datetime.now()})
        db.commit()
        return {"statut": "succes", "message": "Données marquées comme supprimées"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")