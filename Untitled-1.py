import csv
import os
import re
import requests

nba_url = "https://www.nba.com/players"
nba_mapa = "nba_podatki"
nba_html = "nba.html"
nba_csv = "nba_podatki.csv"


def nalozi_url_v_niz(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Could not access page " + url)
        return ""
    return r.text

def shrani_niz_v_datoteko(niz, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, 'w', encoding='utf-8') as izhodna:
        izhodna.write(niz)
    return None