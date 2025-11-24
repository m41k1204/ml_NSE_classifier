"""
Script para obtener bounding boxes de distritos desde OpenStreetMap/Nominatim
y proponer subdivisiones para urbanizaciones específicas.
"""

import requests
import time
import json

# Distritos seleccionados (uno por categoría y ciudad)
DISTRITOS_SELECCIONADOS = {
    "AREQUIPA": {
        "Alto": "Cayma, Arequipa, Peru",
        "Medio": "Jose Luis Bustamante y Rivero, Arequipa, Peru",
        "Bajo": "Cerro Colorado, Arequipa, Peru",
    },
    "TRUJILLO": {
        "Alto": "Victor Larco Herrera, Trujillo, Peru",
        "Medio": "La Esperanza, Trujillo, Peru",
        "Bajo": "El Porvenir, Trujillo, Peru",
    },
    "PIURA": {
        "Alto": "Castilla, Piura, Peru",
        "Medio": "Catacaos, Piura, Peru",
        "Bajo": "26 de Octubre, Piura, Peru",
    },
}


def get_bounding_box_from_nominatim(place_name):
    """
    Obtiene el bounding box de un lugar usando la API de Nominatim.

    Args:
        place_name: Nombre del lugar (ej: "Cayma, Arequipa, Peru")

    Returns:
        dict: Información del bounding box o None si falla
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place_name, "format": "json", "limit": 1, "addressdetails": 1}

    headers = {"User-Agent": "UrbanizacionesPeru/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            result = data[0]
            bbox = result.get("boundingbox", [])

            if len(bbox) == 4:
                # Nominatim devuelve: [min_lat, max_lat, min_lon, max_lon]
                return {
                    "place": place_name,
                    "lat_min": float(bbox[0]),
                    "lat_max": float(bbox[1]),
                    "lon_min": float(bbox[2]),
                    "lon_max": float(bbox[3]),
                    "center_lat": float(result.get("lat", 0)),
                    "center_lon": float(result.get("lon", 0)),
                    "display_name": result.get("display_name", ""),
                }
        return None

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def subdivide_bbox(bbox_info, n_divisions=2):
    """
    Subdivide un bounding box en N partes para crear urbanizaciones.

    Args:
        bbox_info: Dict con lat_min, lat_max, lon_min, lon_max
        n_divisions: Número de divisiones por lado (2 = 4 subdivisiones)

    Returns:
        list: Lista de subdivisiones con sus bounding boxes
    """
    lat_min = bbox_info["lat_min"]
    lat_max = bbox_info["lat_max"]
    lon_min = bbox_info["lon_min"]
    lon_max = bbox_info["lon_max"]

    lat_step = (lat_max - lat_min) / n_divisions
    lon_step = (lon_max - lon_min) / n_divisions

    subdivisiones = []

    for i in range(n_divisions):
        for j in range(n_divisions):
            sub_lat_min = lat_min + (i * lat_step)
            sub_lat_max = lat_min + ((i + 1) * lat_step)
            sub_lon_min = lon_min + (j * lon_step)
            sub_lon_max = lon_min + ((j + 1) * lon_step)

            subdivisiones.append(
                {
                    "zona": f"Zona_{i+1}{j+1}",
                    "lat_min": sub_lat_min,
                    "lat_max": sub_lat_max,
                    "lon_min": sub_lon_min,
                    "lon_max": sub_lon_max,
                }
            )

    return subdivisiones


def main():
    print("\n" + "=" * 80)
    print("🗺️  OBTENIENDO BOUNDING BOXES DE DISTRITOS")
    print("=" * 80 + "\n")

    resultados = {}

    for ciudad, categorias in DISTRITOS_SELECCIONADOS.items():
        print(f"\n{'=' * 80}")
        print(f"📍 {ciudad}")
        print(f"{'=' * 80}\n")

        resultados[ciudad] = {}

        for categoria, distrito in categorias.items():
            print(f"[{categoria:6s}] Consultando: {distrito:<50} ", end="", flush=True)

            bbox_info = get_bounding_box_from_nominatim(distrito)

            if bbox_info:
                print("✅")
                print(f"         Bbox: [{bbox_info['lat_min']:.6f}, {bbox_info['lat_max']:.6f}, "
                      f"{bbox_info['lon_min']:.6f}, {bbox_info['lon_max']:.6f}]")
                print(f"         Centro: ({bbox_info['center_lat']:.6f}, {bbox_info['center_lon']:.6f})")

                # Subdividir en 4 zonas (2x2)
                subdivisiones = subdivide_bbox(bbox_info, n_divisions=2)
                bbox_info["subdivisiones"] = subdivisiones

                resultados[ciudad][categoria] = bbox_info
            else:
                print("❌ No encontrado")
                resultados[ciudad][categoria] = None

            # Respetar rate limit de Nominatim (máx 1 req/seg)
            time.sleep(1.5)

    # Guardar resultados en JSON
    output_file = "bounding_boxes.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados guardados en: {output_file}")

    # Mostrar propuesta de urbanizaciones
    print("\n" + "=" * 80)
    print("💡 PROPUESTA DE URBANIZACIONES (2 POR DISTRITO)")
    print("=" * 80 + "\n")

    for ciudad, categorias in resultados.items():
        print(f"\n{ciudad}:")
        for categoria, bbox_info in categorias.items():
            if bbox_info and "subdivisiones" in bbox_info:
                print(f"\n  {categoria} - {bbox_info['place'].split(',')[0]}:")

                # Seleccionar 2 subdivisiones (esquinas opuestas para máxima variedad)
                subs = bbox_info["subdivisiones"]
                seleccionadas = [subs[0], subs[-1]]  # Primera y última zona

                for idx, sub in enumerate(seleccionadas, 1):
                    print(f"    Urbanización {idx} ({sub['zona']}):")
                    print(
                        f"      ({sub['lat_min']:.6f}, {sub['lat_max']:.6f}, "
                        f"{sub['lon_min']:.6f}, {sub['lon_max']:.6f})"
                    )

    print("\n" + "=" * 80)
    print("✅ Proceso completado!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
