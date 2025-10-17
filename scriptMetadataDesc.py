import pandas as pd
from bs4 import BeautifulSoup
import os

# ============================================================
# === PHASE 2 - EXTRACTION : Lecture du CSV et affichage des fichiers HTML
# ============================================================

metadata_path = "TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_technique.csv"

metadata = pd.read_csv(metadata_path, sep=';', quotechar='"')

print("Fichier de métadonnées chargé avec succès.\n")

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
 #==============================================================================
import re

def extraire_description_entreprise_SOC(objet_html):
    emp_basic_info = objet_html.find('div', id='EmpBasicInfo')
    texte_tmp = None
    
    if emp_basic_info:
        desc_label = emp_basic_info.find('label', string='Description')
        if desc_label:
            description_element = desc_label.find_next_sibling('span', class_='value') or \
                                  desc_label.find_next_sibling('div', class_='value')
            if description_element:
                texte_tmp = description_element.text
        
        if not texte_tmp:
             texte_tmp = emp_basic_info.find('span', attrs={'data-full': re.compile(r'.*')})
             if texte_tmp:
                 texte_tmp = texte_tmp.text
        
        if not texte_tmp:
            texte_tmp = emp_basic_info.text

    if texte_tmp and texte_tmp.strip():
        texte_tmp = re.sub(r'\s+', ' ', texte_tmp).strip()
        resultat = texte_tmp
    else:
        resultat = 'NULL'
        
    return resultat
 
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
#-- GLASSDOOR (AVIS) : Fonction renvoyant sous forme d'une liste les avis
#                      des employés contenu dans la page web des avis société
#==============================================================================
def extraire_liste_avis_employes_sur_entreprise_AVI(objet_html):
    #------------------------------------------------------------------------------
    # Traitement de sortie si pas de page trouvee a l Url
    #------------------------------------------------------------------------------
    texte_tmp = objet_parser_html.find_all('li', attrs = {'class':'empReview'})
    # print(texte_tmp)
    
    if (texte_tmp == []) : 
        pass
        # print("NULL")
    else:
        liste_de_page_web=[[]]
    #    print(liste_de_page_web)
    
        #------------------------------------------------------------------------------
        # Traitement de chaque fiche avis saisie sur la page web
        #------------------------------------------------------------------------------
        for x in range(0, len(texte_tmp)) :
            #--------------------------------------------------------------------------
            #-- 0 - ID de l'avis (arbitraire) incremental
            #--------------------------------------------------------------------------
            if x == 0: 
                liste_de_page_web[0] = ['"0"']
            else:
                liste_de_page_web.append(['"'+str(x)+'"'])
                # print("Avis n° : " + str(x+1) )
        
            #--------------------------------------------------------------------------
            #-- On recupere par une boucle les donnees XML de chaque avis
            #--------------------------------------------------------------------------
            objet_html_2 = BeautifulSoup(str(texte_tmp[x]), 'lxml')
        
            #--------------------------------------------------------------------------
            #-- 1 - Note moyenne entreprise 
            #--------------------------------------------------------------------------
            texte_tmp = (extraire_note_moy_entreprise_AVI(objet_parser_html))
            liste_de_page_web[x].append('"' + texte_tmp + '"')
            # print(x, texte_tmp)
            
        
            #--------------------------------------------------------------------------
            #-- 2 - Date Time 
            #--------------------------------------------------------------------------
            # texte_tmp = donner_datetime_actuel()
            # liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 3 - Titre de l'avis de l'employe sur la societe (review)
            #--------------------------------------------------------------------------
            # texte_tmp = extraire_review_titre ('GLASSDOOR', objet_html_2 )
            # liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 5 - Employe actuel
            #--------------------------------------------------------------------------
            texte_html_trouve = objet_html_2.find_all('span', attrs = {'class':'authorJobTitle middle reviewer'})
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(texte_html_trouve[0]))
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 6 - Ville de l'employe 
            #--------------------------------------------------------------------------
            texte_html_trouve = objet_html_2.find_all('span', attrs = {'class':'authorLocation'}) 
            if (texte_html_trouve == []) :
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(texte_html_trouve[0]))
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 7 - Commentaire texte libre employe sur entreprise
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('p', attrs = {'class':'mainText mb-0'}) 
        
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[0].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
    
            #--------------------------------------------------------------------------
            #-- 8 - Avantages
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('div', attrs = {'class':'mt-md common__EiReviewTextStyles__allowLineBreaks'}) 
        
            # print(texte_html_trouve)
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[0].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
    
    
            #--------------------------------------------------------------------------
            #-- 9 - Inconvénients
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('div', attrs = {'class':'mt-md common__EiReviewTextStyles__allowLineBreaks'}) 
        
            # print(texte_html_trouve)
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[1].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')

    return(liste_de_page_web)            
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
    
    chemin_complet = localisation.replace("/", "\\")

#    if "LINKEDIN/EMP" in localisation.upper():
#
#        print(f"\nClé unique : {cle}")
#        print(f"Nom du fichier : {nom_fichier}")
#        print(f"Localisation complète : {chemin_complet}")
#        print("-" * 80)
#
#        try:
#            with open(chemin_complet, "r", encoding="utf-8") as f:
#                contenu_html = f.read()
#
#            objet_parser_html = BeautifulSoup(contenu_html, "html.parser")
#
#            libelle = extraire_libelle_emploi_EMP(objet_parser_html)
#            entreprise = extraire_nom_entreprise_EMP(objet_parser_html)
#            ville = extraire_ville_emploi_EMP(objet_parser_html)
#            texte = extraire_texte_emploi_EMP(objet_parser_html)
#
#            # Ajout des données au format "clé / colonne / valeur"
#            donnees_extraites.append({"cle_unique": cle, "colonne": "nomSociete", "valeur": entreprise})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "villeEmploi", "valeur": ville})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "libelleEmploi", "valeur": libelle})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "Descriptif", "valeur": texte})
#            #donnees_extraites.append({"cle_unique": cle, "colonne": "localisation", "valeur": localisation})
#
#            print('=' * 80)
#            print(f"INFO EMP LINKEDIN - nom de la société ==> {entreprise}")
#            # print(f"INFO EMP LINKEDIN - ville de l'emploi ==> {ville}")
#            # print(f"INFO EMP LINKEDIN - libellé de l'emploi ==> {libelle}")
#            # print('-' * 80)
#            # print(f"INFO EMP LINKEDIN - texte descriptif ==> \n{texte[:300]}...")
#            # print('=' * 80)
#        except FileNotFoundError:
#            print("Fichier introuvable :", chemin_complet)
#            print('=' * 80)
#        except Exception as e:
#            print("Erreur lors du traitement :", e)
#            print('=' * 80)

#    elif "GLASSDOOR/SOC" in localisation.upper() :
#        
#        print(f"\nClé unique : {cle}")
#        print(f"Nom du fichier : {nom_fichier}")
#        print(f"Localisation complète : {chemin_complet}")
#        print("-" * 80)
#        
#        try:
#            with open(chemin_complet, "r", encoding="utf-8") as f:
#                contenu_html = f.read()
#
#            objet_parser_html = BeautifulSoup(contenu_html, "html.parser")
#            
#            nom = extraire_nom_entreprise_SOC(objet_parser_html)
#            ville = extraire_ville_entreprise_SOC(objet_parser_html)
#            taille = extraire_taille_entreprise_SOC(objet_parser_html)
#            description = extraire_description_entreprise_SOC(objet_parser_html)
#
#            # Ajout des données au format "clé / colonne / valeur"
#            donnees_extraites.append({"cle_unique": cle, "colonne": "nomEntreprise", "valeur": nom})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "villeEntreprise", "valeur": ville})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "tailleEntreprise", "valeur": taille})
#            donnees_extraites.append({"cle_unique": cle, "colonne": "description", "valeur": description})
#
#            print('=' * 80)
#            print(f"INFO SOC GLASSDOOR - nom de l'entreprise ==> {nom}")
#            print(f"INFO SOC GLASSDOOR - ville de l'entreprise ==> {ville}")
#            print(f"INFO SOC GLASSDOOR - taille de l'entreprise ==> {taille}")
#            print('-' * 80)
#            print(f"INFO SOC GLASSDOOR - descriptition ==> \n{description[:300]}...")
#            print('=' * 80)
#
#        except FileNotFoundError:
#            print("Fichier introuvable :", chemin_complet)
#            print('=' * 80)
#        except Exception as e:
#            print("Erreur lors du traitement :", e)
#            print('=' * 80)
    
    if "GLASSDOOR/AVI" in localisation.upper():
        print(f"\nClé unique : {cle}")
        print(f"Nom du fichier : {nom_fichier}")
        print(f"Localisation complète : {chemin_complet}")
        print("-" * 80)
        
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
            
            for i, avis in enumerate(liste_avis):
                if isinstance(avis, (list, tuple)) and len(avis) > 4:
                   valeur_avis = avis[4]
                else:
                    valeur_avis = "NULL"
                donnees_extraites.append({"cle_unique": cle, "colonne": f"avis{i}", "valeur": valeur_avis})

            print('=' * 80)
            print(f"INFO AVI GLASSDOOR - nom de l'entreprise ==> {nom}")
            print(f"INFO AVI GLASSDOOR - note moyenne de l'entreprise ==> {note_moyenne}")
            print('-' * 80)
            print(f"INFO AVI GLASSDOOR - nb d'avis sur l'entreprise ==> {len(liste_avis)}")
            for i, avis in enumerate(liste_avis):
                if i >= 3:
                    break
                if isinstance(avis, (list, tuple)) and len(avis) > 4:
                    print(f"Avis {i} : {avis[4]}")
                else:
                    print(f"Avis {i} : NULL (structure invalide ou incomplète)")
            print('=' * 80)

        except FileNotFoundError:
            print("Fichier introuvable :", chemin_complet)
            print('=' * 80)
        except Exception as e:
            print("Erreur lors du traitement :", e)
            print('=' * 80)
        
    else : 
        continue


# ============================================================
# === SAUVEGARDE EN CSV FORMAT LONG (clé / colonne / valeur)
# ============================================================

output_path = "TD_DATALAKE\\DATALAKE\\99_METADATA\\metadata_descriptive.csv"

df_resultats = pd.DataFrame(donnees_extraites)

df_resultats.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

print("\nExtraction terminée avec succès !")
print(f"Fichier sauvegardé ici : {output_path}")
