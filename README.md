# DA-Python   - Projet 2

## Création d'un environment virtuel
```python -m venv env```

## Installation des dépendances du projet
```pip install -r requirements.txt```

## Description du projet
```./book_to_scrape_ob.py```

Programme capable d'extraire des informations de livres en vente sur le site http://books.toscrape.com/.

Ce script _(un scraper)_ récupère les données des livres en parcourant toutes les catégories.
Il génère pour chaque catégorie un fichier csv contenant les informations scrapées de chaque livre
et enregistre l'image représentant sa couverture.

### Execution du programme :
    
- le répertoire **categories** est créé à la racine du script.
- sous **categories**, tous les répertoires des **noms de catégories** sont créés " _(Travel)_.
- sous les répertoires des **noms de catégories** un fichier **csv** est généré _(Travel_details.csv)_ ainsi qu'un repertoires **images** contenant un fichier jpg de la couverture du livre.

