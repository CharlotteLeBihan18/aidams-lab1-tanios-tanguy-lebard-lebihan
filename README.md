# aidams-lab1-tanios-tanguy-lebard-lebihan

Geospatial Data Analysis Lab — Steel Plants Dataset (AIDAMS)

## Groupe

| # | Nom complet | Student ID |
|---|---|---|
| 1 | Charlotte Le Bihan | B00818310 |
| 2 | Ines Lebard | B00820964 |
| 3 | Camille Tanguy | B00821659 |
| 4 | Oceane Tanios | B00822694 |

## Description

Ce projet analyse le dataset **Global Iron and Steel Tracker** (Global Energy Monitor) :

- Exploration et analyse statistique des usines sidérurgiques (localisation, capacité, propriétaires)
- Visualisations géospatiales interactives avec Plotly
- Fusion des données d'exposition socio-économique **LitPop** (ETH Zurich — population et valeur d'actifs) avec les localisations des usines
- Agrégation des indicateurs au niveau des entreprises
- Dashboard interactif avec Streamlit

## Structure du projet

```
.
├── lab_1.ipynb                                          # Notebook principal (analyse complète)
├── app.py                                                # Dashboard Streamlit
├── data/                                                 # Données steel plants
├── litpop/                                               # Échantillons LitPop (.hdf5)
│   ├── LitPop_pc_300_arcsec_CHN_v1.hdf5
│   ├── LitPop_pc_300_arcsec_IND_v1.hdf5
│   └── LitPop_pc_300_arcsec_JPN_v1.hdf5
├── Plant-level_data_Global_Iron_and_Steel_Tracker...xlsx # Dataset source
├── requirements.txt                                      # Dépendances Python
└── README.md
```

## Installation

Ce projet utilise [`uv`](https://github.com/astral-sh/uv) pour la gestion de l'environnement virtuel.

```bash
# Créer et activer l'environnement virtuel
uv venv
source .venv/bin/activate

# Installer les dépendances
uv pip install -r requirements.txt
```

Dépendances principales : `pandas`, `numpy`, `plotly`, `matplotlib`, `openpyxl`, `h5py`, `tables`, `shapely`, `nbformat`, `streamlit`.

## Données requises

1. **Steel plants** : télécharger le fichier plant-level depuis le [Global Iron and Steel Tracker](https://globalenergymonitor.org/projects/global-iron-steel-tracker) et le placer à la racine du projet.
2. **LitPop (exposure/population)** : échantillons disponibles sur Moodle, à placer dans le dossier `litpop/`.

## Utilisation

### Notebook

Ouvrir `lab_1.ipynb` dans VS Code ou Jupyter, sélectionner le kernel `.venv`, puis exécuter les cellules dans l'ordre (Parties 1 à 6).

### Dashboard

```bash
streamlit run app.py
```

## Lien Streamlit Cloud (bonus)

_À compléter si déployé._

## Notes de développement

- Environnement géré avec `uv` (`pyproject.toml` + `uv.lock`).
- `.venv/` et fichiers de données volumineux sont exclus via `.gitignore`.