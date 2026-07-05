# Architecture cible — Renault Smart Companion (Concessionnaire)

## Composants

- **App utilisateur** — Web (Next.js) & mobile (React Native), interface conversationnelle pilotée par agents AI (configuration véhicule, offres, financement, SAV, prise de RDV).
- **App admin** — Back-office concessionnaire : collecte, visualisation et pilotage des données comportementales et commerciales (leads, essais, ventes).
- **Agents AI** — Orchestration multi-agents (LangGraph) avec RAG sur le catalogue Renault et les stocks du concessionnaire.
- **Data pipeline** — Ingestion (Kafka), traitement (Spark/Airflow), stockage (data lake S3/MinIO + entrepôt analytique).
- **Moteur ML** — Scoring de propension à l'achat, segmentation clients, recommandation de véhicules/offres.
- **Moteur RL** — Personnalisation séquentielle des offres via bandits contextuels (quelle offre montrer, à qui, quand).
- **Couche serving** — API d'inférence temps réel (FastAPI) pour les agents et l'app.

## Pipeline technique (10 étapes)

1. **Collecte** — SDK de tracking embarqué : clics, navigation, configurateur, interactions agents AI, passages showroom (si CRM connecté).
2. **Ingestion temps réel** — Apache Kafka, découplage producteurs/consommateurs.
3. **Stockage (data lake)** — Zone raw (S3/MinIO) → Spark Structured Streaming → zone curated (Parquet) + ClickHouse/BigQuery.
4. **Feature engineering** — Pipeline Airflow quotidien, feature store (Feast).
5. **Machine Learning offline** — XGBoost/LightGBM, tracking MLflow, model registry.
6. **Reinforcement Learning** — Bandit contextuel (LinUCB/Thompson Sampling), mise à jour incrémentale.
7. **Serving & inférence** — API FastAPI (<200ms), cache Redis, scalabilité Kubernetes.
8. **Couche agentique** — Agents spécialisés (véhicule, offres/financement, SAV) orchestrés via LangGraph + RAG.
9. **Administration & pilotage** — Dashboard temps réel : KPIs, alerting anomalies/model drift.
10. **Boucle de feedback** — Chaque interaction réinjectée dans Kafka pour amélioration continue.

## Adaptation "échelle concessionnaire" (2 mois de stage)

Un concessionnaire unique génère un volume de données bien plus faible qu'un déploiement national — l'architecture cible ci-dessus reste valable comme **vision produit**, mais le MVP livrable en 2 mois se concentre sur un sous-ensemble représentatif :

| Phase | Composants livrés en 2 mois | Composants en roadmap (post-stage) |
|---|---|---|
| MVP stage | App utilisateur (web), App admin (dashboard), Data pipeline simplifié (Kafka + Postgres), Moteur ML (scoring propension), Couche serving (API FastAPI) | Moteur RL complet, agents AI multi-spécialisés, Kubernetes, ClickHouse/BigQuery à l'échelle |
| Cible production | Architecture complète décrite plus haut, généralisable à plusieurs concessionnaires du réseau | — |

Voir `docs/budget.xlsx` pour le chiffrage détaillé de chaque brique, en distinguant le coût du MVP (2 mois) et le coût de la cible.
