import os
import pandas as pd
import streamlit as st

from utils.scraper import CATEGORIES, scrape_categorie
from utils.database import get_connection, init_db, save_scraped_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "coinafrique_bs4.db")


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def get_db_stats():
    """Retourne le nb d'entrées par catégorie dans la DB."""
    try:
        conn = get_connection(DB_PATH)
        init_db(conn)
        df = pd.read_sql_query(
            "SELECT categorie, COUNT(*) as nb FROM annonces GROUP BY categorie",
            conn
        )
        conn.close()
        return df
    except Exception:
        return pd.DataFrame(columns=["categorie", "nb"])


# ── Titre ──
st.title("🔍 Scraper des données en direct")
st.markdown("Scraping en temps réel depuis [CoinAfrique Sénégal](https://sn.coinafrique.com) via `requests + BeautifulSoup`.")

st.markdown("---")

# ── Paramètres ──
col1, col2 = st.columns(2)
with col1:
    label    = st.selectbox("Catégorie", list(CATEGORIES.keys()))
    slug     = CATEGORIES[label]
with col2:
    nb_pages = st.slider("Nombre de pages", min_value=1, max_value=20, value=3)

if st.button("🚀 Lancer le scraping", use_container_width=True):
    progress_bar = st.progress(0, text="Démarrage...")

    def update_progress(p, total):
        progress_bar.progress(p / total, text=f"Page {p}/{total}...")

    df = scrape_categorie(slug, nb_pages=nb_pages, progress_callback=update_progress)
    progress_bar.progress(1.0, text="Terminé !")

    if df.empty:
        st.warning("Aucune donnée collectée. Vérifie ta connexion ou réessaie.")
    else:
        # ── Métriques rapides ──
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Annonces collectées", f"{len(df):,}")
        c2.metric("Doublons détectés",   f"{df.duplicated().sum():,}")
        c3.metric("Villes uniques",      df["adresse"].str.split(",").str[0].nunique())
        c4.metric("Pages scrapées",      nb_pages)

        st.dataframe(df, use_container_width=True)

        # ── Boutons ──
        col_dl, col_db = st.columns(2)
        with col_dl:
            st.download_button(
                "⬇️ Télécharger CSV",
                data=to_csv_bytes(df),
                file_name=f"{slug}_{nb_pages}pages.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col_db:
            st.session_state["scraped_df"] = df
            if st.button("💾 Sauvegarder en base de données", use_container_width=True):
                conn = get_connection(DB_PATH)
                init_db(conn)
                n = save_scraped_data(df, conn)
                conn.close()
                st.success(f"{n} lignes sauvegardées dans `coinafrique_bs4.db`.")
                st.cache_data.clear()

st.markdown("---")

# ── État de la base de données ──
st.subheader("État de la base de données")

db_stats = get_db_stats()

CAT_LABELS = {
    "vetements-homme":    "Vêtements Homme",
    "chaussures-homme":   "Chaussures Homme",
    "vetements-enfants":  "Vêtements Enfants",
    "chaussures-enfants": "Chaussures Enfants",
}

if db_stats.empty:
    st.info("La base de données est vide. Lance un scraping et sauvegarde les résultats.")
else:
    total_db = db_stats["nb"].sum()
    st.caption(f"Total en base : **{total_db:,} annonces** réparties sur {len(db_stats)} catégorie(s)")

    cols = st.columns(len(CAT_LABELS))
    for col, (slug_key, label_key) in zip(cols, CAT_LABELS.items()):
        row = db_stats[db_stats["categorie"] == slug_key]
        nb  = int(row["nb"].values[0]) if not row.empty else 0
        col.metric(label_key, f"{nb:,}")
