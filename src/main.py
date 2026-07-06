"""Point d'entrée de Scribe : audio -> transcription -> compte rendu.

Enchaîne les deux briques du pipeline, affiche le compte rendu à l'écran
et l'enregistre dans un fichier daté. Les messages de progression partent
sur stderr pour que stdout ne contienne que le compte rendu (et reste donc
redirigeable proprement avec `>`).
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Lancé directement (python src/main.py), sys.path pointe sur src/ et non
# sur la racine du projet : on ajoute la racine pour que `src` soit importable.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.summarize import summarize
from src.transcribe import transcribe


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scribe",
        description="Transforme un enregistrement audio en compte rendu structuré.",
    )
    parser.add_argument("audio", help="chemin du fichier audio à transcrire")
    parser.add_argument(
        "--json",
        action="store_true",
        help="produit un compte rendu JSON exploitable par programme, au lieu du Markdown",
    )
    args = parser.parse_args()

    try:
        print(f"[1/2] Transcription de {args.audio} en cours...", file=sys.stderr)
        transcript = transcribe(args.audio)
        print(
            f"[1/2] Transcription terminée ({len(transcript)} caractères).",
            file=sys.stderr,
        )
        print("[2/2] Rédaction du compte rendu en cours...", file=sys.stderr)
        report = summarize(transcript, json_mode=args.json)
        print("[2/2] Compte rendu rédigé.", file=sys.stderr)
    except (FileNotFoundError, RuntimeError) as exc:
        sys.exit(f"Erreur : {exc}")

    horodatage = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    extension = "json" if args.json else "md"
    output = Path(f"compte_rendu_{Path(args.audio).stem}_{horodatage}.{extension}")
    output.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nCompte rendu enregistré dans : {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
