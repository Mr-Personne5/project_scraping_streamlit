# 🛒 CoinAfrique Scraper

Application de collecte, nettoyage et visualisation des données d'annonces du site [CoinAfrique Sénégal](https://sn.coinafrique.com).

---

## Aperçu du projet

Ce projet réalise le scraping de 4 catégories d'annonces sur CoinAfrique, stocke les données dans une base SQLite et expose une application Streamlit interactive permettant de scraper, télécharger, visualiser et évaluer les données.

### Catégories scrapées

| Catégorie | URL |
|---|---|
| Vêtements Homme | `/categorie/vetements-homme` |
| Chaussures Homme | `/categorie/chaussures-homme` |
| Vêtements Enfants | `/categorie/vetements-enfants` |
| Chaussures Enfants | `/categorie/chaussures-enfants` |

### Variables collectées

| Variable | Description |
|---|---|
| `nom` | Type de vêtement ou chaussure |
| `prix` | Prix affiché (en CFA) |
| `adresse` | Localisation du vendeur |
| `image_lien` | URL de l'image de l'annonce |

---

## Structure du projet

```
Projet/
├── app.py                        # Point d'entrée Streamlit + CSS global
├── requirements.txt              # Dépendances Python
├── .gitignore
├── .streamlit/
│   └── config.toml               # Thème et configuration serveur
├── pages/
│   ├── 1_Scraping.py             # Page scraping en direct
│   ├── 2_Telechargement.py       # Page téléchargement données Web Scraper
│   ├── 3_Dashboard.py            # Page visualisation / dashboard
│   └── 4_Evaluation.py           # Page formulaire d'évaluation
├── utils/
│   ├── scraper.py                # Fonctions de scraping (requests + BeautifulSoup)
│   └── database.py               # Fonctions SQLite
├── data/
│   ├── vetement_hommes.csv       # Données Web Scraper — Vêtements Homme
│   ├── chaussures_hommes_ws.csv  # Données Web Scraper — Chaussures Homme
│   ├── vetement_enfants.csv      # Données Web Scraper — Vêtements Enfants
│   └── chaussures_enfants_ws.csv # Données Web Scraper — Chaussures Enfants
├── scraping_bs4.ipynb            # Notebook scraping BeautifulSoup
└── scraping_refactored.ipynb     # Notebook scraping Selenium (référence)
```

---

## Installation

### Prérequis

- Python 3.10+
- Git

### 1. Cloner le dépôt

```bash
git clone https://github.com/Mr-Personne5/project_scraping_streamlit.git
cd project_scraping_streamlit
```

### 2. Créer et activer l'environnement virtuel

```bash
# Créer
python -m venv .venv

# Activer — Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Activer — Windows CMD
.\.venv\Scripts\activate.bat

# Activer — macOS / Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Lancement

```bash
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

---

## Pages de l'application

### 🏠 Accueil
Vue d'ensemble avec les statistiques globales des données Web Scraper (total annonces, catégories, prix moyen) et des cartes de navigation vers chaque section.

### 🔍 Scraping
Scraping en direct depuis CoinAfrique via `requests + BeautifulSoup`.
- Sélection de la catégorie et du nombre de pages (1 à 20)
- Barre de progression en temps réel
- Métriques rapides : annonces collectées, doublons, villes uniques
- Téléchargement CSV et sauvegarde en base SQLite
- Récapitulatif de l'état de la base de données

### ⬇️ Téléchargement
Téléchargement des données brutes (non nettoyées) collectées avec Web Scraper.
- Statistiques par dataset (lignes, colonnes, valeurs manquantes)
- Aperçu des 20 premières lignes
- Bouton de téléchargement CSV par catégorie

### 📊 Dashboard
Visualisation des données nettoyées issues de Web Scraper.
- **Filtres** : catégorie (multiselect) + fourchette de prix (slider)
- **Métriques** : total annonces, catégories, prix moyen / min / max
- **Graphiques** :
  - Répartition des annonces par catégorie
  - Distribution des prix (box plot)
  - Histogramme des prix
  - Top 10 villes
- Tableau filtré + export CSV

### 📝 Évaluation
Accès aux formulaires d'évaluation de l'application via **Google Forms** et **Kobo Toolbox**.

---

## Base de données

Le fichier `coinafrique_bs4.db` (SQLite) est créé automatiquement au premier scraping.

```sql
CREATE TABLE annonces (
    categorie  TEXT,
    nom        TEXT,
    prix       TEXT,
    adresse    TEXT,
    image_lien TEXT
);
```

> **Note** : Sur Streamlit Cloud, la base de données n'est pas persistante entre les déploiements. Les données des CSV (`data/`) restent disponibles car elles sont versionnées dans le dépôt.

---

## Déploiement sur Streamlit Cloud

1. Pousser le projet sur GitHub (inclure le dossier `data/`)
2. Se connecter sur [share.streamlit.io](https://share.streamlit.io)
3. Sélectionner le dépôt et définir `app.py` comme fichier principal
4. Cliquer sur **Deploy**

---

## Technologies utilisées

| Outil | Usage |
|---|---|
| `requests` + `BeautifulSoup4` | Scraping web |
| `pandas` | Manipulation des données |
| `SQLite` | Stockage des données scrapées |
| `Streamlit` | Interface web interactive |
| `Plotly` | Visualisations interactives |
| Web Scraper (extension Chrome) | Collecte initiale des données CSV |

---

## Auteurs

Projet réalisé par Djiba Kaba dans le cadre du Master IA — Bloc 2 : Collecte de données.
