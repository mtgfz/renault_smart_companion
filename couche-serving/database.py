"""
Connexion à PostgreSQL — Renault Smart Companion.

Lit l'URL de connexion depuis la variable d'environnement DATABASE_URL
(voir .env.example). Si elle n'est pas définie, utilise une valeur par
défaut adaptée au développement local (docker-compose ou Postgres local).
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://rsc_user:change_me@localhost:5432/renault_smart_companion",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dépendance FastAPI : ouvre une session DB par requête, la ferme après."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
