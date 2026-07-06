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
- **Q2** — *à rédiger*
- **Q3** — *à rédiger*
- **Q4** — *à rédiger*
- **Q5** — *à rédiger*
