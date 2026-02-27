import re
import os
import pandas as pd
import streamlit as st
import plotly.express as px

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


def clean_prix(prix_str):
    cleaned = re.sub(r"[^\d]", "", str(prix_str))
    return int(cleaned) if cleaned else None


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def normalize(df, slug):
    df = df.copy()
    rename_map = {}
    for old, new in [("type_habits", "nom"), ("Type chaussure", "nom"),
                     ("Prix", "prix"), ("Adresse", "adresse"), ("Image-src", "image_lien")]:
        if old in df.columns:
            rename_map[old] = new
    df = df.rename(columns=rename_map)
    if "image_lien" not in df.columns:
        df["image_lien"] = ""
    df["categorie"] = slug
    cols = [c for c in ["categorie", "nom", "prix", "adresse", "image_lien"] if c in df.columns]
    return df[cols]


@st.cache_data
def load_data():
    frames = []
    for slug, (filename, sep) in FILES.items():
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path, sep=sep, encoding="utf-8", on_bad_lines="skip")
        frames.append(normalize(df, slug))
    df_all = pd.concat(frames, ignore_index=True)
    df_all = df_all[~df_all["prix"].str.contains("demande", case=False, na=True)]
    df_all["prix_num"] = df_all["prix"].apply(clean_prix)
    df_all = df_all.dropna(subset=["prix_num", "nom"]).reset_index(drop=True)
    df_all = df_all[df_all["nom"].str.strip() != ""]
    df_all["categorie_label"] = df_all["categorie"].map(CAT_LABELS)
    return df_all


df_all = load_data()

# ── Filtres sidebar ──
st.sidebar.markdown("### Filtres")

all_labels = list(CAT_LABELS.values())
selected_labels = st.sidebar.multiselect(
    "Catégorie",
    options=all_labels,
    default=all_labels,
)

prix_min_abs = int(df_all["prix_num"].min())
prix_max_abs = int(df_all["prix_num"].max())
prix_range = st.sidebar.slider(
    "Fourchette de prix (CFA)",
    min_value=prix_min_abs,
    max_value=prix_max_abs,
    value=(prix_min_abs, prix_max_abs),
    step=500,
)

df = df_all[
    df_all["categorie_label"].isin(selected_labels if selected_labels else all_labels) &
    df_all["prix_num"].between(prix_range[0], prix_range[1])
]

# ── Titre ──
st.title("📊 Dashboard — Données CoinAfrique")
st.markdown("Visualisation des données **nettoyées** issues de Web Scraper.")

# ── Métriques ──
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total annonces",   f"{len(df):,}")
c2.metric("Catégories",       len(df["categorie"].unique()))
c3.metric("Prix moyen (CFA)", f"{int(df['prix_num'].mean()):,}")
c4.metric("Prix min (CFA)",   f"{int(df['prix_num'].min()):,}")
c5.metric("Prix max (CFA)",   f"{int(df['prix_num'].max()):,}")
st.markdown("---")

# ── Ligne 1 : Répartition + Distribution ──
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Annonces par catégorie")
    count_df = df["categorie_label"].value_counts().reset_index()
    count_df.columns = ["categorie", "nb_annonces"]
    fig1 = px.bar(
        count_df, x="categorie", y="nb_annonces", color="categorie",
        labels={"categorie": "Catégorie", "nb_annonces": "Nombre d'annonces"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True, key="fig_bar_cat")

with col_b:
    st.subheader("Distribution des prix par catégorie")
    fig2 = px.box(
        df, x="categorie_label", y="prix_num", color="categorie_label",
        labels={"categorie_label": "Catégorie", "prix_num": "Prix (CFA)"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True, key="fig_box_prix")

# ── Ligne 2 : Histogram + Top villes ──
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Histogramme des prix")
    fig3 = px.histogram(
        df, x="prix_num", color="categorie_label", nbins=50,
        labels={"prix_num": "Prix (CFA)", "categorie_label": "Catégorie"},
        color_discrete_sequence=px.colors.qualitative.Set2,
        barmode="overlay", opacity=0.75,
    )
    fig3.update_layout(legend_title="Catégorie")
    st.plotly_chart(fig3, use_container_width=True, key="fig_hist_prix")

with col_d:
    st.subheader("Top 10 villes")
    top_villes = (
        df["adresse"].str.split(",").str[0].str.strip()
        .value_counts().head(10).reset_index()
    )
    top_villes.columns = ["ville", "nb_annonces"]
    fig4 = px.bar(
        top_villes, x="nb_annonces", y="ville", orientation="h",
        labels={"nb_annonces": "Nombre d'annonces", "ville": "Ville"},
        color="nb_annonces", color_continuous_scale="Oranges",
    )
    fig4.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True, key="fig_bar_villes")

# ── Tableau ──
with st.expander("Voir les données filtrées"):
    st.dataframe(
        df[["categorie_label", "nom", "prix", "adresse"]].reset_index(drop=True),
        use_container_width=True,
    )
    st.download_button(
        "⬇️ Télécharger les données nettoyées",
        data=to_csv_bytes(df.drop(columns=["prix_num", "categorie_label"])),
        file_name="coinafrique_nettoye.csv",
        mime="text/csv",
    )
