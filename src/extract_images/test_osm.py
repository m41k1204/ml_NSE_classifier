import osmnx as ox
import requests
import random
from pathlib import Path
from datetime import datetime

API_KEY = ""

LUGAR = "Miraflores, Lima, Peru"

OUTPUT_DIR = "imagenes_test_osm"


def descargar_red_vial(lugar):
    print(f"📥 Descargando red vial de: {lugar}")
    print("   (Esto puede tomar 10-30 segundos la primera vez...)\n")

    try:
        graph = ox.graph_from_place(lugar, network_type="drive")

        n_nodos = len(graph.nodes)
        n_calles = len(graph.edges)

        print(f"✅ Red descargada:")
        print(f"   • {n_nodos} intersecciones")
        print(f"   • {n_calles} segmentos de calle\n")

        return graph

    except Exception as e:
        print(f"❌ Error descargando red: {e}")
        print("\n💡 Sugerencia: Prueba con otro nombre de distrito:")
        print("   - 'San Isidro, Lima, Peru'")
        print("   - 'Barranco, Lima, Peru'")
        print("   - 'Surco, Lima, Peru'")
        return None


def seleccionar_puntos_aleatorios(graph, n_puntos):
    print(f"🎲 Seleccionando {n_puntos} puntos aleatorios en calles...\n")

    nodos = list(graph.nodes(data=True))

    nodos_seleccionados = random.sample(nodos, min(n_puntos, len(nodos)))

    puntos = []
    for i, (node_id, data) in enumerate(nodos_seleccionados, 1):
        lat = data["y"]
        lon = data["x"]
        puntos.append((lat, lon))

        print(f"  {i:2d}. Lat: {lat:.6f}, Lon: {lon:.6f}")

    print()
    return puntos


def verificar_street_view(lat, lon, api_key):
    url = (
        f"https://maps.googleapis.com/maps/api/streetview/metadata?"
        f"location={lat},{lon}&key={api_key}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        return data.get("status") == "OK"
    except:
        return False


def descargar_imagen(lat, lon, api_key, filename):
    url = (
        f"https://maps.googleapis.com/maps/api/streetview?"
        f"size=640x640&"
        f"location={lat},{lon}&"
        f"fov=90&"
        f"pitch=0&"
        f"heading=0&"
        f"key={api_key}"
    )

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
        else:
            return False

    except Exception as e:
        print(f"      Error: {e}")
        return False


def main():
    print("\n" + "=" * 70)
    print("🌎 DESCARGADOR DE IMÁGENES CON OPENSTREETMAP")
    print("=" * 70 + "\n")

    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)

    graph = descargar_red_vial(LUGAR)

    if not graph:
        print("❌ No se pudo continuar sin la red vial")
        return

    puntos = seleccionar_puntos_aleatorios(graph, 10)

    print("📸 Descargando imágenes de Street View...\n")

    descargadas = 0
    saltadas = 0

    for i, (lat, lon) in enumerate(puntos, 1):
        print(f"  Imagen {i}/10: ", end="")

        if not verificar_street_view(lat, lon, API_KEY):
            print("❌ No hay Street View disponible")
            saltadas += 1
            continue

        filename = output_path / f"lima_{i:02d}.jpg"

        if descargar_imagen(lat, lon, API_KEY, filename):
            print(f"✅ Descargada → {filename.name}")
            descargadas += 1
        else:
            print("❌ Error al descargar")
            saltadas += 1

    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"  ✅ Descargadas: {descargadas}")
    print(f"  ❌ Saltadas: {saltadas}")
    print(f"  💰 Costo: ${descargadas * 0.007:.3f} USD")
    print(f"  📁 Ubicación: {output_path.absolute()}")
    print("=" * 70 + "\n")

    if descargadas > 0:
        print("🎉 ¡Listo! Revisa las imágenes descargadas")
        print(f"   Abre la carpeta: {OUTPUT_DIR}/")
    else:
        print("⚠️  No se descargó ninguna imagen")
        print("   Prueba con otro distrito o verifica tu API key")


if __name__ == "__main__":
    if API_KEY == "TU_API_KEY_AQUI":
        print("\n❌ ERROR: Debes configurar tu API_KEY primero")
        print("\n📝 Edita el archivo y cambia esta línea:")
        print('   API_KEY = "TU_API_KEY_AQUI"')
        print("\n   Por tu API key real, ejemplo:")
        print('   API_KEY = "AIzaSyABC123..."')
        print()
    else:
        main()
