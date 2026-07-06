"""Mode conversation : poser des questions sur le compte rendu généré.

Tout le mécanisme tient dans la liste `messages` : à chaque tour on y ajoute
la question de l'utilisateur PUIS la réponse du modèle, et on renvoie
l'historique complet à l'API. Le modèle ne « se souvient » de rien d'autre
que ce qu'on lui renvoie : cet historique EST sa mémoire.
Le compte rendu, placé dans le prompt système en tête de conversation, est
la partie stable de chaque requête — celle que le cache de préfixe peut
resservir à chaque tour (cf. Q5 du README).
"""

import sys
from pathlib import Path

# Lancé directement (python src/chat.py), sys.path pointe sur src/ et non
# sur la racine du projet : on ajoute la racine pour que `src` soit importable.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from groq import Groq, GroqError

from src import config
from src.summarize import _read_text_file

CHAT_PROMPT_FILE = config.PROJECT_ROOT / "prompts" / "system_prompt_chat.txt"


def chat(compte_rendu: str) -> None:
    """Boucle interactive de questions/réponses ancrées sur le compte rendu.

    Sort proprement sur `quit`, `exit` ou Ctrl+C. Lève FileNotFoundError si
    le prompt système est introuvable.
    """
    if not CHAT_PROMPT_FILE.is_file():
        raise FileNotFoundError(f"Prompt système introuvable : {CHAT_PROMPT_FILE}")
    system_prompt = CHAT_PROMPT_FILE.read_text(encoding="utf-8").replace(
        "{compte_rendu}", compte_rendu
    )

    client = Groq(api_key=config.GROQ_API_KEY)
    messages = [{"role": "system", "content": system_prompt}]

    print(
        "Mode chat : posez vos questions sur le compte rendu"
        " (quit ou exit pour sortir).",
        file=sys.stderr,
    )

    while True:
        try:
            question = input("\nVous > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nFin de la conversation.", file=sys.stderr)
            return
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            print("Fin de la conversation.", file=sys.stderr)
            return

        messages.append({"role": "user", "content": question})
        try:
            response = client.chat.completions.create(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                messages=messages,
            )
        except GroqError as exc:
            # On retire la question restée sans réponse pour garder un
            # historique cohérent (alternance user/assistant), et on continue.
            messages.pop()
            print(f"Erreur de l'API Groq : {exc}", file=sys.stderr)
            print("La question n'a pas été prise en compte, réessayez.", file=sys.stderr)
            continue

        reponse = response.choices[0].message.content
        print(f"\nScribe > {reponse}")
        messages.append({"role": "assistant", "content": reponse})


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python -m src.chat <fichier_compte_rendu>")
    source = Path(sys.argv[1])
    if not source.is_file():
        sys.exit(f"Erreur : compte rendu introuvable : {source}")
    try:
        chat(_read_text_file(source))
    except (FileNotFoundError, RuntimeError) as exc:
        sys.exit(f"Erreur : {exc}")
