# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import os

from Datalake_Parametrage import myPathRoot_METADATA, myPathRoot_CURRATEDZONE

# ============================================================
# === PHASE 2 - EXTRACTION : Lecture du CSV et affichage des fichiers HTML
# ============================================================

metadata_path = os.path.join(myPathRoot_METADATA, "metadata_technique.csv")

metadata = pd.read_csv(metadata_path, sep=';', quotechar='"')

grouped = metadata.groupby("cle_unique")


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def extraire_libelle_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs={'class': 'topcard__title'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def extraire_nom_entreprise_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs={'class': 'topcard__flavor'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def extraire_ville_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs={'class': 'topcard__flavor topcard__flavor--bullet'})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'


#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def extraire_texte_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('div', attrs={"class": "description__text description__text--rich"})
    if not texte_tmp:
        return 'NULL'
    return texte_tmp[0].get_text(strip=True) or 'NULL'

#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le nom de l'entreprise
#==============================================================================
import re
def extraire_nom_entreprise_SOC(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs = {'class':"strong tightAll"})[0].span.contents[0]
    if (texte_tmp == []) :
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        resultat = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
    return(resultat)

#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la ville de l'entreprise
#==============================================================================
import re
def extraire_ville_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', attrs = {'class':"infoEntity"})[1].span.contents[0])

    if (texte_tmp == []) :
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)

#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la taille de l'entreprise
#==============================================================================
import re
def extraire_taille_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', attrs = {'class':"infoEntity"})[2].span.contents[0])

    if (texte_tmp == []) :
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)

 #==============================================================================
 #-- GLASSDOOR (SOCIETE) : Fonction renvoyant la description de l'entreprise
 #-- à écrire !
 #==============================================================================
import re

def extraire_description_entreprise_SOC(objet_html):
    # On essaie plusieurs sélecteurs courants pour la description
    selecteurs_possibles = [
        {'name': 'div', 'attrs': {'data-test': 'employerDescription'}},
        {'name': 'div', 'attrs': {'data-test': 'company-description'}},
        {'name': 'div', 'attrs': {'class': 'description'}},
        {'name': 'p', 'attrs': {'class': 'mainText'}}
    ]

    texte_tmp = None
    for selecteur in selecteurs_possibles:
        resultat_recherche = objet_html.find_all(selecteur['name'], attrs=selecteur['attrs'])
        if resultat_recherche:
            texte_tmp = resultat_recherche
            break # On a trouvé, on arrête de chercher

    # Si on n'a rien trouvé après avoir tout essayé
    if not texte_tmp:
        return 'NULL'

    return texte_tmp[0].get_text(strip=True) or 'NULL'

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <nom_entreprise>
#==============================================================================
def extraire_nom_entreprise_AVI (objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {"class":"header cell info"})[0].span.contents[0]
    if (texte_tmp == []) :
        resultat = 'NULL'
    else:
        resultat = texte_tmp
    return(resultat)

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <Note_moy_entreprise>
#==============================================================================
def extraire_note_moy_entreprise_AVI(objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {'class':'v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large'})[0].contents[0]
    if (texte_tmp == []) :
        resultat = 'NULL'
    else:
        resultat = texte_tmp
    return(resultat)

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant le titre de l'avis
#==============================================================================
def extraire_review_titre(objet_html_avis):
    try:
        titre_element = objet_html_avis.select_one('a.reviewLink span')

        if titre_element:
            return titre_element.get_text(strip=True) or 'NULL'

        h2 = objet_html_avis.find('h2', attrs={'class': 'summary'})
        if h2:
            return h2.get_text(strip=True) or 'NULL'

        return 'NULL'
    except Exception as e:
        return 'NULL'

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant sous forme d'une liste les avis
#                      des employés contenu dans la page web des avis société
#==============================================================================
def extraire_liste_avis_employes_sur_entreprise_AVI(objet_html):
    #------------------------------------------------------------------------------
    # Traitement de sortie si pas de page trouvee a l Url
    #------------------------------------------------------------------------------
    review_blocks = objet_html.find_all('div', attrs={'class': 'hreview'})
    #print(texte_tmp)

    if not review_blocks:
        return []
        # print("NULL")

    liste_de_page_web=[]
    #    print(liste_de_page_web)

        #------------------------------------------------------------------------------
        # Traitement de chaque fiche avis saisie sur la page web
        #------------------------------------------------------------------------------
    for i, block in enumerate(review_blocks):
        current_review = []
        #-- 0 - ID
        current_review.append(str(i)) # ID (index 0)

        #-- 1 - Note moyenne
        current_review.append(extraire_note_moy_entreprise_AVI(objet_html)) # (index 1)

        #-- 3 - Titre de l'avis
        current_review.append(extraire_review_titre(block)) # (index 2)

        #-- 5 - Employe actuel
        try:
            emp_info = block.find('span', attrs={'class': 'authorJobTitle middle reviewer'})
            current_review.append(emp_info.get_text(strip=True)) # (index 3)
        except Exception as e:
            current_review.append('NULL')

        #-- 6 - Ville de l'employe
        try:
            loc = block.find('span', attrs={'class': 'authorLocation'})
            current_review.append(loc.get_text(strip=True)) # (index 4)
        except Exception as e:
            current_review.append('NULL')

        #-- 7 - Commentaire texte libre
        try:
            comm = block.find('p', attrs={'class': 'mainText mb-0'})
            current_review.append(comm.get_text(strip=True)) # (index 5)
        except Exception as e:
            current_review.append('NULL')

        #-- 8 & 9 - Avantages / Inconvénients
        pros_cons_blocks = block.find_all('div', attrs={'class': 'mt-md common__EiReviewTextStyles__allowLineBreaks'})

        # Avantages
        try:
            if len(pros_cons_blocks) > 0:
                current_review.append(pros_cons_blocks[0].get_text(strip=True)) # (index 6)
            else:
                current_review.append('NULL')
        except Exception as e:
            current_review.append('NULL')

        # Inconvénients
        try:
            if len(pros_cons_blocks) > 1:
                current_review.append(pros_cons_blocks[1].get_text(strip=True)) # (index 7)
            else:
                current_review.append('NULL')
        except Exception as e:
            current_review.append('NULL')

        # On ajoute la liste de cet avis à la liste principale
        liste_de_page_web.append(current_review)

    return liste_de_page_web
#==============================================================================

# ============================================================
# === PARCOURS DES FICHIERS HTML ET EXTRACTION DES DONNÉES
# ============================================================

# Liste pour stocker les résultats au format clé/colonne/valeur
donnees_extraites = []

for cle, group in grouped:
    dico = dict(zip(group["colonne"], group["valeur"]))
    localisation = dico.get("localisation_du_fichier_html", "NON TROUVÉE")
    nom_fichier = dico.get("nom_du_fichier_html", "NON TROUVÉ")

    chemin_complet = localisation

    if "LINKEDIN/EMP" in localisation.upper():

        try:
            with open(chemin_complet, "r", encoding="utf-8") as f:
                contenu_html = f.read()

            objet_parser_html = BeautifulSoup(contenu_html, "html.parser")

            libelle = extraire_libelle_emploi_EMP(objet_parser_html)
            entreprise = extraire_nom_entreprise_EMP(objet_parser_html)
            ville = extraire_ville_emploi_EMP(objet_parser_html)
            texte = extraire_texte_emploi_EMP(objet_parser_html)

            # Ajout des données au format "clé / colonne / valeur"
            donnees_extraites.append({"cle_unique": cle, "colonne": "nomSociete", "valeur": entreprise})
            donnees_extraites.append({"cle_unique": cle, "colonne": "villeEmploi", "valeur": ville})
            donnees_extraites.append({"cle_unique": cle, "colonne": "libelleEmploi", "valeur": libelle})
            donnees_extraites.append({"cle_unique": cle, "colonne": "Descriptif", "valeur": texte})
            #donnees_extraites.append({"cle_unique": cle, "colonne": "localisation", "valeur": localisation})

        except FileNotFoundError:
            pass
        except Exception as e:
            pass
    elif "GLASSDOOR/SOC" in localisation.upper() :

        try:
            with open(chemin_complet, "r", encoding="utf-8") as f:
                contenu_html = f.read()

            objet_parser_html = BeautifulSoup(contenu_html, "html.parser")

            nom = extraire_nom_entreprise_SOC(objet_parser_html)
            ville = extraire_ville_entreprise_SOC(objet_parser_html)
            taille = extraire_taille_entreprise_SOC(objet_parser_html)
            description = extraire_description_entreprise_SOC(objet_parser_html)

            # Ajout des données au format "clé / colonne / valeur"
            donnees_extraites.append({"cle_unique": cle, "colonne": "nomEntreprise", "valeur": nom})
            donnees_extraites.append({"cle_unique": cle, "colonne": "villeEntreprise", "valeur": ville})
            donnees_extraites.append({"cle_unique": cle, "colonne": "tailleEntreprise", "valeur": taille})
            donnees_extraites.append({"cle_unique": cle, "colonne": "description", "valeur": description})

        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    elif "GLASSDOOR/AVI" in localisation.upper():

        try:
            with open(chemin_complet, "r", encoding="utf-8") as f:
                contenu_html = f.read()

            objet_parser_html = BeautifulSoup(contenu_html, "html.parser")

            nom = extraire_nom_entreprise_AVI(objet_parser_html)
            note_moyenne = extraire_note_moy_entreprise_AVI(objet_parser_html)
            liste_avis = extraire_liste_avis_employes_sur_entreprise_AVI(objet_parser_html)

            # Ajout des données au format "clé / colonne / valeur"
            donnees_extraites.append({"cle_unique": cle, "colonne": "nomEntreprise", "valeur": nom})
            donnees_extraites.append({"cle_unique": cle, "colonne": "noteMoyEntreprise", "valeur": note_moyenne})

            k = 0
            for i, avis in enumerate(liste_avis):
              # On vérifie qu'on a bien la liste complète (7 éléments)
                if isinstance(avis, (list, tuple)) and len(avis) > 6:
                    # On garde que "commentaire"
                    k+=1
                    donnees_extraites.append({"cle_unique": cle, "colonne": f"avis{k}_lib", "valeur": avis[2]})
                    donnees_extraites.append({"cle_unique": cle, "colonne": f"avis{k}_commentaire", "valeur": avis[5]})
                    donnees_extraites.append({"cle_unique": cle, "colonne": f"avis{k}_avantages", "valeur": avis[6]})
                    donnees_extraites.append({"cle_unique": cle, "colonne": f"avis{k}_inconvenients", "valeur": avis[7]})

        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    else :
        continue


# ============================================================
# === SAUVEGARDE EN CSV FORMAT LONG (clé / colonne / valeur)
# ============================================================

output_path = os.path.join(myPathRoot_CURRATEDZONE, "METADONNEES", "metadata_descriptive.csv")

df_resultats = pd.DataFrame(donnees_extraites)

df_resultats.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

