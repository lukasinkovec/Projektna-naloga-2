import time
import csv
import os
import re
import requests

nba_url = "https://en.hispanosnba.com/players/nba-active/"
nba_mapa = "nba_podatki"
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
    with open(pot, 'w', encoding='utf-8') as izhodna_datoteka:
        izhodna_datoteka.write(niz)
    return None


def shrani_url_v_html():
    for crka in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]:
        niz = nalozi_url_v_niz(nba_url + crka)
        shrani_niz_v_datoteko(niz, nba_mapa, "nba_stran_" + crka + ".html")
        time.sleep(1)
    return None

###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()

# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


def page_to_ads(page):
    '''Split "page" to a list of advertisement blocks.'''
    rx = re.compile(r'<div class="ad">(.*?)<div class="clear">',
                    re.DOTALL)
    ads = re.findall(rx, page)
    return ads

# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_ad_block(block):
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    rx = re.compile(r'title="(?P<name>.*?)"'
                    r'.*?</h3>\s*(?P<description>.*?)\s*</?div'
                    r'.*?class="price">(?P<price>.*?)</div',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()
    return ad_dict

# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(filename, directory):
    '''Parse the ads in filename/directory into a dictionary list.'''
    page = read_file_to_string(filename, directory)
    blocks = page_to_ads(page)
    ads = [get_dict_from_ad_block(block) for block in blocks]
    return ads

def ads_frontpage():
    return ads_from_file(cat_directory, frontpage_filename)

###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    '''Write a CSV file containing one ad from "ads" on each row.'''
    write_csv(ads[0].keys(), ads, directory, filename)


def write_cat_csv(ads):
    '''Save "ads" to "cat_directory"/"csv_filename"'''
    write_cat_ads_to_csv(ads, cat_directory, csv_filename)