# Analyse de la Déforestation en RDC avec Google Earth Engine

Ce projet utilise Google Earth Engine et Python pour analyser l'évolution de la déforestation en République Démocratique du Congo (RDC) entre 2015 et 2025 en utilisant l'indice de végétation NDVI (Normalized Difference Vegetation Index).

## Description

Ce notebook Jupyter permet de :
- Analyser les données satellitaires Landsat 8 (Collection LANDSAT/LC08/C02/T1_L2) sur une région spécifique de la RDC
- Calculer et visualiser l'indice NDVI pour surveiller la végétation
- Générer des séquences temporelles de cartes NDVI avec animation automatique
- Exporter les résultats d'analyse NDVI sous forme de fichiers CSV vers Google Drive
- Analyser la zone définie par les coordonnées [23°E, 30°E, -4°S, 3°N]

## Prérequis

- Python 3.x
- Compte Google Earth Engine authentifié (ID projet : 259532508364)
- Les bibliothèques Python suivantes :
  - geemap
  - earthengine-api (ee)
  - datetime
  - IPython.display
  - time
  - os
  - sys

## Configuration

1. Assurez-vous d'avoir un compte Google Earth Engine actif
2. Authentifiez-vous via `ee.Authenticate()`
3. Initialisez Earth Engine avec l'ID du projet : 259532508364
4. Assurez-vous d'avoir accès à Google Drive pour l'export des données

## Fonctionnalités

### Acquisition des Données
- Filtrage des images Landsat 8 avec :
  - Collection spécifique : LANDSAT/LC08/C02/T1_L2
  - Couverture nuageuse < 20%
  - Intervalle temporel paramétrable
  - Période d'analyse : 2015-2025

### Traitement
- Calcul de l'indice NDVI utilisant les bandes SR_B5 et SR_B4
- Analyse temporelle avec des intervalles de 270 jours
- Grille d'analyse avec résolution de 1250m x 1250m

### Visualisation
- Cartes interactives avec geemap
- Code couleur NDVI :
  - Bleu : NDVI faible (-0.2)
  - Blanc : NDVI moyen
  - Vert : NDVI élevé (0.8)
- Contour de la zone d'intérêt en rouge
- Animation temporelle avec délai de 1 seconde entre les cartes
- Contrôle des couches interactif

### Export des Données
- Format : CSV
- Dossier de destination : 'NDVI_Results_RDC' sur Google Drive
- Nommage des fichiers incluant la période d'analyse
- Export automatique pour chaque intervalle temporel

## Structure des Données

Les données sont analysées et exportées avec :
- Division de la zone d'intérêt en grille de 1250m x 1250m
- Calcul de la moyenne NDVI pour chaque sous-zone
- Export des résultats au format CSV avec :
  - Coordonnées de chaque sous-zone
  - Valeur NDVI moyenne
  - Période temporelle correspondante

## Limitations

- Couverture nuageuse limitée à < 20% pour les images analysées
- Analyses limitées à la zone définie par le polygone ROI
- Traitement séquentiel des périodes temporelles
- Dépendance à une connexion Internet stable
- Temps de traitement variable selon la période analysée
- Capacité de stockage Google Drive nécessaire pour les exports