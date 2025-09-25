# Analyse de la Déforestation en RDC (Forest Cover Analysis in DRC)

## Description
Ce projet analyse l'évolution de la couverture forestière en République Démocratique du Congo (RDC) en utilisant des données NDVI (Normalized Difference Vegetation Index). Il permet de visualiser les changements historiques et de prédire les tendances futures de la déforestation.

## Fonctionnalités
- Analyse temporelle des données NDVI (2015-2024)
- Prédiction de la couverture forestière pour 2025
- Visualisation interactive des cartes de déforestation
- Analyse statistique des changements spatiaux
- Tableau comparatif des pertes forestières annuelles
- Imputation intelligente des données manquantes (k-NN)

## Technologies Utilisées
- Python 3.x
- Streamlit (interface utilisateur)
- Pandas & GeoPandas (manipulation de données géospatiales)
- Scikit-learn (apprentissage automatique)
- Folium (cartographie interactive)
- Matplotlib (visualisation)
- Shapely (manipulation de géométries)

## Installation

1. Cloner le dépôt :
```bash
git clone [url-du-repo]
cd NDVI_Results_RDC
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure des Données
Le projet utilise des fichiers CSV contenant les données NDVI :
- Format : NDVI_SubZones_Export_[date-début]_[date-fin].csv
- Chaque fichier contient :
  - Coordonnées (x, y)
  - Géométries des zones
  - Valeurs NDVI moyennes
  - Dates de début et de fin

## Utilisation

1. Lancer l'application :
Si streamlit est dans le PATH
```bash
streamlit run deforestation.py
```

or

Si streamlit n'est pas dans le PATH
```bash
python -m streamlit run deforestation.py
```

2. L'interface affiche :
   - Carte de prédiction NDVI
   - Comparaison d'images historiques
   - Tableau des pertes forestières
   - Métriques spatiales

## Fonctionnement du Code

### Traitement des Données
- Chargement et nettoyage des données CSV
- Gestion des zones d'eau (NDVI < -0.1)
- Imputation des valeurs manquantes par k-NN
- Création d'identifiants uniques pour chaque location

### Modélisation
- Random Forest Regressor
- Features : coordonnées (x, y), centroids, temps
- Split train/test : 80/20
- Prédiction pour 2025

### Visualisation
- Cartes choroplèthes avec échelle de couleurs personnalisée
- Bleu : eau
- Blanc : pas de données
- Vert : végétation

## Résultats
- Visualisation des changements temporels (2015-2024)
- Prédictions pour 2025
- Métriques de changement spatial :
  - Zone totale
  - Surface déboisée
  - Pourcentage de déforestation
  - Variation spatiale
  - Amplitude NDVI

## Limitations
- La précision des prédictions dépend de la qualité des données NDVI
- Les zones avec données manquantes nécessitent une imputation
- Le modèle ne prend pas en compte les facteurs externes (politique, économie)

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence
Ce projet est sous licence MIT.
