from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import text
from app.main import SessionLocal
from app.cache import lire_cache, ecrire_cache
import math
import json

router = APIRouter()

class RequeteLocalisation(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    rayon_m: int = Field(15000, ge=500, le=50000)
    types_services: Optional[List[str]] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculer_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

@router.post("/recherche/geo")
def rechercher_prestataires(q: RequeteLocalisation, db=Depends(get_db)):
    cle_cache = f"geo:{round(q.lat,3)}:{round(q.lng,3)}:{q.rayon_m}:{sorted(q.types_services or [])}"
    
    en_cache = lire_cache(cle_cache)
    if en_cache:
        return {"statut": "mis_en_cache", "donnees": en_cache}

    params = {
        "lat_min": q.lat - (q.rayon_m / 111320),
        "lat_max": q.lat + (q.rayon_m / 111320),
        "lng_min": q.lng - (q.rayon_m / (111320 * math.cos(math.radians(q.lat)))),
        "lng_max": q.lng + (q.rayon_m / (111320 * math.cos(math.radians(q.lat)))),
    }

    # CORREÇÃO: Sintaxe PostgreSQL compatível
    conditions = []
    if q.types_services:
        for i, service in enumerate(q.types_services):
            conditions.append(f"types_services @> CAST(:type_{i} AS jsonb)")
            params[f"type_{i}"] = f'["{service}"]'
    
    json_clause = " AND (" + " OR ".join(conditions) + ")" if conditions else ""

    sql = f"""
    SELECT id, nom_complet, email, telephone, types_services, latitude, longitude, verifie
    FROM prestataires
    WHERE latitude BETWEEN :lat_min AND :lat_max
      AND longitude BETWEEN :lng_min AND :lng_max
      {json_clause}
    """

    try:
        result = db.execute(text(sql), params)
        rows = []
        for r in result:
            row_dict = dict(r._mapping)
            dist = calculer_distance(q.lat, q.lng, r.latitude, r.longitude)
            if dist <= q.rayon_m:
                row_dict['distance_m'] = round(dist)
                if isinstance(row_dict['types_services'], str):
                    row_dict['types_services'] = json.loads(row_dict['types_services'])
                rows.append(row_dict)

        rows.sort(key=lambda x: x['distance_m'])
        ecrire_cache(cle_cache, rows)
        return {"statut": "succes", "donnees": rows, "total": len(rows)}

    except Exception as e:
        print(f"❌ Erreur DB: {e}")
        raise HTTPException(status_code=500, detail=str(e))