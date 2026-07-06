# Roadmap du stage — 6 semaines (6 juillet → 15 août 2026)

| Semaine | Dates | Livrable |
|---|---|---|
| S1 | 6-12 juillet | Cadrage validé, VPS en place, schéma de base de données, environnement de dev opérationnel |
| S2 | 13-19 juillet | Backend API (FastAPI) : CRUD clients/leads, connexion PostgreSQL |
| S3 | 20-26 juillet | Frontend web : formulaire configurateur + prise de lead, intégration agent AI conversationnel (Groq) |
| S4 | 27 juillet - 2 août | Dashboard admin (KPIs, vue leads) |
| S5 | 3-9 août | Machine Learning : modèle de scoring de propension à l'achat + intégration à l'API |
| S6 | 10-15 août | Tests, déploiement, documentation finale, préparation de la soutenance |

## Aujourd'hui (6 juillet) — à faire dans la journée

1. Créer le VPS (OVH VPS Comfort ou équivalent) et s'y connecter en SSH.
2. Lancer `docker-compose up -d` (Postgres + Kafka/Redis) — déjà préparé dans `infra/docker-compose.yml`.
3. Appliquer le schéma de base de données (`data-pipeline/schema.sql`).
4. Lancer l'API FastAPI de base (`couche-serving/main.py`) et vérifier `/health`.
5. Initialiser le frontend Next.js (`app-utilisateur/`).
6. Premier commit + push sur GitHub — preuve horodatée que le projet a démarré le jour 1.
