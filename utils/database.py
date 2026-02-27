import sqlite3
import pandas as pd

DB_PATH = "coinafrique_bs4.db"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path, check_same_thread=False)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS annonces (
            categorie  TEXT,
            nom        TEXT,
            prix       TEXT,
            adresse    TEXT,
            image_lien TEXT
        )
    """)
    conn.commit()


def save_scraped_data(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    """Insère le DataFrame dans la table annonces. Retourne le nombre de lignes insérées."""
    if df.empty:
        return 0
    df.to_sql("annonces", conn, if_exists="append", index=False)
    conn.commit()
    return len(df)


def load_all_data(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM annonces", conn)
