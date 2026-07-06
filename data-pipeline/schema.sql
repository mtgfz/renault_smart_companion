-- Renault Smart Companion — Concessionnaire
-- Schéma de base de données initial (PostgreSQL)
-- À exécuter le jour 1 : psql -U rsc_user -d renault_smart_companion -f schema.sql

CREATE TABLE IF NOT EXISTS clients (
    id              SERIAL PRIMARY KEY,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE,
    telephone       VARCHAR(20),
    ville           VARCHAR(100),
    source          VARCHAR(50),        -- ex: 'site_web', 'showroom', 'telephone'
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vehicules (
    id              SERIAL PRIMARY KEY,
    modele          VARCHAR(100) NOT NULL,     -- ex: 'Clio', 'Kardian', 'Express'
    version         VARCHAR(100),
    prix_catalogue  NUMERIC(10, 2),
    disponible      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leads (
    id              SERIAL PRIMARY KEY,
    client_id       INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    vehicule_id     INTEGER REFERENCES vehicules(id),
    statut          VARCHAR(30) DEFAULT 'nouveau',   -- nouveau, contacte, essai_planifie, essai_effectue, converti, perdu
    score_propension NUMERIC(4, 3),                  -- rempli plus tard par le modèle ML (0 à 1)
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS interactions (
    id              SERIAL PRIMARY KEY,
    client_id       INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    type            VARCHAR(30) NOT NULL,     -- 'clic_configurateur', 'message_agent', 'appel', 'visite_showroom'
    canal           VARCHAR(30),              -- 'web', 'mobile', 'showroom'
    contenu         JSONB,                    -- détail flexible de l'interaction
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rendez_vous (
    id              SERIAL PRIMARY KEY,
    lead_id         INTEGER REFERENCES leads(id) ON DELETE CASCADE,
    type            VARCHAR(30),              -- 'essai', 'sav', 'livraison'
    date_prevue     TIMESTAMP NOT NULL,
    statut          VARCHAR(30) DEFAULT 'planifie',  -- planifie, honore, annule, no_show
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Index pour les requêtes fréquentes du dashboard admin
CREATE INDEX IF NOT EXISTS idx_leads_statut ON leads(statut);
CREATE INDEX IF NOT EXISTS idx_interactions_client ON interactions(client_id);
CREATE INDEX IF NOT EXISTS idx_rdv_date ON rendez_vous(date_prevue);

-- Quelques véhicules de départ pour tester (à adapter au stock réel du concessionnaire)
INSERT INTO vehicules (modele, version, prix_catalogue, disponible) VALUES
    ('Clio', 'Techno TCe 100', 189900, true),
    ('Kardian', 'Evolution', 199900, true),
    ('Express', 'Van', 249900, true)
ON CONFLICT DO NOTHING;
