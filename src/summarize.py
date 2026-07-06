"""Rédaction du compte rendu via l'API chat completions de Groq.

Le comportement du LLM est piloté par les prompts système stockés dans
prompts/ (system_prompt.txt pour le Markdown, system_prompt_json.txt pour
le mode JSON) : pour itérer sur la qualité du compte rendu, on modifie ces
fichiers, pas le code.
"""

import json
import sys
from pathlib import Path

# Lancé directement (python src/summarize.py), sys.path pointe sur src/ et non
# sur la racine du projet : on ajoute la racine pour que `src` soit importable.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from groq import Groq, GroqError

from src import config

SYSTEM_PROMPT_FILE = config.PROJECT_ROOT / "prompts" / "system_prompt.txt"
JSON_SYSTEM_PROMPT_FILE = config.PROJECT_ROOT / "prompts" / "system_prompt_json.txt"


def summarize(transcript: str, json_mode: bool = False) -> str:
    """Retourne un compte rendu structuré de la transcription.

    Par défaut le compte rendu est du Markdown lisible ; avec json_mode=True,
    c'est une chaîne JSON (clés : titre, resume, points_cles,
    decisions_actions), garantie valide.

    Lève FileNotFoundError si le prompt système est introuvable, et
    RuntimeError si l'API Groq répond en erreur.
    """
    prompt_file = JSON_SYSTEM_PROMPT_FILE if json_mode else SYSTEM_PROMPT_FILE
    if not prompt_file.is_file():
        raise FileNotFoundError(f"Prompt système introuvable : {prompt_file}")
    system_prompt = prompt_file.read_text(encoding="utf-8")

    extra_args = {"response_format": {"type": "json_object"}} if json_mode else {}
    client = Groq(api_key=config.GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            **extra_args,
        )
    except GroqError as exc:
        raise RuntimeError(
            f"L'API Groq a renvoyé une erreur pendant la rédaction du compte rendu : {exc}"
        ) from exc

    content = response.choices[0].message.content
    if json_mode:
        try:
            json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Le LLM n'a pas renvoyé un JSON valide : {exc}"
            ) from exc
    return content


def _read_text_file(path: Path) -> str:
    """Lit un fichier texte en UTF-8, en tolérant l'UTF-16 avec lequel
    PowerShell écrit les fichiers redirigés avec `>`."""
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(
        f"Encodage de {path} non reconnu (UTF-8 ou UTF-16 attendu)."
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    json_mode = "--json" in args
    args = [a for a in args if a != "--json"]
    if len(args) != 1:
        sys.exit("Usage : python -m src.summarize <fichier_transcription.txt> [--json]")
    source = Path(args[0])
    if not source.is_file():
        sys.exit(f"Erreur : fichier de transcription introuvable : {source}")
    try:
        print(summarize(_read_text_file(source), json_mode=json_mode))
    except (FileNotFoundError, RuntimeError) as exc:
        sys.exit(f"Erreur : {exc}")
