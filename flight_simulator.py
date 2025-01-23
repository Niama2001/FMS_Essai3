"""Simulateur de vol avec waypoints"""
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import os
from src.data.airports import AIRPORTS
from src.data.aircraft import AIRCRAFT
from src.data.waypoints import WAYPOINTS
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcule la distance entre deux points en km (formule de Haversine)"""
    R = 6371  # Rayon de la Terre en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def calculate_total_distance(points):
    """Calcule la distance totale d'une route avec waypoints"""
    total = 0
    for i in range(len(points)-1):
        p1, p2 = points[i], points[i+1]
        total += calculate_distance(p1['lat'], p1['lon'], p2['lat'], p2['lon'])
    return total

class FlightSimulator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simulateur de Vol")
        self.window.geometry("800x600")
        
        # Variables
        self.departure_var = tk.StringVar()
        self.arrival_var = tk.StringVar()
        self.aircraft_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principale
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame contrôles
        control_frame = ttk.LabelFrame(main_frame, text="Contrôles de vol", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Sélection départ
        ttk.Label(control_frame, text="Aéroport de départ:").grid(row=0, column=0, padx=5, pady=5)
        departure_cb = ttk.Combobox(control_frame, textvariable=self.departure_var)
        departure_cb['values'] = [f"{code} - {data['name']}" for code, data in AIRPORTS.items()]
        departure_cb.grid(row=0, column=1, padx=5, pady=5)
        
        # Sélection arrivée
        ttk.Label(control_frame, text="Aéroport d'arrivée:").grid(row=1, column=0, padx=5, pady=5)
        arrival_cb = ttk.Combobox(control_frame, textvariable=self.arrival_var)
        arrival_cb['values'] = departure_cb['values']
        arrival_cb.grid(row=1, column=1, padx=5, pady=5)
        
        # Sélection avion
        ttk.Label(control_frame, text="Type d'avion:").grid(row=2, column=0, padx=5, pady=5)
        aircraft_cb = ttk.Combobox(control_frame, textvariable=self.aircraft_var)
        aircraft_cb['values'] = [f"{code} - {data['name']}" for code, data in AIRCRAFT.items()]
        aircraft_cb.grid(row=2, column=1, padx=5, pady=5)
        
        # Bouton calcul
        ttk.Button(control_frame, text="Calculer la route", 
                  command=self.calculate_route).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Frame informations
        info_frame = ttk.LabelFrame(main_frame, text="Informations de vol", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        # Labels d'information
        self.distance_label = ttk.Label(info_frame, text="Distance: - km")
        self.distance_label.pack(pady=2)
        
        self.time_label = ttk.Label(info_frame, text="Temps de vol: - min")
        self.time_label.pack(pady=2)
        
        self.fuel_label = ttk.Label(info_frame, text="Carburant nécessaire: - L")
        self.fuel_label.pack(pady=2)
        
        self.altitude_label = ttk.Label(info_frame, text="Altitude de croisière: - m")
        self.altitude_label.pack(pady=2)
        
        # Frame waypoints
        waypoints_frame = ttk.LabelFrame(main_frame, text="Waypoints", padding="10")
        waypoints_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.waypoints_list = tk.Listbox(waypoints_frame)
        self.waypoints_list.pack(fill=tk.BOTH, expand=True)
    
    def calculate_route(self):
        """Calcule et affiche la route"""
        try:
            # Récupérer les codes
            dep_code = self.departure_var.get().split(' - ')[0]
            arr_code = self.arrival_var.get().split(' - ')[0]
            aircraft_code = self.aircraft_var.get().split(' - ')[0]
            
            if not all([dep_code, arr_code, aircraft_code]):
                messagebox.showerror("Erreur", "Veuillez sélectionner tous les champs")
                return
            
            # Récupérer les données
            dep_data = AIRPORTS[dep_code]
            arr_data = AIRPORTS[arr_code]
            aircraft_data = AIRCRAFT[aircraft_code]
            
            # Récupérer les waypoints
            route_key = f"{dep_code}-{arr_code}"
            route_waypoints = WAYPOINTS.get(route_key, [])
            
            # Créer la liste complète des points
            route_points = [{'name': dep_data['name'], 'lat': dep_data['lat'], 
                           'lon': dep_data['lon'], 'altitude': dep_data['altitude']}]
            route_points.extend(route_waypoints)
            route_points.append({'name': arr_data['name'], 'lat': arr_data['lat'], 
                               'lon': arr_data['lon'], 'altitude': arr_data['altitude']})
            
            # Calculer la distance totale
            total_distance = calculate_total_distance(route_points)
            
            # Calculer le temps de vol
            flight_time = total_distance / aircraft_data['speed']  # en heures
            
            # Calculer la consommation de carburant
            fuel_needed = total_distance * aircraft_data['consumption']
            
            # Vérifier si le vol est possible
            if fuel_needed > aircraft_data['fuel_capacity']:
                messagebox.showwarning(
                    "Attention",
                    "Le vol n'est pas possible avec la capacité en carburant de cet avion!"
                )
                return
            
            # Mettre à jour l'interface
            self.distance_label.config(text=f"Distance: {total_distance:.0f} km")
            self.time_label.config(text=f"Temps de vol: {flight_time*60:.0f} min")
            self.fuel_label.config(text=f"Carburant nécessaire: {fuel_needed:.0f} L")
            self.altitude_label.config(text=f"Altitude de croisière: {aircraft_data['cruise_altitude']} m")
            
            # Mettre à jour la liste des waypoints
            self.waypoints_list.delete(0, tk.END)
            for point in route_points:
                self.waypoints_list.insert(tk.END, 
                    f"{point['name']} - Alt: {point['altitude']}m")
            
            # Créer la carte
            self._create_map(route_points, total_distance, fuel_needed)
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def _create_map(self, route_points, distance, fuel):
        """Crée et affiche la carte avec la route et les waypoints"""
        # Centrer la carte
        center_lat = sum(p['lat'] for p in route_points) / len(route_points)
        center_lon = sum(p['lon'] for p in route_points) / len(route_points)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        
        # Ajouter les marqueurs
        for i, point in enumerate(route_points):
            if i == 0:
                color = 'green'
                prefix = 'Départ'
            elif i == len(route_points) - 1:
                color = 'red'
                prefix = 'Arrivée'
            else:
                color = 'blue'
                prefix = 'Waypoint'
            
            folium.Marker(
                [point['lat'], point['lon']],
                popup=f"{prefix}: {point['name']}<br>Altitude: {point['altitude']}m",
                icon=folium.Icon(color=color)
            ).add_to(m)
        
        # Tracer la route
        route_coords = [[p['lat'], p['lon']] for p in route_points]
        folium.PolyLine(
            route_coords,
            weight=2,
            color='blue',
            opacity=0.8
        ).add_to(m)
        
        # Ajouter une légende
        legend_html = f"""
            <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px">
            <h4>Informations de vol</h4>
            <p>Distance totale: {distance:.0f} km</p>
            <p>Carburant nécessaire: {fuel:.0f} L</p>
            <p>Nombre de waypoints: {len(route_points)-2}</p>
            <p>Départ: {route_points[0]['name']} ({route_points[0]['altitude']}m)</p>
            <p>Arrivée: {route_points[-1]['name']} ({route_points[-1]['altitude']}m)</p>
            </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Sauvegarder et afficher
        map_path = "route_with_waypoints.html"
        m.save(map_path)
        webbrowser.open('file://' + os.path.realpath(map_path))
    
    def run(self):
        """Lance le simulateur"""
        self.window.mainloop()

if __name__ == "__main__":
    app = FlightSimulator()
    app.run()
