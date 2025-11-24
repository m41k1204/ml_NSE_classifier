import osmnx as ox

TESTS = [
    ("Cayma Norte", (-16.393344, -16.278875, -71.556694, -71.447529)),
    ("Bustamante Oeste", (-16.455307, -16.433064, -71.547559, -71.524350)),
    ("El Golf Norte", (-8.162293, -8.140474, -79.070289, -79.048536)),
    ("Castilla Piura Sur", (-5.265031, -5.115276, -80.649162, -80.493615)),
]


def test_bbox_download(nombre, bbox):
    lat_min, lat_max, lon_min, lon_max = bbox

    print(f"\n{'='*70}")
    print(f"Probando: {nombre}")
    print(f"Bbox: lat=[{lat_min:.6f}, {lat_max:.6f}], lon=[{lon_min:.6f}, {lon_max:.6f}]")

    try:
        if lat_min >= lat_max:
            print(f"❌ ERROR: lat_min ({lat_min}) >= lat_max ({lat_max})")
            return None

        if lon_min >= lon_max:
            print(f"❌ ERROR: lon_min ({lon_min}) >= lon_max ({lon_max})")
            return None

        print(f"Descargando con ox.graph_from_bbox...")
        print(f"   bbox=(north={lat_max}, south={lat_min}, east={lon_max}, west={lon_min})")

        graph = ox.graph_from_bbox(
            bbox=(lat_max, lat_min, lon_max, lon_min), network_type="drive"
        )

        n_nodes = len(graph.nodes)
        n_edges = len(graph.edges)

        print(f"✅ ÉXITO!")
        print(f"   • Nodos: {n_nodes:,}")
        print(f"   • Calles: {n_edges:,}")

        return graph

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None


def main():
    print("\n" + "=" * 70)
    print("🔍 PROBANDO DESCARGA DE BOUNDING BOXES")
    print("=" * 70)

    resultados = []

    for nombre, bbox in TESTS:
        graph = test_bbox_download(nombre, bbox)
        resultados.append((nombre, bbox, graph is not None))

    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)

    for nombre, bbox, exito in resultados:
        estado = "✅ OK" if exito else "❌ FALLO"
        print(f"{estado} - {nombre}")

    exitosos = sum(1 for _, _, e in resultados if e)
    print(f"\nTotal exitosos: {exitosos}/{len(resultados)}")


if __name__ == "__main__":
    main()
