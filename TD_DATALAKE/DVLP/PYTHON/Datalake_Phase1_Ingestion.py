# -*- coding: utf-8 -*-

import os
import shutil
import csv
from datetime import datetime

from Datalake_Parametrage import myPathRoot_DATASOURCE, myPathRoot_LANDINGZONE, myPathRoot_METADATA

# Dossiers cibles
path_linkedin_emp = os.path.join(myPathRoot_LANDINGZONE, "LINKEDIN", "EMP")
path_glassdoor_avi = os.path.join(myPathRoot_LANDINGZONE, "GLASSDOOR", "AVI")
path_glassdoor_soc = os.path.join(myPathRoot_LANDINGZONE, "GLASSDOOR", "SOC")

meta_file = "metadata_technique.csv"
meta_full_path = os.path.join(myPathRoot_METADATA, meta_file)

myListOfFileSourceTmp = os.listdir(myPathRoot_DATASOURCE)

rows = []
rows.append(["cle_unique", "colonne", "valeur"])

cle_unique = 0

for myFileName in myListOfFileSourceTmp:
    src_file = os.path.join(myPathRoot_DATASOURCE, myFileName)
    if "LINKEDIN" in myFileName:
        dst_dir = path_linkedin_emp
    elif "AVIS-SOC-GLASSDOOR" in myFileName:
        dst_dir = path_glassdoor_avi
    elif "INFO-SOC-GLASSDOOR" in myFileName:
        dst_dir = path_glassdoor_soc
    else:
        continue

    dst_file = os.path.join(dst_dir, myFileName)
    shutil.copy(src_file, dst_file)

    rows.append([str(cle_unique), "date_heure_de_recuperation", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    rows.append([str(cle_unique), "nom_du_fichier_html", myFileName])
    rows.append([str(cle_unique), "provenance_du_fichier_html", src_file])
    rows.append([str(cle_unique), "localisation_du_fichier_html", dst_file])

    # exemple en + si besoin (à voir avec le prof):
    # rows.append([str(cle_unique), "nom_entreprise", "Business & décision"])
    # rows.append([str(cle_unique), "ville_entreprise", "Lyon 7 eme"])
    # rows.append([str(cle_unique), "note_entreprise", "3,2"])

    cle_unique += 1

with open(meta_full_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerows(rows)

