import math

def calculate_distance(coord1, coord2):
    """Haversine formula to calculate distance between two GPS points in km."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def analyze_corridor_risk(current_location, hazard_zones):
    """Checks telemetry against registered hazard hotspots."""
    alerts = []
    for zone in hazard_zones:
        distance = calculate_distance(current_location, zone["coords"])
        if distance <= zone["radius_km"]:
            alerts.append({
                "hazard": zone["name"],
                "distance_km": round(distance, 2),
                "severity": zone["severity"]
            })
    return alerts