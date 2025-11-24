"""
Script para descargar imágenes de Street View de provincias peruanas (Arequipa, Trujillo, Piura)
usando bounding boxes específicos de urbanizaciones.
Descarga 10 imágenes por urbanización de forma concurrente.
"""

import os
import osmnx as ox
import requests
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Cargar variables de entorno
load_dotenv()

# Configuración
API_KEY = os.getenv("STREET_VIEW_API_KEY", "")

# Directorio de salida
OUTPUT_DIR = "imagenes_provincias"

# Urbanizaciones: usar bbox para áreas pequeñas, nombre de distrito para áreas grandes
# Formato: (nombre_urbanizacion, bbox_o_distrito)
# Si es tupla de 4 números = bbox, si es string = nombre de distrito
URBANIZACIONES_POR_CIUDAD = {
    "Arequipa": {
        "Alto": [
            ("Cayma_1", "Cayma, Arequipa, Peru"),  # Distrito completo
            ("Yanahuara", "Yanahuara, Arequipa, Peru"),  # Distrito pequeño
        ],
        "Medio": [
            ("Bustamante_Oeste", (-16.455307, -16.433064, -71.547559, -71.524350)),
            ("Bustamante_Este", (-16.433064, -16.410821, -71.524350, -71.501140)),
        ],
        "Bajo": [
            ("Cerro_Colorado_1", "Cerro Colorado, Arequipa, Peru"),  # Distrito completo
            ("Alto_Selva_Alegre", "Alto Selva Alegre, Arequipa, Peru"),  # Distrito completo
        ],
    },
    "Trujillo": {
        "Alto": [
            ("El_Golf_Norte", (-8.162293, -8.140474, -79.070289, -79.048536)),
            ("California_Sur", (-8.140474, -8.118654, -79.048536, -79.026782)),
        ],
        "Medio": [
            ("La_Esperanza_Norte", (-8.087606, -8.063584, -79.086145, -79.058108)),
            ("La_Esperanza_Sur", (-8.063584, -8.039563, -79.058108, -79.030072)),
        ],
        "Bajo": [
            ("El_Porvenir_Oeste", (-8.089783, -8.051983, -79.036240, -78.994735)),
            ("Alto_Trujillo_Este", (-8.051983, -8.014184, -78.994735, -78.953231)),
        ],
    },
    "Piura": {
        "Alto": [
            ("Castilla_1", "Castilla, Piura, Peru"),  # Distrito completo (grande)
            ("Piura_Centro", "Piura, Piura, Peru"),  # Distrito completo
        ],
        "Medio": [
            ("Catacaos_1", "Catacaos, Piura, Peru"),  # Distrito completo (muy grande)
            ("Catacaos_2", "Catacaos, Piura, Peru"),  # Mismo distrito, segunda muestra
        ],
        "Bajo": [
            ("San_Martin_Oeste", (-5.218936, -5.168272, -80.767768, -80.703437)),
            ("26_de_Octubre_Este", (-5.168272, -5.117608, -80.703437, -80.639106)),
        ],
    },
}

# Imágenes por urbanización
IMAGENES_POR_URBANIZACION = 10


def crear_estructura_directorios():
    """Crea la estructura de carpetas para organizar las imágenes."""
    base_path = Path(OUTPUT_DIR)
    base_path.mkdir(exist_ok=True)

    # Solo crear 3 subdirectorios: Alto, Medio, Bajo
    for categoria in ["Alto", "Medio", "Bajo"]:
        categoria_path = base_path / categoria
        categoria_path.mkdir(exist_ok=True)

    print(f"📁 Estructura de directorios creada en: {base_path.absolute()}\n")
    return base_path


def descargar_red_vial_lima():
    """
    Descarga la red vial de Lima Metropolitana para usar como referencia.
    Esta función descarga una vez y cachea el resultado.
    """
    print("\n🗺️  Descargando red vial de Lima Metropolitana como base...")
    print("   (Esto puede tomar 1-2 minutos)\n")

    try:
        bbox = (-77.15, -12.40, -76.90, -11.80)
        graph = ox.graph_from_bbox(
            north=-11.80,
            south=-12.40,
            east=-76.90,
            west=-77.15,
            network_type="drive",
        )

        print(f"✅ Red vial descargada: {len(graph.nodes):,} intersecciones\n")
        return graph

    except Exception as e:
        print(f"❌ Error descargando red vial: {e}")
        return None


def descargar_red_vial_bbox(bbox):
    """
    Descarga la red vial de un bounding box específico.

    Args:
        bbox: Tupla (lat_min, lat_max, lon_min, lon_max)

    Returns:
        networkx.MultiDiGraph: Grafo con la red vial o None si falla
    """
    lat_min, lat_max, lon_min, lon_max = bbox

    try:
        # ox.graph_from_bbox requiere bbox=(north, south, east, west)
        graph = ox.graph_from_bbox(
            bbox=(lat_max, lat_min, lon_max, lon_min),
            network_type="drive",
        )
        return graph
    except Exception as e:
        print(f"      ⚠️  Error descargando bbox: {e}")
        return None


def seleccionar_puntos_aleatorios(graph, n_puntos):
    """
    Selecciona puntos aleatorios de la red vial.

    Args:
        graph: Grafo de OSMnx con la red vial
        n_puntos: Número de puntos a seleccionar

    Returns:
        list: Lista de tuplas (lat, lon)
    """
    if graph is None or len(graph.nodes) == 0:
        return []

    nodos = list(graph.nodes(data=True))
    nodos_seleccionados = random.sample(nodos, min(n_puntos, len(nodos)))

    puntos = []
    for node_id, data in nodos_seleccionados:
        lat = data["y"]
        lon = data["x"]
        puntos.append((lat, lon))

    return puntos


def verificar_street_view(lat, lon, api_key):
    """Verifica si hay Street View disponible en las coordenadas."""
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
    """
    Descarga una imagen de Street View.

    Args:
        lat: Latitud
        lon: Longitud
        api_key: Google API Key
        filename: Ruta del archivo de salida

    Returns:
        bool: True si se descargó correctamente
    """
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


def descargar_urbanizacion(urbanizacion_nombre, bbox_o_distrito, ciudad, categoria, base_path, stats_lock):
    """
    Descarga imágenes de una urbanización específica usando bbox o nombre de distrito.

    Args:
        urbanizacion_nombre: Nombre de la urbanización
        bbox_o_distrito: Bounding box (lat_min, lat_max, lon_min, lon_max) o string con nombre de distrito
        ciudad: Nombre de la ciudad (Arequipa, Trujillo, Piura)
        categoria: Categoría NSE (Alto, Medio, Bajo)
        base_path: Path al directorio base
        stats_lock: Lock para acceso seguro a estadísticas

    Returns:
        dict: Estadísticas de descarga
    """
    print(f"\n📍 [{ciudad} - {categoria}] Procesando: {urbanizacion_nombre}")

    # Detectar si es bbox o nombre de distrito
    if isinstance(bbox_o_distrito, str):
        # Es un nombre de distrito, usar ox.graph_from_place
        print(f"   🗺️  Descargando red vial del distrito: {bbox_o_distrito}")
        try:
            graph = ox.graph_from_place(bbox_o_distrito, network_type="drive")
        except Exception as e:
            print(f"   ❌ Error descargando distrito: {e}")
            graph = None
    else:
        # Es un bounding box
        print(f"   🗺️  Descargando red vial de bounding box...")
        graph = descargar_red_vial_bbox(bbox_o_distrito)

    if graph is None or len(graph.nodes) == 0:
        print(f"   ❌ No se pudo descargar red vial o no hay calles en esta zona")
        return {"descargadas": 0, "saltadas": IMAGENES_POR_URBANIZACION}

    n_nodos = len(graph.nodes)
    print(f"   ✅ Red descargada: {n_nodos:,} intersecciones")

    # Seleccionar exactamente IMAGENES_POR_URBANIZACION puntos aleatorios
    puntos = seleccionar_puntos_aleatorios(graph, IMAGENES_POR_URBANIZACION)
    print(f"   🎲 Seleccionados {len(puntos)} puntos aleatorios")

    # Guardar en el subdirectorio de categoría (no por ciudad)
    categoria_path = base_path / categoria
    stats_local = {"descargadas": 0, "saltadas": 0}

    # Descargar imágenes (máximo IMAGENES_POR_URBANIZACION)
    print(f"   📸 Descargando imágenes...")
    imagenes_descargadas_contador = 0

    for i, (lat, lon) in enumerate(puntos, 1):
        # Verificar que no hayamos excedido el límite
        if imagenes_descargadas_contador >= IMAGENES_POR_URBANIZACION:
            break

        print(f"      [{i}/{IMAGENES_POR_URBANIZACION}] ", end="", flush=True)

        # Verificar disponibilidad de Street View
        if not verificar_street_view(lat, lon, API_KEY):
            print("❌ No hay Street View")
            stats_local["saltadas"] += 1
            continue

        # Crear nombre de archivo usando el contador de imágenes descargadas
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = (
            categoria_path
            / f"{ciudad}_{categoria}_{urbanizacion_nombre}_{imagenes_descargadas_contador+1:02d}_{timestamp}.jpg"
        )

        # Descargar imagen
        if descargar_imagen(lat, lon, API_KEY, filename):
            imagenes_descargadas_contador += 1
            stats_local["descargadas"] += 1
            print(f"✅ {filename.name}")
        else:
            print("❌ Error al descargar")
            stats_local["saltadas"] += 1

    print(
        f"   ✅ {urbanizacion_nombre} completado: {stats_local['descargadas']} descargadas / {stats_local['saltadas']} saltadas\n"
    )
    return stats_local


def descargar_categoria_ciudad(ciudad, categoria, urbanizaciones, base_path, stats_lock):
    """
    Descarga todas las urbanizaciones de una categoría específica en una ciudad.
    Esta función se ejecuta en un thread separado.

    Args:
        ciudad: Nombre de la ciudad
        categoria: Categoría NSE (Alto, Medio, Bajo)
        urbanizaciones: Lista de tuplas (nombre, bbox)
        base_path: Path al directorio base
        stats_lock: Lock para acceso seguro a estadísticas

    Returns:
        dict: Estadísticas de descarga de esta categoría-ciudad
    """
    print(f"\n🔵 [{ciudad} - {categoria}] Thread iniciado")

    stats_categoria = {"descargadas": 0, "saltadas": 0}

    for urb_nombre, bbox_o_distrito in urbanizaciones:
        stats_local = descargar_urbanizacion(
            urb_nombre, bbox_o_distrito, ciudad, categoria, base_path, stats_lock
        )
        stats_categoria["descargadas"] += stats_local["descargadas"]
        stats_categoria["saltadas"] += stats_local["saltadas"]

    print(f"✅ [{ciudad} - {categoria}] Thread completado: {stats_categoria['descargadas']} descargadas")
    return (ciudad, categoria, stats_categoria)


def descargar_todas_urbanizaciones(base_path):
    """
    Descarga imágenes de todas las urbanizaciones de forma concurrente.
    Usa 9 threads: 1 por cada categoría de ciudad (3 ciudades × 3 categorías).

    Args:
        base_path: Path al directorio base

    Returns:
        dict: Estadísticas globales de descarga
    """
    print("\n" + "=" * 70)
    print("📸 DESCARGANDO IMÁGENES DE STREET VIEW (9 THREADS CONCURRENTES)")
    print("=" * 70)

    stats = {
        "descargadas": {},
        "saltadas": {},
        "total_descargadas": 0,
        "total_saltadas": 0,
    }

    # Inicializar estadísticas por ciudad y categoría
    for ciudad in URBANIZACIONES_POR_CIUDAD.keys():
        stats["descargadas"][ciudad] = {"Alto": 0, "Medio": 0, "Bajo": 0}
        stats["saltadas"][ciudad] = {"Alto": 0, "Medio": 0, "Bajo": 0}

    stats_lock = threading.Lock()

    # Contar total de urbanizaciones
    total_urbs = sum(
        len(urbs)
        for ciudad in URBANIZACIONES_POR_CIUDAD.values()
        for urbs in ciudad.values()
    )

    print(f"\n📊 Configuración de threads:")
    print(f"   • 1 thread por categoría-ciudad = 9 threads totales")
    print(f"   • Urbanizaciones totales: {total_urbs}")
    print(f"   • Imágenes esperadas: {total_urbs * IMAGENES_POR_URBANIZACION}\n")

    # Ejecutar descargas en paralelo (9 threads, uno por categoría-ciudad)
    with ThreadPoolExecutor(max_workers=9) as executor:
        futures = {}

        # Crear un thread por cada combinación ciudad-categoría
        for ciudad, categorias in URBANIZACIONES_POR_CIUDAD.items():
            for categoria, urbanizaciones in categorias.items():
                future = executor.submit(
                    descargar_categoria_ciudad,
                    ciudad,
                    categoria,
                    urbanizaciones,
                    base_path,
                    stats_lock,
                )
                futures[future] = (ciudad, categoria)

        # Recolectar resultados a medida que se completan
        for future in as_completed(futures):
            ciudad, categoria = futures[future]
            try:
                ciudad_result, categoria_result, stats_local = future.result()

                # Combinar estadísticas
                with stats_lock:
                    stats["descargadas"][ciudad][categoria] = stats_local["descargadas"]
                    stats["saltadas"][ciudad][categoria] = stats_local["saltadas"]
                    stats["total_descargadas"] += stats_local["descargadas"]
                    stats["total_saltadas"] += stats_local["saltadas"]

            except Exception as e:
                print(f"❌ Error en thread [{ciudad} - {categoria}]: {e}")

    return stats


def mostrar_resumen_final(stats):
    """Muestra el resumen final de la descarga."""
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70 + "\n")

    print("Por ciudad y categoría:")
    for ciudad in URBANIZACIONES_POR_CIUDAD.keys():
        print(f"\n  {ciudad}:")
        for categoria in ["Alto", "Medio", "Bajo"]:
            desc = stats["descargadas"][ciudad][categoria]
            salt = stats["saltadas"][ciudad][categoria]
            n_urbs = len(URBANIZACIONES_POR_CIUDAD[ciudad][categoria])
            total_esperado = n_urbs * IMAGENES_POR_URBANIZACION
            print(
                f"    {categoria:10s}: {desc:3d} descargadas / {salt:3d} saltadas / {total_esperado:3d} esperadas"
            )

    print(f"\n{'=' * 70}")
    print(f"  ✅ Total descargadas: {stats['total_descargadas']}")
    print(f"  ❌ Total saltadas: {stats['total_saltadas']}")
    print(f"  💰 Costo estimado: ${stats['total_descargadas'] * 0.007:.2f} USD")
    print(f"  📁 Ubicación: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 70 + "\n")


def main():
    print("\n" + "=" * 70)
    print("🌎 DESCARGADOR DE IMÁGENES - PROVINCIAS PERUANAS")
    print("=" * 70 + "\n")

    # Verificar API key
    if not API_KEY or API_KEY == "":
        print("❌ ERROR: Debes configurar tu STREET_VIEW_API_KEY en el archivo .env")
        print("\n📝 Crea un archivo .env con:")
        print('   STREET_VIEW_API_KEY="tu_api_key_aqui"')
        return

    print(f"📊 Configuración:")
    print(f"   • Ciudades: {len(URBANIZACIONES_POR_CIUDAD)}")
    total_urbs = sum(
        len(urbs)
        for ciudad in URBANIZACIONES_POR_CIUDAD.values()
        for urbs in ciudad.values()
    )
    print(f"   • Urbanizaciones totales: {total_urbs}")
    print(f"   • Imágenes por urbanización: {IMAGENES_POR_URBANIZACION}")
    print(f"   • Total imágenes esperadas: {total_urbs * IMAGENES_POR_URBANIZACION}\n")

    # Crear estructura de directorios
    base_path = crear_estructura_directorios()

    # Descargar imágenes
    stats = descargar_todas_urbanizaciones(base_path)

    # Mostrar resumen
    mostrar_resumen_final(stats)

    print("🎉 ¡Proceso completado!")
    print(f"   Revisa las imágenes en: {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
