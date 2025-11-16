@echo off
cd /d "%~dp0"
cd ..\PYTHON

echo ******** Lancement Pipeline Complet ********
echo.

echo Phase 1 - Ingestion...
python Datalake_Phase1_Ingestion.py
echo.

echo Phase 2 - Extraction...
python Datalake_Phase2_Extraction.py
echo.

echo Phase 3 - Transformation ETL...
python Datalake_Phase3_Transformation_ETL.py
echo.

echo ******** Pipeline Termine ********
pause
