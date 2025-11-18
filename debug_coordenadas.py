"""
Script para debuggear por qué no se encuentran coordenadas válidas
"""
import osmnx as ox
import random
from distritos_nse import obtener_nse_por_coordenada, LIMA_BOUNDS, DISTRITOS_NSE

print("=" * 70)
print("DEBUG: Verificando bounding boxes y coordenadas")
print("=" * 70)

print("\n1. LIMA_BOUNDS:")
print(f"   lat_min: {LIMA_BOUNDS['lat_min']}")
print(f"   lat_max: {LIMA_BOUNDS['lat_max']}")
print(f"   lon_min: {LIMA_BOUNDS['lon_min']}")
print(f"   lon_max: {LIMA_BOUNDS['lon_max']}")

print("\n2. Descargando red vial...")
bbox = (
    LIMA_BOUNDS['lon_min'],
    LIMA_BOUNDS['lat_min'],
    LIMA_BOUNDS['lon_max'],
    LIMA_BOUNDS['lat_max'],
)
graph = ox.graph_from_bbox(bbox, network_type="drive")
print(f"   ✅ Red descargada: {len(graph.nodes)} nodos")

print("\n3. Muestreando 10 puntos aleatorios de la red:")
nodos = list(graph.nodes(data=True))
muestra = random.sample(nodos, 10)

for i, (node_id, data) in enumerate(muestra, 1):
    lat = data["y"]
    lon = data["x"]
    distrito, nse = obtener_nse_por_coordenada(lat, lon)
    print(f"   Punto {i}: lat={lat:.6f}, lon={lon:.6f} -> distrito={distrito}, nse={nse}")

print("\n4. Verificando algunos bounding boxes de distritos:")
for i, (distrito, zonas) in enumerate(list(DISTRITOS_NSE.items())[:3]):
    print(f"\n   {distrito}:")
    for bbox, nse in zonas:
        lat_min, lat_max, lon_min, lon_max = bbox
        print(f"      {nse}: lat=[{lat_min}, {lat_max}], lon=[{lon_min}, {lon_max}]")

print("\n5. Probando coordenadas manualmente en el centro de algunos distritos:")
test_coords = [
    (-12.10, -77.03, "Debería ser San Isidro (Alto)"),
    (-12.12, -77.03, "Debería ser Miraflores (Alto)"),
    (-12.05, -77.05, "Debería ser Lima Centro"),
]

for lat, lon, descripcion in test_coords:
    distrito, nse = obtener_nse_por_coordenada(lat, lon)
    print(f"   {descripcion}")
    print(f"      lat={lat}, lon={lon} -> distrito={distrito}, nse={nse}")

print("\n" + "=" * 70)
