# Simulateur de Vol

Un simulateur de vol simple avec interface graphique et calcul de routes avec waypoints.

## Installation

1. Assurez-vous d'avoir Python 3.8 ou supérieur installé
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Structure du projet

```
flight_sim_clean/
├── README.md
├── requirements.txt
├── flight_simulator.py
└── src/
    ├── data/
    │   ├── __init__.py
    │   ├── airports.py      # Base de données des aéroports
    │   ├── aircraft.py      # Base de données des avions
    │   └── waypoints.py     # Points de navigation prédéfinis
    └── models/
        └── __init__.py
```

## Utilisation

1. Lancez le simulateur :
```bash
python flight_simulator.py
```

2. Dans l'interface :
   - Sélectionnez l'aéroport de départ
   - Sélectionnez l'aéroport d'arrivée
   - Choisissez un type d'avion
   - Cliquez sur "Calculer la route"

3. La carte s'ouvrira avec :
   - Point de départ (vert)
   - Waypoints (bleu)
   - Point d'arrivée (rouge)
   - Route tracée
   - Informations de vol

## Routes disponibles

- Casablanca (GMMN) - Paris (LFPG)
- Casablanca (GMMN) - Madrid (LEMD)
- Casablanca (GMMN) - Londres (EGLL)
- Madrid (LEMD) - Paris (LFPG)
- Paris (LFPG) - Francfort (EDDF)

## Flotte disponible

- Airbus A320
- Boeing 737-800
- Airbus A330-300
- Boeing 777-300ER
- Airbus A350-900
