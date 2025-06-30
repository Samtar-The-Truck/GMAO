# GMAO

Prototype simple de Gestion de la Maintenance Assistée par Ordinateur.

Ce projet propose une petite application de bureau écrite avec PyQt5 et SQLite. Une interface web Flask est également fournie à titre d'exemple.

Fonctionnalités principales :

- gérer une liste d'équipements ;
- enregistrer des tâches de maintenance associées à chaque équipement ;
- suivre l'état des tâches (en attente ou réalisées).
- supprimer des équipements ou des tâches.

## Prérequis

- Python 3.8 ou supérieur
- `pip` pour installer les dépendances

## Installation

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancez l'application de bureau :
   ```bash
   python desktop.py
   ```
   (l'interface web peut toujours être lancée avec `python app.py` si besoin)

Les données sont stockées dans un fichier `gmao.db` (SQLite) créé automatiquement au premier lancement.
