import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://sn.coinafrique.com/categorie/"

CATEGORIES = {
    "Vêtements Homme": "vetements-homme",
    "Chaussures Homme": "chaussures-homme",
    "Vêtements Enfants": "vetements-enfants",
    "Chaussures Enfants": "chaussures-enfants",
}


def scrape_page(slug: str, page: int) -> list[dict]:
    """
    Scrape une seule page d'une catégorie CoinAfrique.

    Returns:
        list[dict] avec les clés : categorie, nom, prix, adresse, image_lien
    """
    url = f"{BASE_URL}{slug}?page={page}"
    data = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.find_all("div", class_="col s6 m4 l3")

        for container in containers:
            try:
                a_tag = container.find("a", title=True)
                nom = a_tag["title"].strip() if a_tag else ""

                prix_el = container.find("p", class_="ad__card-price")
                prix = prix_el.get_text(strip=True) if prix_el else ""

                adr_el = container.find("p", class_="ad__card-location")
                adresse = (
                    adr_el.get_text(separator=" ", strip=True)
                    .replace("location_on", "")
                    .strip()
                    if adr_el
                    else ""
                )

                img_el = container.find("img", class_="ad__card-img")
                image_lien = (
                    (img_el.get("src") or img_el.get("data-src") or "")
                    if img_el
                    else ""
                )

                if nom and prix:
                    data.append({
                        "categorie": slug,
                        "nom": nom,
                        "prix": prix,
                        "adresse": adresse,
                        "image_lien": image_lien,
                    })
            except Exception:
                continue

    except Exception as e:
        print(f"  [!] Erreur page {page} ({slug}) : {e}")

    return data


def scrape_categorie(slug: str, nb_pages: int = 9, progress_callback=None) -> pd.DataFrame:
    """
    Scrape toutes les pages d'une catégorie.

    Args:
        slug             : identifiant de la catégorie
        nb_pages         : nombre de pages à scraper
        progress_callback: fonction(page, total) appelée après chaque page

    Returns:
        pd.DataFrame
    """
    all_data = []
    for page in range(1, nb_pages + 1):
        rows = scrape_page(slug, page)
        all_data.extend(rows)
        if progress_callback:
            progress_callback(page, nb_pages)
        time.sleep(1)

    df = pd.DataFrame(all_data)
    if not df.empty:
        df = df.drop_duplicates().reset_index(drop=True)
    return df
