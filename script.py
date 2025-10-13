import os
import shutil

# NE PLUS LANCER LE SCRIPT

# Dossier source
myPathSource = "TD_DATALAKE/DATALAKE/0_SOURCE_WEB"

# Dossiers cibles
path_linkedin_emp = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"
path_glassdoor_avi = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/AVI"
path_glassdoor_soc = "TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC"

meta_path = "TD_DATALAKE/DATALAKE/99_METADATA"
meta_file = "metadata_technique.csv"
meta_full_path = os.path.join(meta_path, meta_file)

myListOfFileSourceTmp = os.listdir(myPathSource)

rows = []
rows.append(["cle_unique", "colonne", "valeur"])

cle_unique = 0  

print("******** Début de copie des fichiers ********")

for myFileName in myListOfFileSourceTmp:
    src_file = os.path.join(myPathSource, myFileName)
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

    print(f"Copie du fichier : {src_file} -- vers --> {dst_file}")

    shutil.copy(src_file, dst_file)
    
with open(meta_full_path, "w", newline='', encoding="utf-8") as csvfile:
writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerows(rows)

print("******** Fin de copie des fichiers ********")