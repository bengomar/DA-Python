# DA-Python   - Projet 2

## Création d'un environment virtuel
```
python -m venv env
source env/bin/activate
```

## Installation des dépendances du projet
```pip install -r requirements.txt```

## Description du projet

Programme capable d'extraire des informations de livres en vente sur le site http://books.toscrape.com/.

Ce script _(un scraper)_ récupère les données des livres en parcourant toutes les catégories.
Il génère pour chaque catégorie un fichier csv contenant les informations scrapées de chaque livre
et enregistre l'image représentant sa couverture.

### Execution du programme :
    
```python books_to_scrape_ob.py```
    
- le répertoire **categories** est créé à la racine du script.
- sous **categories**, tous les répertoires des **noms de catégories** sont créés " _(ex: Travel)_.
- sous les répertoires des **noms de catégories** un fichier **csv** est généré _(ex: Travel_details.csv)_ ainsi qu'un répertoire **images** contenant les fichiers jpg des couvertures des livres de la catégorie concernée.

