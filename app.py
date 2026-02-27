import os
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CoinAfrique Scraper",
    page_icon="🛒",
    layout="wide",
)

# ── CSS global ──
st.markdown("""
<style>
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-left: 4px solid #FF6B35;
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
[data-testid="stMetricValue"] {
    color: #FF6B35;
    font-weight: 700;
    font-size: 1.8rem !important;
}
[data-testid="stMetricLabel"] {
    color: #555;
    font-size: 0.85rem;
    font-weight: 500;
}
h1 {
    color: #1a1a2e;
    padding-bottom: 12px;
    border-bottom: 3px solid #FF6B35;
    margin-bottom: 28px;
}
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: transform 0.15s, box-shadow 0.15s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 14px rgba(255,107,53,0.30);
}
.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
    border: 1.5px solid #FF6B35 !important;
    color: #FF6B35 !important;
    background: #fff !important;
    transition: background 0.15s, color 0.15s;
}
.stDownloadButton > button:hover {
    background: #FF6B35 !important;
    color: #fff !important;
}
details {
    border: 1px solid #e8e8e8 !important;
    border-radius: 10px !important;
    overflow: hidden;
}
summary {
    background: #F5F7FA !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}
[data-testid="stSidebar"] {
    background-color: #1a1a2e !important;
}
[data-testid="stSidebar"] * {
    color: #f0f0f0 !important;
}
[data-testid="stSidebarNav"] a {
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: 500;
    transition: background 0.15s;
}
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] [aria-selected="true"] {
    background-color: rgba(255,107,53,0.2) !important;
    color: #FF6B35 !important;
}
.card {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.card-icon  { font-size: 2.4rem; margin-bottom: 8px; }
.card-title { font-size: 1.05rem; font-weight: 700; color: #1a1a2e; margin-bottom: 6px; }
.card-desc  { font-size: 0.85rem; color: #777; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown(
        "<h2 style='color:#FF6B35; margin-bottom:4px;'>🛒 CoinAfrique</h2>",
        unsafe_allow_html=True,
    )
    st.caption("Scraping · Données · Dashboard")
    st.markdown("---")

# ── Page d'accueil ──
def home():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    FILES = {
        "vetements-homme":    ("vetement_hommes.csv",       ";"),
        "chaussures-homme":   ("chaussures_hommes_ws.csv",  ","),
        "vetements-enfants":  ("vetement_enfants.csv",      ";"),
        "chaussures-enfants": ("chaussures_enfants_ws.csv", ","),
    }

    @st.cache_data
    def get_stats():
        total, prix_vals = 0, []
        for _, (filename, sep) in FILES.items():
            path = os.path.join(DATA_DIR, filename)
            df = pd.read_csv(path, sep=sep, encoding="utf-8", on_bad_lines="skip")
            total += len(df)
            prix_col = "Prix" if "Prix" in df.columns else ("prix" if "prix" in df.columns else None)
            if prix_col:
                for p in df[prix_col].dropna():
                    cleaned = re.sub(r"[^\d]", "", str(p))
                    if cleaned:
                        prix_vals.append(int(cleaned))
        return total, len(FILES), int(sum(prix_vals) / len(prix_vals)) if prix_vals else 0

    total_annonces, nb_categories, prix_moyen = get_stats()

    st.title("🛒 CoinAfrique Scraper")
    st.markdown("Plateforme de collecte et d'analyse des annonces **CoinAfrique Sénégal**.")
    st.markdown("---")

    # ── Métriques globales ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Total annonces Web Scraper", f"{total_annonces:,}")
    c2.metric("Catégories couvertes",        f"{nb_categories}")
    c3.metric("Prix moyen (CFA)",            f"{prix_moyen:,}")

    st.markdown("---")
    st.subheader("Naviguer dans l'application")

    # ── Cards ──
    cards = [
        ("🔍", "Scraping",       "Scraper des données en direct sur plusieurs pages"),
        ("⬇️", "Téléchargement", "Télécharger les données brutes Web Scraper (CSV)"),
        ("📊", "Dashboard",      "Visualiser et analyser les données nettoyées"),
        ("📝", "Évaluation",     "Donner votre avis via Google Forms ou Kobo"),
    ]

    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, cards):
        col.markdown(f"""
        <div class="card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Navigation ──
pg = st.navigation([
    st.Page(home,                        title="Accueil",        icon="🏠", default=True),
    st.Page("pages/1_Scraping.py",       title="Scraping",       icon="🔍"),
    st.Page("pages/2_Telechargement.py", title="Téléchargement", icon="⬇️"),
    st.Page("pages/3_Dashboard.py",      title="Dashboard",      icon="📊"),
    st.Page("pages/4_Evaluation.py",     title="Évaluation",     icon="📝"),
])
pg.run()
