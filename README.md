# Projet Data Lakehouse - Analyse emplois LinkedIn & Glassdoor

## 📋 Description du projet

Mise en œuvre d'un pipeline complet de traitement et d'ingestion de données HTML (LinkedIn et Glassdoor) en Data Lakehouse, avec architecture en zones et processus ETL.

### Objectif

Collecter, traiter et analyser des données sur :
- **Emplois** (LinkedIn)
- **Entreprises** (Glassdoor)
- **Avis employés** (Glassdoor)

## 🏗️ Architecture technique

### Zones du Data Lakehouse

```
TD_DATALAKE/
├── DATALAKE/
│   ├── 0_SOURCE_WEB/          # Données sources brutes (HTML)
│   ├── 1_LANDING_ZONE/        # Zone d'ingestion
│   │   ├── LINKEDIN/EMP/      # Offres d'emploi
│   │   ├── GLASSDOOR/SOC/     # Informations entreprises
│   │   └── GLASSDOOR/AVI/     # Avis employés
│   ├── 2_CURATED_ZONE/        # Données extraites et nettoyées
│   │   └── METADONNEES/       # Métadonnées descriptives
│   ├── 3_PRODUCTION_ZONE/     # Données structurées pour BI
│   └── 99_METADATA/           # Métadonnées techniques
│
└── DVLP/
    ├── PYTHON/                # Scripts Python par phase
    └── BATCH/                 # Scripts d'orchestration (.bat)
```

### Les 3 phases du pipeline

| Phase | Nom | Description | Entrée | Sortie |
|-------|-----|-------------|--------|--------|
| **1** | Ingestion | Copie fichiers HTML vers Landing Zone | 0_SOURCE_WEB | 1_LANDING_ZONE + metadata_technique.csv |
| **2** | Extraction | Parse HTML et extrait données descriptives | 1_LANDING_ZONE | 2_CURATED_ZONE/metadata_descriptive.csv |
| **3** | Transformation ETL | Transforme en tables relationnelles | 2_CURATED_ZONE | 3_PRODUCTION_ZONE (societes.csv, emplois.csv, avis.csv) |

> **Note sur la Phase 4 (Visualisation)** : Les données de la zone PRODUCTION sont directement exploitables dans l'outil BI (Qlik Sense). Les agrégations et calculs sont effectués en temps réel dans le dashboard, ce qui permet une plus grande flexibilité d'analyse sans nécessiter de prétraitement supplémentaire.

## 🚀 Utilisation

### Prérequis

```bash
pip install pandas beautifulsoup4
```

### Lancement du pipeline complet

**Sous Windows** :
```bash
cd TD_DATALAKE\DVLP\BATCH
00-Lancement_Pipeline_Complet.bat
```

**Sous Linux/Mac** :
```bash
cd TD_DATALAKE/DVLP/PYTHON
python Datalake_Programme_Principal.py
```

### Lancement d'une phase spécifique

**Scripts BATCH (Windows)** :
```bash
cd TD_DATALAKE\DVLP\BATCH
01-Phase1_Ingestion.bat              # Phase 1 uniquement
02-Phase2_Extraction.bat             # Phase 2 uniquement
03-Phase3_Transformation_ETL.bat     # Phase 3 uniquement
```

**Python direct** :
```bash
cd TD_DATALAKE/DVLP/PYTHON
python Datalake_Programme_Principal.py 1  # Lance uniquement la phase 1
python Datalake_Programme_Principal.py 2  # Lance uniquement la phase 2
python Datalake_Programme_Principal.py 3  # Lance uniquement la phase 3
```

**Ou lancer les scripts directement** :
```bash
cd TD_DATALAKE/DVLP/PYTHON
python Datalake_Phase1_Ingestion.py
python Datalake_Phase2_Extraction.py
python Datalake_Phase3_Transformation_ETL.py
```

## 📊 Modèle de données

### Tables produites (3_PRODUCTION_ZONE)

#### 1. societes.csv
```
idsociete | nomsociete | villeSociete | codePostalSociete | regionSociete | paysSociete
```

#### 2. emplois.csv
```
idemploi | libelleEmploi | villeEmploi | codePostalEmploi | regionEmploi | paysEmploi | descriptifemploi | idsociete
```

#### 3. avis.csv
```
idavis | idsociete | titreAvis | descriptionAvis | avantageAvis | inconvenientAvis | noteMoyenneAvis
```

### Dashboard BI

Le dashboard Qlik Sense (`Dashboard.pdf`) charge directement les 3 fichiers CSV de production et effectue les agrégations suivantes :
- **Top 10 sociétés** par nombre d'offres
- **Carte géographique** avec répartition des offres par ville
- **Analyse de performance** (scatter plot : nombre d'avis vs note moyenne)
- **Notes moyennes** par société

## 📁 Structure des fichiers Python

```python
Datalake_Parametrage.py              # Configuration centralisée (chemins, constantes)
Datalake_Phase1_Ingestion.py         # Phase 1 : Ingestion vers Landing Zone
Datalake_Phase2_Extraction.py        # Phase 2 : Parsing HTML et extraction
Datalake_Phase3_Transformation_ETL.py # Phase 3 : ETL vers Production
Datalake_Programme_Principal.py      # Orchestrateur du pipeline (lance les 3 phases)
```

## 📝 Métadonnées

### Métadonnées Techniques (99_METADATA/metadata_technique.csv)

Format vertical :
```csv
cle_unique;colonne;valeur
0;date_heure_de_recuperation;2025-01-15 10:30:00
0;nom_du_fichier_html;INFO-EMP-LINKEDIN-E001.html
0;provenance_du_fichier_html;/path/source
0;localisation_du_fichier_html;/path/landing
0;categorie;LINKEDIN_EMP
```

### Métadonnées Descriptives (2_CURATED_ZONE/METADONNEES/metadata_descriptive.csv)

Format vertical :
```csv
cle_unique;colonne;valeur
0;nomSociete;Société XYZ
0;villeEmploi;Lyon
0;libelleEmploi;Data Engineer
0;Descriptif;Description complète...
```

## 🎯 Livrables

- [x] Scripts Python (Phases 1, 2, 3)
- [x] Scripts BATCH d'orchestration
- [x] Fichiers CSV de métadonnées (techniques et descriptives)
- [x] Fichiers CSV production (societes, emplois, avis)
- [x] Dashboard Qlik Sense avec visualisations
- [x] Modèle décisionnel (schéma relationnel)
- [x] Architecture en zones (Landing, Curated, Production)
- [x] Documentation (README)

## 📈 Utilisation avec SQL / BI

Le fichier `seed_data.sql` contient :
- Les scripts de création de tables PostgreSQL
- Les procédures stockées pour charger les dimensions et faits
- Le modèle en étoile (dimensions + tables de faits)

```sql
-- Chargement des données dans PostgreSQL
\i TD_DATALAKE/DATALAKE/3_PRODUCTION_ZONE/seed_data.sql

-- Puis charger les CSV avec COPY ou outil d'import
```

---

**Date** : Novembre 2025
**Framework** : Python + BeautifulSoup + Pandas

