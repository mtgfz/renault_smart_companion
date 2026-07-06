"""
Renault Smart Companion — Concessionnaire
API backend (FastAPI) — point de départ jour 1.

Lancer en local :
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

Puis ouvrir : http://localhost:8000/docs (documentation interactive auto-générée)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Renault Smart Companion — API",
    description="API du concessionnaire : clients, leads, scoring, agents AI.",
    version="0.1.0",
)

# Autoriser le frontend (Next.js en dev tourne sur localhost:3000) à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Modèles de données (Pydantic) — reflètent le schema.sql
# ---------------------------------------------------------------------------
class ClientIn(BaseModel):
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    ville: Optional[str] = None
    source: Optional[str] = "site_web"


class LeadIn(BaseModel):
    client_id: int
    vehicule_id: int
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Stockage temporaire en mémoire — À REMPLACER par PostgreSQL dès S1/S2
# (volontairement simple aujourd'hui pour pouvoir démarrer immédiatement
# sans attendre la configuration complète de la base de données)
# ---------------------------------------------------------------------------
_clients_db = {}
_leads_db = {}
_next_client_id = 1
_next_lead_id = 1


@app.get("/health")
def health_check():
    """Vérifie que l'API tourne. À appeler en premier pour valider l'installation."""
    return {"status": "ok", "service": "renault-smart-companion-api", "timestamp": datetime.utcnow().isoformat()}


@app.post("/clients", status_code=201)
def create_client(client: ClientIn):
    global _next_client_id
    client_id = _next_client_id
    _clients_db[client_id] = {**client.dict(), "id": client_id, "created_at": datetime.utcnow().isoformat()}
    _next_client_id += 1
    return _clients_db[client_id]


@app.get("/clients")
def list_clients():
    return list(_clients_db.values())


@app.get("/clients/{client_id}")
def get_client(client_id: int):
    if client_id not in _clients_db:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return _clients_db[client_id]


@app.post("/leads", status_code=201)
def create_lead(lead: LeadIn):
    global _next_lead_id
    if lead.client_id not in _clients_db:
        raise HTTPException(status_code=404, detail="Client introuvable — créez d'abord le client")
    lead_id = _next_lead_id
    _leads_db[lead_id] = {
        **lead.dict(),
        "id": lead_id,
        "statut": "nouveau",
        "score_propension": None,
        "created_at": datetime.utcnow().isoformat(),
    }
    _next_lead_id += 1
    return _leads_db[lead_id]


@app.get("/leads")
def list_leads():
    return list(_leads_db.values())


@app.get("/kpis")
def get_kpis():
    """Endpoint utilisé par le dashboard admin (S4)."""
    total_clients = len(_clients_db)
    total_leads = len(_leads_db)
    leads_par_statut = {}
    for lead in _leads_db.values():
        leads_par_statut[lead["statut"]] = leads_par_statut.get(lead["statut"], 0) + 1
    return {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "leads_par_statut": leads_par_statut,
    }
