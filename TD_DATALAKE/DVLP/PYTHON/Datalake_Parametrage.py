# -*- coding: utf-8 -*-

#==============================================================================
#== Variables et parametres pour l'application CREATION DATALAKE
#==============================================================================

import os

# Calcul du chemin de base (remonte de DVLP/PYTHON vers TD_DATALAKE)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#------------------------------------------------------------------------------
#-- Chemins des zones du Data Lakehouse
#------------------------------------------------------------------------------
myPathRoot_DATASOURCE = os.path.join(BASE_DIR, "DATALAKE", "0_SOURCE_WEB")
myPathRoot_LANDINGZONE = os.path.join(BASE_DIR, "DATALAKE", "1_LANDING_ZONE")
myPathRoot_CURRATEDZONE = os.path.join(BASE_DIR, "DATALAKE", "2_CURATED_ZONE")
myPathRoot_PRODUCTIONZONE = os.path.join(BASE_DIR, "DATALAKE", "3_PRODUCTION_ZONE")
myPathRoot_METADATA = os.path.join(BASE_DIR, "DATALAKE", "99_METADATA")

