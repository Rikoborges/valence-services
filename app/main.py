from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.models import Base, ConsentLog  # ← Modelos

load_dotenv()

# 🔗 Configuração da conexão com a base de dados
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/valence_services")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Criar as tabelas automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Services Valence", version="0.1.0", description="Plateforme de mise en relation locale")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Importar e registar os routers
from app.api.v1.geo import router as geo_router
from app.api.v1.consent import router as consent_router

app.include_router(geo_router, prefix="/api/v1", tags=["geo"])
app.include_router(consent_router, prefix="/api/v1", tags=["consent"])

@app.on_event("startup")
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()
            print(f"✅ Base de données connectée avec succès !")
            print(f"📦 Version MySQL/MariaDB: {version[0]}")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")