# -*- coding: utf-8 -*-

import csv
import os
import re
import unicodedata

from Datalake_Parametrage import myPathRoot_CURRATEDZONE, myPathRoot_PRODUCTIONZONE


def normalize_key(text):
    """
    Normalise un texte pour la comparaison ou le stockage propre :
    - Met en minuscules
    - Supprime les accents (diacritiques)
    - Remplace toute ponctuation non-alphanumérique (tirets, virgules...) par un espace
    - Réduit les espaces multiples à un seul
    """
    if not text:
        return ""

    s = str(text).lower()

    s = unicodedata.normalize('NFD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8')

    s = re.sub(r'[^a-z0-9\s]', ' ', s)

    s = re.sub(r'\s+', ' ', s).strip()
    return s


chemin_fichier_entree = os.path.join(myPathRoot_CURRATEDZONE, "METADONNEES", "metadata_descriptive.csv")

nom_fichier_societes = os.path.join(myPathRoot_PRODUCTIONZONE, 'societes.csv')
nom_fichier_emplois = os.path.join(myPathRoot_PRODUCTIONZONE, 'emplois.csv')
nom_fichier_avis = os.path.join(myPathRoot_PRODUCTIONZONE, 'avis.csv')


def parse_location(raw):
    """
    Retourne un dict avec keys: city, postal_code, region, country.
    Valeurs vides ('') quand manquantes.
    LES VALEURS RETOURNÉES (SAUF POSTAL) SONT NORMALISÉES.
    """
    if not raw:
        return {'city': '', 'postal_code': '', 'region': '', 'country': ''}

    s = raw.strip()

    parts_brutes = [p.strip() for p in s.split(',') if p.strip()]

    parts = [normalize_key(p) for p in parts_brutes if p.strip()]


    def is_postal_token(tok):
        return bool(re.match(r'^\d{2,5}$', tok))

    postal = ''
    city = ''
    region = ''
    country = ''

    if len(parts) == 1:
        token = parts[0]

        m = re.match(r'^(\d{2,5})\s+(.*)$', token)
        if m:
            postal = m.group(1)
            city = m.group(2)
        elif is_postal_token(token):
            postal = token
        else:
            city = token
    else:
        if is_postal_token(parts[0]):
            postal = parts[0]
            city = parts[1] if len(parts) > 1 else ''
            region = parts[2] if len(parts) > 2 else ''
            country = parts[3] if len(parts) > 3 else ''
        else:
            possible_country_brut = parts_brutes[-1]
            possible_country_norm = parts[-1]

            if possible_country_brut.upper() in ('FR', 'FRA') or 'france' in possible_country_norm:
                country = possible_country_norm
                if len(parts) == 2:
                    city = parts[0]
                elif len(parts) == 3:
                    city = parts[0]
                    region = parts[1]
                else:
                    city = parts[0]

                    region = ' '.join(parts[1:-1]) if len(parts) > 2 else ''
            else:

                city = parts[0]
                region = parts[1] if len(parts) > 1 else ''
                country = parts[-1] if len(parts) > 2 else ''

    return {
        'city': city or '',
        'postal_code': postal or '',
        'region': region or '',
        'country': country or ''
    }

offres_emploi_pivot = {}

try:
    with open(chemin_fichier_entree, mode='r', encoding='utf-8') as fichier_source:
        lecteur_csv = csv.reader(fichier_source, delimiter=';')

        for ligne in lecteur_csv:
            if len(ligne) == 3:
                cle_str, colonne, valeur = [part.strip() for part in ligne]

                try:
                    cle_originale = int(cle_str)
                    if cle_originale not in offres_emploi_pivot:
                        offres_emploi_pivot[cle_originale] = {}
                    offres_emploi_pivot[cle_originale][colonne] = valeur
                except ValueError:
                    pass
            else:
                pass

except FileNotFoundError:
    exit()


liste_societes = []
liste_emplois = []
liste_avis = []

societes_ajoutees = {}
societe_id_compteur = 1
emploi_id_compteur = 1
avis_id_compteur = 1

def clean_value(v):
    """Nettoie une valeur : gère None, strip, et 'NULL'."""
    if v is None:
        return ''
    s = v.strip()
    return '' if s.upper() == 'NULL' else s

for offre_data in offres_emploi_pivot.values():


    nom_societe_brut = offre_data.get('nomSociete') or offre_data.get('nomEntreprise') or ''

    nom_societe_nettoye = clean_value(nom_societe_brut)

    if not nom_societe_nettoye:
        continue
    cle_societe = normalize_key(nom_societe_nettoye)

    if not cle_societe:
        continue

    loc = parse_location(offre_data.get('villeEmploi'))

    if cle_societe not in societes_ajoutees:
        current_societe_id = societe_id_compteur

        societes_ajoutees[cle_societe] = current_societe_id

        liste_societes.append({
            'idsociete': current_societe_id,
            'nomsociete': nom_societe_nettoye,
            'villeSociete': loc['city'],
            'codePostalSociete': loc['postal_code'],
            'regionSociete': loc['region'],
            'paysSociete': loc['country']
        })
        societe_id_compteur += 1
    else:
        current_societe_id = societes_ajoutees[cle_societe]


    libelle_emploi_nettoye = clean_value(offre_data.get('libelleEmploi'))

    if libelle_emploi_nettoye:
        loc_emploi = parse_location(offre_data.get('villeEmploi'))

        liste_emplois.append({
            'idemploi': emploi_id_compteur,
            'libelleEmploi': libelle_emploi_nettoye,
            'villeEmploi': loc_emploi['city'],
            'codePostalEmploi': loc_emploi['postal_code'],
            'regionEmploi': loc_emploi['region'],
            'paysEmploi': loc_emploi['country'],
            'descriptifemploi': clean_value(offre_data.get('Descriptif')),
            'idsociete': current_societe_id
        })
        emploi_id_compteur += 1


    note_moyenne = clean_value(offre_data.get('noteMoyEntreprise'))

    for i in range(1, 11):
        key_lib = f'avis{i}_lib'
        key_comment = f'avis{i}_commentaire'
        key_avantages = f'avis{i}_avantages'
        key_inconv = f'avis{i}_inconvenients'

        titre_avis = clean_value(offre_data.get(key_lib))
        description_avis = clean_value(offre_data.get(key_comment))
        avantage_avis = clean_value(offre_data.get(key_avantages))
        inconvenient_avis = clean_value(offre_data.get(key_inconv))

        if any([titre_avis, description_avis, avantage_avis, inconvenient_avis, note_moyenne]):

            if i > 1 and not any([titre_avis, description_avis, avantage_avis, inconvenient_avis]):
                break

            liste_avis.append({
                'idavis': avis_id_compteur,
                'idsociete': current_societe_id,
                'titreAvis': titre_avis,
                'descriptionAvis': description_avis,
                'avantageAvis': avantage_avis,
                'inconvenientAvis': inconvenient_avis,
                'noteMoyenneAvis': note_moyenne
            })
            avis_id_compteur += 1

            if not any([titre_avis, description_avis, avantage_avis, inconvenient_avis]):
                break



headers_societe = ['idsociete', 'nomsociete', 'villeSociete', 'codePostalSociete', 'regionSociete', 'paysSociete']
with open(nom_fichier_societes, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers_societe, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(liste_societes)

headers_emploi = ['idemploi', 'libelleEmploi', 'villeEmploi', 'codePostalEmploi', 'regionEmploi', 'paysEmploi', 'descriptifemploi', 'idsociete']
with open(nom_fichier_emplois, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers_emploi, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(liste_emplois)

headers_avis = ['idavis', 'idsociete', 'titreAvis', 'descriptionAvis', 'avantageAvis', 'inconvenientAvis', 'noteMoyenneAvis']
with open(nom_fichier_avis, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers_avis, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(liste_avis)

