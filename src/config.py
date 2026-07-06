"""Configuration centrale de Scribe.

Charge la clé API Groq depuis le fichier `.env` à la racine du projet
(via python-dotenv) et centralise les identifiants des modèles.
C'est le SEUL endroit du projet où les noms de modèles apparaissent :
pour changer de modèle, on ne modifie que ce fichier.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Ce fichier vit dans src/ ; la racine du projet est un niveau au-dessus.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

# --- Modèles Groq ---
STT_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"

# Proche de zéro : le compte rendu doit restituer fidèlement la transcription,
# pas faire preuve de créativité (voir Q4 du README).
LLM_TEMPERATURE = 0.15

# --- Secrets ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    sys.exit(
        "Erreur de configuration : la variable GROQ_API_KEY est absente ou vide.\n"
        f"  1. Copiez .env.example vers .env à la racine du projet ({PROJECT_ROOT})\n"
        "  2. Renseignez-y votre clé API Groq (à créer sur https://console.groq.com/keys)"
    )
