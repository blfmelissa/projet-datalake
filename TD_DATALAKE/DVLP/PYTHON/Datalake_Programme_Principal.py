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
            sys.exit(1)
    except ValueError:
        sys.exit(1)

# Phase 1 : Ingestion
if phase_a_executer is None or phase_a_executer == 1:
    try:
        import Datalake_Phase1_Ingestion
    except Exception as e:
        sys.exit(1)

# Phase 2 : Extraction
if phase_a_executer is None or phase_a_executer == 2:
    try:
        import Datalake_Phase2_Extraction
    except Exception as e:
        sys.exit(1)

# Phase 3 : Transformation ETL
if phase_a_executer is None or phase_a_executer == 3:
    try:
        import Datalake_Phase3_Transformation_ETL
    except Exception as e:
        sys.exit(1)

