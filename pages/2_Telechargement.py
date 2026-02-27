import os
import streamlit as st
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

CAT_LABELS = {
    "vetements-homme":    "Vêtements Homme",
    "chaussures-homme":   "Chaussures Homme",
    "vetements-enfants":  "Vêtements Enfants",
    "chaussures-enfants": "Chaussures Enfants",
}

FILES = {
    "vetements-homme":    ("vetement_hommes.csv",       ";"),
    "chaussures-homme":   ("chaussures_hommes_ws.csv",  ","),
    "vetements-enfants":  ("vetement_enfants.csv",      ";"),
    "chaussures-enfants": ("chaussures_enfants_ws.csv", ","),
}


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


st.title("⬇️ Télécharger les données Web Scraper")
st.markdown("Données **brutes (non nettoyées)** collectées avec Web Scraper.")

# ── Cartes de résumé global ──
cols = st.columns(len(FILES))
totals = {}
for col, (slug, (filename, sep)) in zip(cols, FILES.items()):
    path = os.path.join(DATA_DIR, filename)
    df_tmp = pd.read_csv(path, sep=sep, encoding="utf-8", on_bad_lines="skip")
    totals[slug] = df_tmp
    col.metric(CAT_LABELS[slug], f"{len(df_tmp):,} lignes")

st.markdown("---")

# ── Détail par dataset ──
for slug, df in totals.items():
    nb_manquants = df.isnull().sum().sum()
    pct_manquants = nb_manquants / (df.shape[0] * df.shape[1]) * 100

    with st.expander(f"📦 {CAT_LABELS[slug]} — {len(df):,} lignes", expanded=False):

        # Stats rapides
        c1, c2, c3 = st.columns(3)
        c1.metric("Lignes", f"{len(df):,}")
        c2.metric("Colonnes", df.shape[1])
        c3.metric("Valeurs manquantes", f"{nb_manquants:,} ({pct_manquants:.1f}%)")

        st.markdown("**Aperçu (20 premières lignes)**")
        st.dataframe(df.head(20), use_container_width=True)

        st.download_button(
            label=f"⬇️ Télécharger {CAT_LABELS[slug]} (CSV)",
            data=to_csv_bytes(df),
            file_name=f"{slug}_webscraper.csv",
            mime="text/csv",
            key=f"dl_{slug}",
            use_container_width=True,
        )
