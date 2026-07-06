# Couche serving

API d'inférence temps réel (FastAPI) pour les agents et l'app — **connectée à PostgreSQL**.

## Démarrage

1. Démarrer PostgreSQL (via `infra/docker-compose.yml` ou une installation locale).
2. Appliquer le schéma : `psql -h localhost -U rsc_user -d renault_smart_companion -f ../data-pipeline/schema.sql`
3. Copier `.env.example` en `.env` et ajuster `DATABASE_URL` si besoin.
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload --port 8000`
6. Ouvrir http://localhost:8000/docs

## Fait
- [x] Connexion PostgreSQL (`database.py`)
- [x] CRUD clients, leads, véhicules
- [x] Endpoint `/kpis` pour le dashboard admin

## À faire
- [ ] Endpoint /score (propension client)
- [ ] Endpoint /recommend (véhicule/offre)
- [ ] Authentification (admin vs public)
