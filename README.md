# GMAO

Prototype simple de Gestion de la Maintenance Assistée par Ordinateur.

Ce projet contient une petite application web écrite avec Flask et SQLite. Elle permet de :

- gérer une liste d'équipements ;
- enregistrer des tâches de maintenance associées à chaque équipement ;
- suivre l'état des tâches (en attente ou réalisées).

## Prérequis

- Python 3.8 ou supérieur
- `pip` pour installer les dépendances

## Installation

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancez l'application :
   ```bash
   python app.py
   ```
3. Ouvrez votre navigateur sur `http://localhost:5000` pour accéder à l'interface.

Les données sont stockées dans un fichier `gmao.db` (SQLite) créé automatiquement au premier lancement.
