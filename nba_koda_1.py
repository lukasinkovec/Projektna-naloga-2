import time
import csv
import json
import os
import re
import sys
import requests


def nalozi_url_v_niz(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Could not access page " + url)
        return ""
    return r.text

def pripravi_imenik(ime_datoteke):
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

def vsebina_datoteke(ime_datoteke):
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def zapisi_json(objekt, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)

vzorec1 = re.compile(r'<th scope="row" class="tdl"><a href="/players/(?P<ime>.*?)" title="', re.DOTALL)

vzorec2 = re.compile(
    r'<div itemscope itemtype="https://schema.org/Person"><h1 class="h1fjug" itemprop="name">(?P<ime>.+?)</h1><meta itemprop="mainEntityOfPage".*?'
    r'<p class="jugcab"><span itemprop="jobTitle">(?P<polozaj>(Point guard|Shooting guard|Small forward|Power forward|Center)).*?</span> \| \d+? \| <span class="jugequ".*?'
    r'<li><strong>Height:</strong> <span itemprop="height">(?P<visina>\d\.\d\d) m / \d ft \d+? in</span></li>.*?'
    r'<li><strong>Weight:</strong> <span itemprop="weight">(?P<teza>\d+?) kg / \d\d\d lbs</span></li>.*?'
    r'<li><strong>Age: </strong>\d\d&nbsp;&nbsp;&nbsp;<strong>Birth date:</strong>  <time datetime="(?P<leto>19\d\d)-\d+?-\d+?" itemprop="birthDate">\w+? \d+?, 19\d\d</time>.*?'
    r'<li><strong>Nationality:</strong> <span itemprop="nationality">(?P<drzava>.+?)</span></li>.*?'
    r'Career<td>(?P<minute>\d+?\.\d)<td class="tdn">(?P<tocke>\d+?\.\d)<td>(?P<skoki>\d+?\.\d)<td>(?P<podaje>\d+?\.\d)<td>\d+?<td>\d+?<td>\d+?</table></section>',
    re.DOTALL
)

def izloci_podatke_nba_igralca(ujemanje):
    podatki_nba_igralcev = ujemanje.groupdict()
    podatki_nba_igralcev['visina'] = float(podatki_nba_igralcev['visina'])
    podatki_nba_igralcev['teza'] = int(podatki_nba_igralcev['teza'])
    podatki_nba_igralcev['leto'] = int(podatki_nba_igralcev['leto'])
    podatki_nba_igralcev['minute'] = float(podatki_nba_igralcev['minute'])
    podatki_nba_igralcev['tocke'] = float(podatki_nba_igralcev['tocke'])
    podatki_nba_igralcev['skoki'] = float(podatki_nba_igralcev['skoki'])
    podatki_nba_igralcev['podaje'] = float(podatki_nba_igralcev['podaje'])
    return podatki_nba_igralcev

seznam_imen = []
for crka in "y":#'abcdefghijklmnopqrstuvwyz':
    url = 'https://en.hispanosnba.com/players/nba-active/{}'.format(crka)
    vsebina = nalozi_url_v_niz(url)
    for ujemanje in vzorec1.finditer(vsebina):
        seznam_imen.append(ujemanje.groupdict()["ime"])
        time.sleep(1)

for ime in seznam_imen:
    url = 'https://en.hispanosnba.com/players/{}'.format(ime)
    shrani_spletno_stran(url, 'projektna-naloga-2/zajeti-podatki/{}.html'.format(ime))
    time.sleep(1)

podatki_nba_igralcev = []
for ime in seznam_imen:
    vsebina = vsebina_datoteke('projektna-naloga-2/zajeti-podatki/{}.html'.format(ime))
    for ujemanje in vzorec2.finditer(vsebina):
        podatki_nba_igralcev.append(izloci_podatke_nba_igralca(ujemanje))
zapisi_json(podatki_nba_igralcev, 'projektna-naloga-2/obdelani-podatki/vsi-nba-igralci.json')
zapisi_csv(podatki_nba_igralcev, ['ime', 'polozaj', 'visina', 'teza', 'leto', 'drzava', 'minute', 'tocke', 'skoki', 'podaje'], 'projektna-naloga-2/obdelani-podatki/vsi-nba-igralci.csv')