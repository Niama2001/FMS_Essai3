"""Module contenant les données des waypoints"""

WAYPOINTS = {
    "GMMN-LFPG": [  # Casablanca - Paris CDG
        {"name": "BAMED", "lat": 35.5833, "lon": -5.5000, "altitude": 11000},
        {"name": "DIVKO", "lat": 39.8833, "lon": -1.1667, "altitude": 11500},
        {"name": "MENDI", "lat": 43.5000, "lon": 0.0000, "altitude": 11700},
        {"name": "LACOU", "lat": 46.0000, "lon": 1.5000, "altitude": 11300}
    ],
    "GMMN-LEMD": [  # Casablanca - Madrid
        {"name": "WALAD", "lat": 35.0000, "lon": -6.5000, "altitude": 11000},
        {"name": "SEVIL", "lat": 37.5000, "lon": -5.0000, "altitude": 11300}
    ],
    "GMMN-EGLL": [  # Casablanca - Londres
        {"name": "PORTO", "lat": 41.2481, "lon": -8.6813, "altitude": 11000},
        {"name": "BREST", "lat": 48.4472, "lon": -4.4185, "altitude": 11500}
    ],
    "LEMD-LFPG": [  # Madrid - Paris
        {"name": "RONKO", "lat": 43.0000, "lon": -1.0000, "altitude": 11000},
        {"name": "BIARRITZ", "lat": 43.4683, "lon": -1.5311, "altitude": 11300}
    ],
    "LFPG-EDDF": [  # Paris - Francfort
        {"name": "NANCY", "lat": 48.6921, "lon": 6.2301, "altitude": 11000},
        {"name": "STRASBOURG", "lat": 48.5734, "lon": 7.7521, "altitude": 11300}
    ]
}
