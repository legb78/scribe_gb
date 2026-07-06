# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio
(réunion, cours, note vocale) en compte rendu écrit et structuré.

Le fonctionnement tient en trois temps :

1. L'utilisateur fournit un fichier audio.
2. Un modèle de transcription (Speech-to-Text) convertit l'audio en texte brut.
3. Un LLM reformule ce texte en compte rendu propre : titre, points clés, décisions, actions.

Les deux modèles sont appelés via l'API serverless de Groq.

## Installation

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine (voir `.env.example`) avec votre clé API Groq.

## Utilisation

*À compléter au fil du développement.*

## Réponses aux questions du TP

- **Q1 : pourquoi le `.gitignore` doit-il exister avant d'écrire la moindre ligne de code manipulant des secrets ?**
  Parce que Git n'oublie rien : un fichier commité reste lisible dans l'historique pour
  toujours, même si on le supprime au commit suivant. Une clé API qui passe une seule fois
  dans un commit poussé sur GitHub doit être considérée comme volée (des robots scannent
  les dépôts publics en permanence). En ignorant `.env` avant même qu'il existe, la fuite
  devient impossible : `git add .` ne pourra jamais l'embarquer, même par étourderie.
  Faire l'inverse (coder d'abord, ignorer ensuite) repose sur la vigilance humaine, et
  c'est exactement comme ça que les fuites arrivent.
- **Q2 : quels modèles STT et LLM propose Groq aujourd'hui, et lesquels choisissez-vous ?**

  **Côté STT**, Groq propose en production deux variantes de Whisper :
  `whisper-large-v3` (0,111 $/h d'audio) et `whisper-large-v3-turbo` (0,04 $/h).
  Nous choisissons **`whisper-large-v3-turbo`** : sa qualité de transcription est
  quasi identique à celle de large-v3 sur de l'audio de réunion classique, pour un
  coût presque trois fois moindre et une transcription plus rapide. Le modèle
  large-v3 complet ne se justifierait que pour de l'audio très dégradé (bruit fort,
  accents difficiles), où sa légère avance en précision compte.

  **Côté LLM**, le catalogue de production comprend `llama-3.1-8b-instant`
  (560 tokens/s, 0,05/0,08 $ par million de tokens), `llama-3.3-70b-versatile`
  (280 tokens/s, 0,59/0,79 $), `openai/gpt-oss-120b` (500 tokens/s, 0,15/0,60 $)
  et `openai/gpt-oss-20b` (1000 tokens/s, 0,075/0,30 $), plus des systèmes
  agentiques (`groq/compound`) et des modèles en préversion (Llama 4 Scout,
  Qwen, etc.) déconseillés en production.
  Nous choisissons **`llama-3.3-70b-versatile`** : c'est le meilleur rédacteur
  *en français* du catalogue (le multilinguisme fait partie de son entraînement
  officiel, là où les gpt-oss sont surtout optimisés pour l'anglais), il suit
  fidèlement des consignes de structuration (titre, points clés, décisions,
  actions), et sa vitesse comme son coût restent largement suffisants pour notre
  usage : un compte rendu représente quelques milliers de tokens, soit une
  fraction de centime par exécution. Si le coût devenait un critère dominant,
  `openai/gpt-oss-120b` serait l'alternative naturelle (moins cher et plus
  rapide, au prix d'un français un peu moins naturel).

  Ces deux identifiants sont définis à un seul endroit du projet :
  [src/config.py](src/config.py).
- **Q3** — *à rédiger*
- **Q4** — *à rédiger*
- **Q5** — *à rédiger*
