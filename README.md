# Renault Smart Companion — Concessionnaire

Plateforme marketing intelligente pilotée par agents AI, Machine Learning et apprentissage par renforcement, conçue pour collecter la donnée client d'un concessionnaire Renault et augmenter le taux de conversion (visites → essais → achats).

**Stage PFA — Data & Software** · Durée : 2 mois · Superviseur concessionnaire : à compléter

## Objectif

Transformer chaque interaction client (site web, showroom, configurateur, SAV) en signal exploitable, et chaque signal en décision marketing personnalisée et mesurable — à l'échelle d'un concessionnaire.

## Structure du repo

| Dossier | Contenu |
|---|---|
| `app-utilisateur/` | App web/mobile client — configurateur, prise de RDV essai, SAV, chatbot agent AI |
| `app-admin/` | Back-office concessionnaire — KPIs, pilotage des leads, vue 360° client |
| `agents-ai/` | Orchestration multi-agents (LangGraph) + RAG sur le catalogue Renault |
| `data-pipeline/` | Ingestion (Kafka), traitement (Spark/Airflow), stockage (data lake) |
| `moteur-ml/` | Scoring de propension à l'achat, segmentation clients |
| `moteur-rl/` | Personnalisation séquentielle des offres (bandits contextuels) |
| `couche-serving/` | API d'inférence temps réel (FastAPI) |
| `infra/` | Docker Compose, configuration Kubernetes, CI/CD |
| `docs/` | Architecture, planning, budget, recherche Renault |

## Roadmap du stage (2 mois → MVP, avec vision cible complète)

Voir `docs/roadmap.md` pour le détail semaine par semaine et `docs/architecture.md` pour l'architecture cible complète (celle présentée en soutenance).

## Statut

🚧 En cours — cadrage terminé, mise en place de l'environnement de développement.
