@echo off
echo ====================================
echo  CRM Intelligent SMOFT - Demarrage
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo [2/3] Verification du modele...
if not exist "crm_scoring_model.pkl" (
    echo Modele non trouve. Entrainement en cours...
    python demo\scoring_model.py
)

echo.
echo [3/3] Demarrage de l'API...
echo.
echo ============================================
echo  API disponible sur: http://localhost:8000
echo  Interface Web: Ouvrez web/index.php
echo ============================================
echo.

python demo\api.py
