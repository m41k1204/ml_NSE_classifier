import osmnx as ox

URBANIZACIONES_TEST = {
    "AREQUIPA - Alto": [
        "Cayma, Arequipa, Peru",
        "Yanahuara, Arequipa, Peru",
        "Urbanización Los Guindos, Cayma, Arequipa, Peru",
        "Urbanización Bello Horizonte, Cayma, Arequipa, Peru",
        "Urbanización La Señorial, Cayma, Arequipa, Peru",
        "Los Guindos, Arequipa, Peru",
        "Bello Horizonte, Arequipa, Peru",
    ],
    "AREQUIPA - Medio": [
        "Jose Luis Bustamante y Rivero, Arequipa, Peru",
        "Paucarpata, Arequipa, Peru",
        "Mariano Melgar, Arequipa, Peru",
        "Miraflores, Arequipa, Peru",
    ],
    "AREQUIPA - Bajo": [
        "Alto Selva Alegre, Arequipa, Peru",
        "Cerro Colorado, Arequipa, Peru",
        "Independencia, Alto Selva Alegre, Arequipa, Peru",
        "Pampas de Polanco, Alto Selva Alegre, Arequipa, Peru",
    ],
    "TRUJILLO - Alto": [
        "Victor Larco Herrera, Trujillo, Peru",
        "Victor Larco, Trujillo, Peru",
        "Trujillo, Trujillo, Peru",
        "Urbanización El Golf, Trujillo, Peru",
        "Urbanización California, Trujillo, Peru",
        "Buenos Aires, Victor Larco, Trujillo, Peru",
    ],
    "TRUJILLO - Medio": [
        "La Esperanza, Trujillo, Peru",
        "Moche, Trujillo, Peru",
        "Huanchaco, Trujillo, Peru",
    ],
    "TRUJILLO - Bajo": [
        "El Porvenir, Trujillo, Peru",
        "Florencia de Mora, Trujillo, Peru",
        "Alto Trujillo, Trujillo, Peru",
        "Miguel Grau, El Porvenir, Trujillo, Peru",
    ],
    "PIURA - Alto": [
        "Piura, Piura, Peru",
        "Castilla, Piura, Peru",
        "Miraflores, Castilla, Piura, Peru",
        "Urbanización Santa Rosa, Piura, Peru",
        "Urbanización Las Casuarinas, Piura, Peru",
    ],
    "PIURA - Medio": [
        "Catacaos, Piura, Peru",
        "Piura, Piura, Peru",
        "Castilla, Piura, Peru",
    ],
    "PIURA - Bajo": [
        "26 de Octubre, Piura, Peru",
        "Veintiséis de Octubre, Piura, Peru",
        "Castilla, Piura, Peru",
        "Asentamiento Humano San Martin, Piura, Peru",
    ],
}


def probar_lugar(lugar, timeout=30):
    try:
        graph = ox.graph_from_place(lugar, network_type="drive")
        n_nodos = len(graph.nodes)
        return (True, n_nodos, f"✅ {n_nodos:,} intersecciones")
    except Exception as e:
        error_msg = str(e)
        if "Could not geocode" in error_msg or "Found no graph nodes" in error_msg:
            return (False, 0, "❌ No encontrado en OSM")
        else:
            return (False, 0, f"❌ Error: {error_msg[:50]}...")


def main():
    print("\n" + "=" * 80)
    print("🔍 PROBANDO URBANIZACIONES EN OPENSTREETMAP")
    print("=" * 80 + "\n")

    resultados = {}

    for categoria, lugares in URBANIZACIONES_TEST.items():
        print(f"\n{'=' * 80}")
        print(f"📍 {categoria}")
        print(f"{'=' * 80}\n")

        resultados[categoria] = []

        for lugar in lugares:
            print(f"Probando: {lugar:<60} ", end="", flush=True)
            existe, n_nodos, mensaje = probar_lugar(lugar)

            print(mensaje)

            if existe:
                resultados[categoria].append((lugar, n_nodos))

    print("\n" + "=" * 80)
    print("📊 RESUMEN - LUGARES QUE FUNCIONAN")
    print("=" * 80 + "\n")

    for categoria, lugares_ok in resultados.items():
        print(f"\n{categoria}:")
        if lugares_ok:
            for lugar, n_nodos in lugares_ok:
                print(f"   ✅ {lugar} ({n_nodos:,} nodos)")
        else:
            print("   ⚠️  Ningún lugar encontrado")

    print("\n" + "=" * 80)
    print("💡 RECOMENDACIONES PARA EL SCRIPT FINAL")
    print("=" * 80 + "\n")

    for categoria, lugares_ok in resultados.items():
        if lugares_ok and len(lugares_ok) >= 2:
            print(f"\n{categoria}:")
            for i, (lugar, n_nodos) in enumerate(lugares_ok[:2], 1):
                print(f"   {i}. {lugar}")


if __name__ == "__main__":
    main()
