import os
import osmnx as ox
import requests
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

load_dotenv()

API_KEY = os.getenv("STREET_VIEW_API_KEY", "")

OUTPUT_DIR = "final_images"

DISTRITOS_POR_CATEGORIA = {
    "Alto": [
        "Miraflores, Lima, Peru",
        "San Isidro, Lima, Peru",
        "La Molina, Lima, Peru",
        "San Borja, Lima, Peru",
    ],
    "Medio": [
        "Los Olivos, Lima, Peru",
        "Breña, Lima, Peru",
        "Lince, Lima, Peru",
        "La Victoria, Lima, Peru",
    ],
    "Bajo": [
        "Villa El Salvador, Lima, Peru",
        "Villa Maria del Triunfo, Lima, Peru",
        "San Juan de Lurigancho, Lima, Peru",
        "Carabayllo, Lima, Peru",
    ],
}

IMAGENES_POR_DISTRITO = 1800


def crear_estructura_directorios():
    base_path = Path(OUTPUT_DIR)
    base_path.mkdir(exist_ok=True)

    for categoria in DISTRITOS_POR_CATEGORIA.keys():
        categoria_path = base_path / categoria
        categoria_path.mkdir(exist_ok=True)

    print(f"📁 Estructura de directorios creada en: {base_path.absolute()}\n")
    return base_path


def descargar_red_vial(lugar):
    try:
        graph = ox.graph_from_place(lugar, network_type="drive")
        return graph
    except Exception as e:
        print(f"      ❌ Error descargando red vial: {e}")
        return None


def seleccionar_puntos_aleatorios(graph, n_puntos):
    nodos = list(graph.nodes(data=True))
    nodos_seleccionados = random.sample(nodos, min(n_puntos, len(nodos)))

    puntos = []
    for node_id, data in nodos_seleccionados:
        lat = data["y"]
        lon = data["x"]
        puntos.append((lat, lon))

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
        return False


def descargar_distrito(distrito, categoria, base_path, stats_lock):
    distrito_corto = distrito.split(",")[0]
    print(f"\n📍 [{categoria}] Procesando: {distrito_corto}")

    print(f"   🗺️  Descargando red vial de {distrito_corto}...")
    graph = descargar_red_vial(distrito)

    if graph is None:
        print(f"   ❌ No se pudo descargar red vial de {distrito_corto}")
        return {"descargadas": 0, "saltadas": IMAGENES_POR_DISTRITO}

    n_nodos = len(graph.nodes)
    print(f"   ✅ Red descargada: {n_nodos:,} intersecciones")

    puntos = seleccionar_puntos_aleatorios(graph, IMAGENES_POR_DISTRITO)
    print(f"   🎲 Seleccionados {len(puntos)} puntos aleatorios")

    categoria_path = base_path / categoria
    stats_local = {"descargadas": 0, "saltadas": 0}

    print(f"   📸 Descargando imágenes...")
    imagenes_descargadas_contador = 0

    for i, (lat, lon) in enumerate(puntos, 1):
        if imagenes_descargadas_contador >= IMAGENES_POR_DISTRITO:
            break

        print(f"      [{i}/{IMAGENES_POR_DISTRITO}] ", end="", flush=True)

        if not verificar_street_view(lat, lon, API_KEY):
            print("❌ No hay Street View")
            stats_local["saltadas"] += 1
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = (
            categoria_path
            / f"{categoria}_{distrito_corto}_{imagenes_descargadas_contador+1:02d}_{timestamp}.jpg"
        )

        if descargar_imagen(lat, lon, API_KEY, filename):
            imagenes_descargadas_contador += 1
            stats_local["descargadas"] += 1
            print(f"✅ {filename.name}")
        else:
            print("❌ Error al descargar")
            stats_local["saltadas"] += 1

    print(
        f"   ✅ {distrito_corto} completado: {stats_local['descargadas']} descargadas / {stats_local['saltadas']} saltadas\n"
    )
    return stats_local


def descargar_todas_categorias(base_path):
    print("\n" + "=" * 70)
    print("📸 DESCARGANDO IMÁGENES DE STREET VIEW (CONCURRENTE)")
    print("=" * 70)

    stats = {
        "descargadas": {cat: 0 for cat in DISTRITOS_POR_CATEGORIA.keys()},
        "saltadas": {cat: 0 for cat in DISTRITOS_POR_CATEGORIA.keys()},
        "total_descargadas": 0,
        "total_saltadas": 0,
    }

    stats_lock = threading.Lock()

    tareas = []
    for categoria, distritos in DISTRITOS_POR_CATEGORIA.items():
        for distrito in distritos:
            tareas.append((distrito, categoria))

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(
                descargar_distrito, distrito, categoria, base_path, stats_lock
            ): (distrito, categoria)
            for distrito, categoria in tareas
        }

        for future in as_completed(futures):
            distrito, categoria = futures[future]
            try:
                stats_local = future.result()

                with stats_lock:
                    stats["descargadas"][categoria] += stats_local["descargadas"]
                    stats["saltadas"][categoria] += stats_local["saltadas"]
                    stats["total_descargadas"] += stats_local["descargadas"]
                    stats["total_saltadas"] += stats_local["saltadas"]

            except Exception as e:
                print(f"❌ Error procesando {distrito}: {e}")

    return stats


def mostrar_resumen_final(stats):
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70 + "\n")

    print("Por categoría:")
    for categoria in DISTRITOS_POR_CATEGORIA.keys():
        desc = stats["descargadas"][categoria]
        salt = stats["saltadas"][categoria]
        total_esperado = len(DISTRITOS_POR_CATEGORIA[categoria]) * IMAGENES_POR_DISTRITO
        print(
            f"  {categoria:10s}: {desc:3d} descargadas / {salt:3d} saltadas / {total_esperado:3d} esperadas"
        )

    print(f"\n{'=' * 70}")
    print(f"  ✅ Total descargadas: {stats['total_descargadas']}")
    print(f"  ❌ Total saltadas: {stats['total_saltadas']}")
    print(f"  💰 Costo estimado: ${stats['total_descargadas'] * 0.007:.2f} USD")
    print(f"  📁 Ubicación: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 70 + "\n")


def main():
    print("\n" + "=" * 70)
    print("🌎 DESCARGADOR DE IMÁGENES NSE SIMPLIFICADO")
    print("=" * 70 + "\n")

    if not API_KEY or API_KEY == "":
        print("❌ ERROR: Debes configurar tu STREET_VIEW_API_KEY en el archivo .env")
        print("\n📝 Crea un archivo .env con:")
        print('   STREET_VIEW_API_KEY="tu_api_key_aqui"')
        return

    print(f"📊 Configuración:")
    print(f"   • Categorías: {len(DISTRITOS_POR_CATEGORIA)}")
    print(
        f"   • Distritos totales: {sum(len(d) for d in DISTRITOS_POR_CATEGORIA.values())}"
    )
    print(f"   • Imágenes por distrito: {IMAGENES_POR_DISTRITO}")
    print(
        f"   • Total imágenes esperadas: {sum(len(d) for d in DISTRITOS_POR_CATEGORIA.values()) * IMAGENES_POR_DISTRITO}\n"
    )

    base_path = crear_estructura_directorios()

    stats = descargar_todas_categorias(base_path)

    mostrar_resumen_final(stats)

    print("🎉 ¡Proceso completado!")
    print(f"   Revisa las imágenes en: {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
