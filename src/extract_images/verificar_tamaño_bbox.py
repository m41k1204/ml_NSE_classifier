import math

URBANIZACIONES = {
    "Arequipa - Alto - Cayma Norte": (-16.393344, -16.278875, -71.556694, -71.447529),
    "Arequipa - Alto - Cayma Sur": (-16.278875, -16.164406, -71.447529, -71.338364),
    "Arequipa - Medio - Bustamante Oeste": (-16.455307, -16.433064, -71.547559, -71.524350),
    "Arequipa - Medio - Bustamante Este": (-16.433064, -16.410821, -71.524350, -71.501140),
    "Arequipa - Bajo - Cerro Colorado Oeste": (-16.407568, -16.298328, -71.651989, -71.575671),
    "Arequipa - Bajo - Cerro Colorado Sur": (-16.298328, -16.189088, -71.575671, -71.499353),

    "Trujillo - Alto - El Golf Norte": (-8.162293, -8.140474, -79.070289, -79.048536),
    "Trujillo - Alto - California Sur": (-8.140474, -8.118654, -79.048536, -79.026782),
    "Trujillo - Medio - La Esperanza Norte": (-8.087606, -8.063584, -79.086145, -79.058108),
    "Trujillo - Medio - La Esperanza Sur": (-8.063584, -8.039563, -79.058108, -79.030072),
    "Trujillo - Bajo - El Porvenir Oeste": (-8.089783, -8.051983, -79.036240, -78.994735),
    "Trujillo - Bajo - Alto Trujillo Este": (-8.051983, -8.014184, -78.994735, -78.953231),

    "Piura - Alto - Miraflores Country Club": (-5.265031, -5.115276, -80.649162, -80.493615),
    "Piura - Alto - Castilla Norte": (-5.115276, -4.965522, -80.493615, -80.338068),
    "Piura - Medio - Catacaos Centro Oeste": (-5.811244, -5.481369, -80.800992, -80.384766),
    "Piura - Medio - Catacaos Norte": (-5.481369, -5.151495, -80.384766, -79.968539),
    "Piura - Bajo - San Martin Oeste": (-5.218936, -5.168272, -80.767768, -80.703437),
    "Piura - Bajo - 26 de Octubre Este": (-5.168272, -5.117608, -80.703437, -80.639106),
}


def calcular_area_km2(bbox):
    lat_min, lat_max, lon_min, lon_max = bbox

    lat_center = (lat_min + lat_max) / 2

    height_km = abs(lat_max - lat_min) * 111
    width_km = abs(lon_max - lon_min) * 111 * math.cos(math.radians(lat_center))

    area_km2 = height_km * width_km

    return area_km2


def main():
    print("\n" + "=" * 80)
    print("📏 VERIFICACIÓN DE TAMAÑO DE BOUNDING BOXES")
    print("=" * 80 + "\n")

    resultados = []

    for nombre, bbox in URBANIZACIONES.items():
        area = calcular_area_km2(bbox)
        resultados.append((nombre, area, bbox))

    resultados.sort(key=lambda x: x[1], reverse=True)

    print(f"{'Urbanización':<50} {'Área (km²)':<15}")
    print("=" * 80)

    for nombre, area, bbox in resultados:
        nivel = "🔴 MUY GRANDE" if area > 200 else "🟡 GRANDE" if area > 50 else "🟢 OK"
        print(f"{nombre:<50} {area:>10.2f} km²    {nivel}")

    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)

    muy_grandes = sum(1 for _, area, _ in resultados if area > 200)
    grandes = sum(1 for _, area, _ in resultados if 50 < area <= 200)
    ok = sum(1 for _, area, _ in resultados if area <= 50)

    print(f"🔴 MUY GRANDES (>200 km²): {muy_grandes}")
    print(f"🟡 GRANDES (50-200 km²): {grandes}")
    print(f"🟢 OK (<50 km²): {ok}")

    print("\n💡 RECOMENDACIÓN:")
    print("   Los bounding boxes MUY GRANDES tardarán mucho en descargar.")
    print("   Se recomienda subdividirlos en áreas más pequeñas (<50 km²).")


if __name__ == "__main__":
    main()
