import osmnx as ox
import requests
import random
from pathlib import Path
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import threading
from src.extract_images.distritos_nse import (
    obtener_nse_por_coordenada,
    obtener_todos_distritos,
    LIMA_BOUNDS,
    DISTRITOS_NSE,
)

load_dotenv()

API_KEY = os.getenv("STREET_VIEW_API_KEY", "")

OUTPUT_DIR = "images"

CATEGORIAS = ["Alto", "Medio alto", "Medio", "Medio bajo", "Bajo"]

IMAGENES_POR_DISTRITO = 800


def crear_estructura_directorios():
    base_path = Path(OUTPUT_DIR)
    base_path.mkdir(exist_ok=True)

    for categoria in CATEGORIAS:
        categoria_path = base_path / categoria
        categoria_path.mkdir(exist_ok=True)

    print(f"📁 Estructura de directorios creada en: {base_path.absolute()}\n")
    return base_path


_LIMA_GRAPH_CACHE = {"drive": None, "walk": None}


def descargar_red_vial_lima(network_type="drive"):
    global _LIMA_GRAPH_CACHE

    if _LIMA_GRAPH_CACHE[network_type] is not None:
        return _LIMA_GRAPH_CACHE[network_type]

    print(f"\n🗺️  Descargando red vial de Lima ({network_type})...")
    print("   (Esto puede tomar 1-2 minutos, pero solo se hace una vez)")

    try:
        from src.extract_images.distritos_nse import LIMA_BOUNDS

        lat_min = LIMA_BOUNDS["lat_min"]
        lat_max = LIMA_BOUNDS["lat_max"]
        lon_min = LIMA_BOUNDS["lon_min"]
        lon_max = LIMA_BOUNDS["lon_max"]

        bbox = (lon_min, lat_min, lon_max, lat_max)
        graph = ox.graph_from_bbox(bbox, network_type=network_type)

        _LIMA_GRAPH_CACHE[network_type] = graph
        print(
            f"   ✅ Red vial descargada ({network_type}): {len(graph.nodes):,} nodos\n"
        )
        return graph
    except Exception as e:
        print(f"   ❌ Error descargando red vial ({network_type}): {e}")
        return None


def seleccionar_puntos_en_zona(
    bbox_zona, n_puntos_objetivo, distrito, nse, graph_drive=None, graph_walk=None
):
    lat_min, lat_max, lon_min, lon_max = bbox_zona

    if graph_drive is None:
        graph_drive = descargar_red_vial_lima("drive")

    nodos_en_zona = []
    uso_walk = False

    if graph_drive and len(graph_drive.nodes) > 0:
        for node_id, data in graph_drive.nodes(data=True):
            lat = data["y"]
            lon = data["x"]
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                nodos_en_zona.append((node_id, data))

    if len(nodos_en_zona) == 0:
        uso_walk = True
        if graph_walk is None:
            graph_walk = descargar_red_vial_lima("walk")

        if graph_walk and len(graph_walk.nodes) > 0:
            for node_id, data in graph_walk.nodes(data=True):
                lat = data["y"]
                lon = data["x"]
                if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                    nodos_en_zona.append((node_id, data))

    if len(nodos_en_zona) == 0:
        return [], False

    n_seleccion = min(n_puntos_objetivo, len(nodos_en_zona))
    nodos_seleccionados = random.sample(nodos_en_zona, n_seleccion)

    puntos = []
    for node_id, data in nodos_seleccionados:
        lat = data["y"]
        lon = data["x"]
        puntos.append((lat, lon, distrito, nse))

    return puntos, uso_walk


def generar_dataset_por_distrito(imagenes_por_distrito):
    print("\n" + "=" * 70)
    print("🎲 GENERANDO COORDENADAS POR DISTRITO")
    print("=" * 70 + "\n")

    dataset = {categoria: [] for categoria in CATEGORIAS}

    total_distritos = len(DISTRITOS_NSE)
    distrito_actual = 0

    print(f"📍 Total de distritos a procesar: {total_distritos}\n")

    print("🚗 Descargando red vial para autos (drive)...")
    graph_drive = descargar_red_vial_lima("drive")

    if graph_drive is None:
        print("❌ No se pudo descargar la red vial de Lima. Abortando...")
        return dataset

    graph_walk = None

    for distrito, zonas in DISTRITOS_NSE.items():
        distrito_actual += 1
        distrito_corto = distrito.split(",")[
            0
        ]
        print(
            f"📌 [{distrito_actual}/{total_distritos}] Procesando distrito: {distrito_corto}"
        )
        print(f"   Zonas NSE: {len(zonas)}")

        puntos_por_zona = max(1, imagenes_por_distrito // len(zonas))
        puntos_restantes = imagenes_por_distrito % len(zonas)

        total_puntos_distrito = 0

        for idx, (bbox_zona, nse) in enumerate(zonas):
            n_puntos_zona = puntos_por_zona + (1 if idx < puntos_restantes else 0)

            lat_min, lat_max, lon_min, lon_max = bbox_zona
            print(f"      Zona {nse}: ", end="", flush=True)

            puntos, uso_walk = seleccionar_puntos_en_zona(
                bbox_zona, n_puntos_zona, distrito, nse, graph_drive, graph_walk
            )

            if graph_walk is None and uso_walk:
                graph_walk = _LIMA_GRAPH_CACHE.get("walk")

            if puntos:
                for lat, lon, dist, nse_punto in puntos:
                    dataset[nse_punto].append((lat, lon, dist))

                total_puntos_distrito += len(puntos)
                if uso_walk:
                    print(f"✅ {len(puntos)} puntos (🚶 walk)")
                else:
                    print(f"✅ {len(puntos)} puntos")
            else:
                print(f"⚠️  Sin puntos (zona sin calles)")

        print(
            f"   Total generados en {distrito_corto}: {total_puntos_distrito} puntos\n"
        )

    print("=" * 70)
    print("📊 RESUMEN DE COORDENADAS GENERADAS")
    print("=" * 70)
    for categoria in CATEGORIAS:
        count = len(dataset[categoria])
        print(f"  {categoria:15s}: {count:4d} puntos")
    print("=" * 70 + "\n")

    return dataset


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


def descargar_categoria(categoria, puntos, base_path, stats_lock, metadata_lock):
    print(f"\n{'=' * 70}")
    print(f"📂 [{categoria}] Iniciando descarga de {len(puntos)} puntos")
    print(f"{'=' * 70}\n")

    categoria_path = base_path / categoria
    contador_exitos = 0

    stats_local = {
        "descargadas": 0,
        "saltadas": 0,
        "intentos": 0,
    }

    metadata_local = []

    for i, (lat, lon, distrito) in enumerate(puntos, 1):
        stats_local["intentos"] += 1

        print(f"  [{categoria}] [{i}/{len(puntos)}] ", end="", flush=True)

        if not verificar_street_view(lat, lon, API_KEY):
            print("❌ No hay Street View")
            stats_local["saltadas"] += 1
            continue

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )
        filename = categoria_path / f"{categoria}_{contador_exitos:04d}_{timestamp}.jpg"

        if descargar_imagen(lat, lon, API_KEY, filename):
            contador_exitos += 1
            stats_local["descargadas"] += 1

            metadata_local.append(
                {
                    "filename": str(filename.relative_to(base_path)),
                    "categoria": categoria,
                    "lat": lat,
                    "lon": lon,
                    "distrito": distrito,
                    "timestamp": timestamp,
                }
            )

            print(f"✅ {filename.name}")
        else:
            print("❌ Error al descargar")
            stats_local["saltadas"] += 1

    print(
        f"\n✅ [{categoria}] Completado: {stats_local['descargadas']} descargadas, {stats_local['saltadas']} saltadas\n"
    )

    return stats_local, metadata_local


def descargar_imagenes_dataset(dataset, base_path):
    print("\n" + "=" * 70)
    print("📸 DESCARGANDO IMÁGENES DE STREET VIEW (PARALELO)")
    print("=" * 70 + "\n")

    stats = {
        "descargadas": {cat: 0 for cat in CATEGORIAS},
        "saltadas": {cat: 0 for cat in CATEGORIAS},
        "total_intentos": 0,
        "total_descargadas": 0,
    }

    metadata = []

    stats_lock = threading.Lock()
    metadata_lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for categoria in CATEGORIAS:
            puntos = dataset[categoria]
            future = executor.submit(
                descargar_categoria,
                categoria,
                puntos,
                base_path,
                stats_lock,
                metadata_lock,
            )
            futures[future] = categoria

        for future in futures:
            categoria = futures[future]
            try:
                stats_local, metadata_local = future.result()

                stats["descargadas"][categoria] = stats_local["descargadas"]
                stats["saltadas"][categoria] = stats_local["saltadas"]
                stats["total_intentos"] += stats_local["intentos"]
                stats["total_descargadas"] += stats_local["descargadas"]

                metadata.extend(metadata_local)

            except Exception as e:
                print(f"❌ Error en categoría {categoria}: {e}")

    metadata_file = base_path / "metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Metadata guardada en: {metadata_file}\n")

    return stats


def mostrar_resumen_final(stats):
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70 + "\n")

    print("Por categoría:")
    for categoria in CATEGORIAS:
        desc = stats["descargadas"][categoria]
        salt = stats["saltadas"][categoria]
        total = desc + salt
        print(
            f"  {categoria:15s}: {desc:3d} descargadas / {salt:3d} saltadas / {total:3d} total"
        )

    print(f"\n{'=' * 70}")
    print(f"  ✅ Total descargadas: {stats['total_descargadas']}")
    print(f"  ❌ Total saltadas: {sum(stats['saltadas'].values())}")
    print(f"  💰 Costo estimado: ${stats['total_descargadas'] * 0.007:.2f} USD")
    print(f"  📁 Ubicación: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 70 + "\n")


def main():
    print("\n" + "=" * 70)
    print("🌎 DESCARGADOR DE IMÁGENES NSE LIMA")
    print("=" * 70 + "\n")

    if not API_KEY or API_KEY == "":
        print("❌ ERROR: Debes configurar tu API_KEY primero")
        print("\n📝 Edita el archivo y cambia esta línea:")
        print('   API_KEY = ""')
        print("\n   Por tu API key real, ejemplo:")
        print('   API_KEY = "AIzaSyABC123..."')
        return

    base_path = crear_estructura_directorios()

    dataset = generar_dataset_por_distrito(IMAGENES_POR_DISTRITO)

    stats = descargar_imagenes_dataset(dataset, base_path)

    mostrar_resumen_final(stats)

    print("🎉 ¡Proceso completado!")
    print(f"   Revisa las imágenes en: {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
