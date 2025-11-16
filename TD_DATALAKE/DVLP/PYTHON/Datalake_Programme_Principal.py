#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programme principal - Lance le pipeline complet du Data Lakehouse
Usage:
    python Datalake_Programme_Principal.py        # Lance toutes les phases
    python Datalake_Programme_Principal.py 1      # Lance uniquement la phase 1
    python Datalake_Programme_Principal.py 2      # Lance uniquement la phase 2
    python Datalake_Programme_Principal.py 3      # Lance uniquement la phase 3
"""

import sys

# Déterminer quelle(s) phase(s) exécuter
phase_a_executer = None
if len(sys.argv) > 1:
    try:
        phase_a_executer = int(sys.argv[1])
        if phase_a_executer not in [1, 2, 3]:
            print("Erreur : Le numéro de phase doit être 1, 2 ou 3")
            sys.exit(1)
    except ValueError:
        print("Erreur : Argument invalide. Usage : python Datalake_Programme_Principal.py [1|2|3]")
        sys.exit(1)

print("=" * 70)
print("PIPELINE DATA LAKEHOUSE - LANCEMENT")
if phase_a_executer:
    print(f"Mode : Exécution de la phase {phase_a_executer} uniquement")
else:
    print("Mode : Exécution complète (toutes les phases)")
print("=" * 70)

# Phase 1 : Ingestion
if phase_a_executer is None or phase_a_executer == 1:
    print("\n[PHASE 1] Ingestion des données...")
    try:
        import Datalake_Phase1_Ingestion
        print("Phase 1 terminée avec succès")
    except Exception as e:
        print(f"Erreur Phase 1 : {e}")
        sys.exit(1)

# Phase 2 : Extraction
if phase_a_executer is None or phase_a_executer == 2:
    print("\n[PHASE 2] Extraction des métadonnées...")
    try:
        import Datalake_Phase2_Extraction
        print("Phase 2 terminée avec succès")
    except Exception as e:
        print(f"Erreur Phase 2 : {e}")
        sys.exit(1)

# Phase 3 : Transformation ETL
if phase_a_executer is None or phase_a_executer == 3:
    print("\n[PHASE 3] Transformation ETL...")
    try:
        import Datalake_Phase3_Transformation_ETL
        print("Phase 3 terminée avec succès")
    except Exception as e:
        print(f"Erreur Phase 3 : {e}")
        sys.exit(1)

print("\n" + "=" * 70)
print("PIPELINE TERMINé AVEC SUCCES")
print("=" * 70)

