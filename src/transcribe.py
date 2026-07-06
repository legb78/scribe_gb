"""Transcription audio via l'API Speech-to-Text de Groq.

Contraintes de l'API (doc « Speech to Text » de la console Groq) :
formats acceptés flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm ;
taille maximale 25 Mo en offre gratuite (100 Mo en offre payante) ;
toute requête est facturée au minimum comme 10 secondes d'audio.
"""

import sys
from pathlib import Path

# Lancé directement (python src/transcribe.py), sys.path pointe sur src/ et non
# sur la racine du projet : on ajoute la racine pour que `src` soit importable.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from groq import Groq, GroqError

from src import config


def transcribe(audio_path: str | Path) -> str:
    """Retourne la transcription texte du fichier audio donné.

    Lève FileNotFoundError si le fichier n'existe pas, et RuntimeError si
    l'API Groq répond en erreur (clé invalide, format refusé, quota épuisé,
    fichier trop lourd...).
    """
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier audio introuvable : {path}")

    client = Groq(api_key=config.GROQ_API_KEY)
    try:
        with path.open("rb") as audio:
            response = client.audio.transcriptions.create(
                file=audio,
                model=config.STT_MODEL,
            )
    except GroqError as exc:
        raise RuntimeError(
            f"L'API Groq a renvoyé une erreur pendant la transcription : {exc}"
        ) from exc

    return response.text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python -m src.transcribe <fichier_audio>")
    try:
        print(transcribe(sys.argv[1]))
    except (FileNotFoundError, RuntimeError) as exc:
        sys.exit(f"Erreur : {exc}")
