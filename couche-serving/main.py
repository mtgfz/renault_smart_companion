"""
Renault Smart Companion — Concessionnaire
API backend (FastAPI) — connectée à PostgreSQL.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db

app = FastAPI(
    title="Renault Smart Companion — API",
    description="API du concessionnaire : clients, leads, scoring, agents AI. Connectée à PostgreSQL.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClientIn(BaseModel):
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    ville: Optional[str] = None
    source: Optional[str] = "site_web"
    canal: Optional[str] = None
    campagne: Optional[str] = None


class LeadIn(BaseModel):
    client_id: int
    vehicule_id: int
    notes: Optional[str] = None


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "service": "renault-smart-companion-api", "database": "connected"}


@app.post("/clients", status_code=201)
def create_client(client: ClientIn, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                INSERT INTO clients (nom, prenom, email, telephone, ville, source, canal, campagne)
                VALUES (:nom, :prenom, :email, :telephone, :ville, :source, :canal, :campagne)
                RETURNING id, nom, prenom, email, telephone, ville, source, canal, campagne, created_at
            """),
            client.dict(),
        )
        db.commit()
        row = result.mappings().first()
        return dict(row)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Un client avec cet email existe déjà.")


@app.get("/clients")
def list_clients(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM clients ORDER BY created_at DESC"))
    return [dict(row) for row in result.mappings()]


@app.get("/clients/{client_id}")
def get_client(client_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM clients WHERE id = :id"), {"id": client_id})
    row = result.mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return dict(row)


@app.post("/leads", status_code=201)
def create_lead(lead: LeadIn, db: Session = Depends(get_db)):
    client_exists = db.execute(
        text("SELECT 1 FROM clients WHERE id = :id"), {"id": lead.client_id}
    ).first()
    if not client_exists:
        raise HTTPException(status_code=404, detail="Client introuvable — créez d'abord le client")

    vehicule_exists = db.execute(
        text("SELECT 1 FROM vehicules WHERE id = :id"), {"id": lead.vehicule_id}
    ).first()
    if not vehicule_exists:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    result = db.execute(
        text("""
            INSERT INTO leads (client_id, vehicule_id, notes)
            VALUES (:client_id, :vehicule_id, :notes)
            RETURNING id, client_id, vehicule_id, statut, score_propension, notes, created_at
        """),
        lead.dict(),
    )
    db.commit()
    row = result.mappings().first()
    return dict(row)


@app.get("/leads")
def list_leads(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT l.*, c.nom, c.prenom, v.modele, v.version
        FROM leads l
        JOIN clients c ON c.id = l.client_id
        JOIN vehicules v ON v.id = l.vehicule_id
        ORDER BY l.created_at DESC
    """))
    return [dict(row) for row in result.mappings()]


@app.get("/vehicules")
def list_vehicules(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM vehicules WHERE disponible = true"))
    return [dict(row) for row in result.mappings()]


@app.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    """Endpoint utilisé par le dashboard admin (S4)."""
    total_clients = db.execute(text("SELECT COUNT(*) FROM clients")).scalar()
    total_leads = db.execute(text("SELECT COUNT(*) FROM leads")).scalar()
    par_statut = db.execute(
        text("SELECT statut, COUNT(*) as total FROM leads GROUP BY statut")
    ).mappings().all()
    return {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "leads_par_statut": {row["statut"]: row["total"] for row in par_statut},
    }


@app.get("/kpis/par-canal")
def get_kpis_par_canal(db: Session = Depends(get_db)):
    """Répartition des clients par source/canal/campagne — pour évaluer le ROI publicitaire."""
    par_source = db.execute(
        text("SELECT source, COUNT(*) as total FROM clients WHERE source IS NOT NULL GROUP BY source ORDER BY total DESC")
    ).mappings().all()

    par_canal = db.execute(
        text("SELECT canal, COUNT(*) as total FROM clients WHERE canal IS NOT NULL GROUP BY canal ORDER BY total DESC")
    ).mappings().all()

    par_campagne = db.execute(
        text("SELECT campagne, COUNT(*) as total FROM clients WHERE campagne IS NOT NULL GROUP BY campagne ORDER BY total DESC")
    ).mappings().all()

    return {
        "par_source": {row["source"]: row["total"] for row in par_source},
        "par_canal": {row["canal"]: row["total"] for row in par_canal},
        "par_campagne": {row["campagne"]: row["total"] for row in par_campagne},
    }
