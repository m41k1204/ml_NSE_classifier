"""
Configuración de distritos de Lima con sus niveles socioeconómicos.
Subdivisiones basadas en análisis visual de mapas oficiales de NSE de la Municipalidad de Lima.
Formato: (lat_min, lat_max, lon_min, lon_max)
"""

DISTRITOS_NSE = {
    # ==================== DISTRITOS HOMOGÉNEOS ====================
    # NSE ALTO
    "Santa Maria del Mar, Lima, Peru": [
        ((-12.420, -12.400, -76.810, -76.770), "Alto"),
    ],
    "San Isidro, Lima, Peru": [
        ((-12.110, -12.090, -77.050, -77.030), "Alto"),
    ],
    "San Borja, Lima, Peru": [
        ((-12.110, -12.090, -77.010, -76.985), "Alto"),
    ],
    "Miraflores, Lima, Peru": [
        ((-12.135, -12.110, -77.045, -77.015), "Alto"),
    ],
    "Magdalena del Mar, Lima, Peru": [
        ((-12.100, -12.080, -77.080, -77.055), "Alto"),
    ],
    "La Molina, Lima, Peru": [
        ((-12.120, -12.070, -76.960, -76.920), "Alto"),
    ],
    "Jesus Maria, Lima, Peru": [
        ((-12.080, -12.065, -77.055, -77.035), "Alto"),
    ],
    # NSE MEDIO ALTO
    "Breña, Lima, Peru": [
        ((-12.070, -12.055, -77.065, -77.045), "Medio alto"),
    ],
    # NSE MEDIO
    "San Luis, Lima, Peru": [
        ((-12.085, -12.070, -77.000, -76.985), "Medio"),
    ],
    # ==================== DISTRITOS HETEROGÉNEOS ====================
    # LINCE - Basado en mapa: Predominantemente Medio alto con Alto al suroeste y algo de Medio
    "Lince, Lima, Peru": [
        # Zona suroeste - Alto
        ((-12.085, -12.078, -77.045, -77.038), "Alto"),
        # Zona oeste y centro - Medio alto (predominante)
        ((-12.085, -12.070, -77.038, -77.025), "Medio alto"),
        ((-12.078, -12.070, -77.045, -77.038), "Medio alto"),
        # Zona este - Medio alto con algo de Medio
        ((-12.078, -12.070, -77.032, -77.025), "Medio"),
    ],
    # PUEBLO LIBRE - Basado en mapa: Alto al oeste/centro-norte, Medio alto al este, poco Medio
    "Pueblo Libre, Lima, Peru": [
        # Zona oeste y norte - Alto
        ((-12.080, -12.070, -77.080, -77.070), "Alto"),
        ((-12.075, -12.070, -77.070, -77.060), "Alto"),
        # Zona centro - Alto y Medio alto
        ((-12.085, -12.075, -77.080, -77.070), "Alto"),
        ((-12.085, -12.075, -77.070, -77.060), "Medio alto"),
        # Zona este - Medio alto
        ((-12.080, -12.070, -77.070, -77.060), "Medio alto"),
        # Zona sur - Medio
        ((-12.090, -12.085, -77.075, -77.065), "Medio"),
    ],
    # SAN MIGUEL - Basado en mapa: MUY heterogéneo, Alto al oeste, Medio al este
    "San Miguel, Lima, Peru": [
        # Zona oeste y noroeste - Alto (predominante)
        ((-12.080, -12.070, -77.100, -77.085), "Alto"),
        ((-12.090, -12.080, -77.100, -77.090), "Alto"),
        ((-12.085, -12.075, -77.095, -77.085), "Alto"),
        # Zona centro-este - Medio alto y Medio
        ((-12.080, -12.070, -77.085, -77.075), "Medio alto"),
        # Zona este y sureste - Medio
        ((-12.090, -12.080, -77.090, -77.075), "Medio"),
        ((-12.095, -12.085, -77.095, -77.080), "Medio"),
    ],
    # SURQUILLO - Basado en mapa: MUY heterogéneo, Alto al norte, Medio alto/Medio al centro y sur
    "Surquillo, Lima, Peru": [
        # Zona norte y noroeste - Alto
        ((-12.110, -12.105, -77.020, -77.010), "Alto"),
        ((-12.115, -12.110, -77.020, -77.015), "Alto"),
        # Zona oeste - Medio alto
        ((-12.115, -12.110, -77.015, -77.010), "Medio alto"),
        # Zona centro - Medio
        ((-12.115, -12.110, -77.010, -77.005), "Medio"),
        ((-12.120, -12.115, -77.020, -77.010), "Medio"),
        # Zona sureste - Medio
        ((-12.120, -12.115, -77.010, -77.005), "Medio"),
    ],
    # ==================== OTROS DISTRITOS HETEROGÉNEOS ====================
    # LIMA (Cercado) - Basado en mapa: Oeste tiene Alto pequeño y Medio alto, Centro Medio, Norte/Este Medio bajo y Bajo
    "Lima, Lima, Peru": [
        # Zona oeste - Alto (pequeña)
        ((-12.050, -12.045, -77.050, -77.045), "Alto"),
        # Zona oeste - Medio alto (amplia)
        ((-12.060, -12.045, -77.045, -77.035), "Medio alto"),
        # Zona centro - Medio
        ((-12.055, -12.045, -77.035, -77.025), "Medio"),
        ((-12.065, -12.055, -77.040, -77.030), "Medio"),
        # Zona norte - Medio bajo
        ((-12.045, -12.040, -77.040, -77.030), "Medio bajo"),
        # Zona noreste/este - Bajo y Medio bajo (Barrios Altos)
        ((-12.050, -12.045, -77.030, -77.020), "Bajo"),
        ((-12.060, -12.050, -77.030, -77.020), "Medio bajo"),
    ],
    # BARRANCO - Basado en mapa: Norte Alto, resto Medio alto
    "Barranco, Lima, Peru": [
        # Norte - Alto
        ((-12.145, -12.140, -77.025, -77.015), "Alto"),
        # Centro y sur - Medio alto
        ((-12.150, -12.145, -77.025, -77.015), "Medio alto"),
        ((-12.156, -12.150, -77.030, -77.015), "Medio alto"),
    ],
    # CHORRILLOS - Basado en mapa: MUY heterogéneo, norte Alto cerca al mar, gradiente hacia Bajo al sur
    "Chorrillos, Lima, Peru": [
        # Norte cerca al mar - Alto y Medio alto
        ((-12.165, -12.160, -77.030, -77.015), "Alto"),
        ((-12.170, -12.165, -77.030, -77.015), "Medio alto"),
        # Centro-norte - Medio
        ((-12.178, -12.170, -77.030, -77.015), "Medio"),
        # Centro - Medio y Medio bajo
        ((-12.170, -12.165, -77.045, -77.030), "Medio"),
        ((-12.178, -12.170, -77.045, -77.030), "Medio bajo"),
        ((-12.188, -12.178, -77.035, -77.020), "Medio"),
        # Sur y sureste - Medio bajo y Bajo
        ((-12.195, -12.188, -77.040, -77.025), "Medio bajo"),
        ((-12.205, -12.195, -77.040, -77.025), "Bajo"),
        ((-12.210, -12.205, -77.045, -77.035), "Medio bajo"),
    ],
    # COMAS - Basado en mapa: Oeste Bajo/Medio bajo, Centro Medio, disperso
    "Comas, Lima, Peru": [
        # Zona oeste - Bajo y Medio bajo
        ((-11.930, -11.920, -77.070, -77.055), "Bajo"),
        ((-11.945, -11.930, -77.070, -77.055), "Medio bajo"),
        ((-11.960, -11.945, -77.070, -77.055), "Bajo"),
        # Zona centro - Medio con bolsones de Medio bajo
        ((-11.930, -11.920, -77.055, -77.040), "Medio"),
        ((-11.945, -11.930, -77.055, -77.040), "Medio bajo"),
        ((-11.960, -11.945, -77.055, -77.040), "Medio"),
        # Zona este y sur - Medio bajo y Medio
        ((-11.975, -11.960, -77.070, -77.055), "Medio bajo"),
        ((-11.990, -11.975, -77.070, -77.055), "Medio"),
        ((-12.005, -11.990, -77.070, -77.055), "Medio"),
        ((-12.020, -12.005, -77.070, -77.055), "Medio"),
    ],
    # EL AGUSTINO - Basado en mapa: Oeste Medio, Centro Medio bajo, Este/Norte Bajo
    "El Agustino, Lima, Peru": [
        # Zona oeste - Medio
        ((-12.045, -12.035, -77.000, -76.990), "Medio"),
        # Zona centro-oeste - Medio
        ((-12.055, -12.045, -77.000, -76.990), "Medio"),
        # Zona centro - Medio bajo y Medio
        ((-12.045, -12.035, -76.990, -76.980), "Medio bajo"),
        ((-12.055, -12.045, -76.990, -76.980), "Medio"),
        # Zona este - Medio bajo y Bajo
        ((-12.045, -12.035, -76.980, -76.970), "Medio bajo"),
        ((-12.055, -12.045, -76.980, -76.970), "Bajo"),
        # Zona norte - Bajo
        ((-12.035, -12.025, -76.995, -76.980), "Bajo"),
    ],
    # INDEPENDENCIA - Basado en mapa: Centro Medio, periferia Medio bajo y Bajo
    "Independencia, Lima, Peru": [
        # Centro - Medio
        ((-11.985, -11.975, -77.070, -77.055), "Medio"),
        ((-11.995, -11.985, -77.065, -77.050), "Medio"),
        # Periferia norte - Bajo
        ((-11.975, -11.965, -77.070, -77.055), "Bajo"),
        # Periferia oeste - Medio bajo
        ((-11.985, -11.975, -77.080, -77.070), "Medio bajo"),
        # Periferia este - Bajo y Medio bajo
        ((-11.985, -11.975, -77.055, -77.040), "Medio bajo"),
        ((-12.000, -11.985, -77.070, -77.055), "Bajo"),
        # Sur - Medio bajo
        ((-12.010, -12.000, -77.070, -77.055), "Medio bajo"),
    ],
    # LA VICTORIA - Basado en mapa: Predominantemente Medio alto y Medio
    "La Victoria, Lima, Peru": [
        # Norte y oeste - Medio alto
        ((-12.070, -12.060, -77.040, -77.025), "Medio alto"),
        # Centro - Medio
        ((-12.075, -12.070, -77.035, -77.020), "Medio"),
        ((-12.080, -12.075, -77.035, -77.025), "Medio"),
        # Este - Medio
        ((-12.075, -12.065, -77.025, -77.015), "Medio"),
        # Sur - Medio con algo de Medio bajo
        ((-12.085, -12.075, -77.030, -77.020), "Medio"),
    ],
    # LOS OLIVOS - Basado en mapa: Centro-este Medio alto, oeste/bordes Medio/Medio bajo
    "Los Olivos, Lima, Peru": [
        # Zona norte-oeste - Medio bajo
        ((-11.970, -11.960, -77.090, -77.070), "Medio bajo"),
        # Zona norte-centro - Medio
        ((-11.970, -11.960, -77.070, -77.050), "Medio"),
        # Zona centro-oeste - Medio
        ((-11.990, -11.970, -77.090, -77.070), "Medio"),
        # Zona centro-este - Medio alto (mejor zona según mapa)
        ((-11.990, -11.970, -77.070, -77.050), "Medio alto"),
        # Zona sur-oeste - Medio bajo
        ((-12.005, -11.990, -77.090, -77.070), "Medio bajo"),
        # Zona sur-centro - Medio
        ((-12.005, -11.990, -77.070, -77.050), "Medio"),
        ((-12.020, -12.005, -77.080, -77.060), "Medio"),
    ],
    # LURIGANCHO (Chosica) - Basado en mapa: Centro Medio, mucho Medio bajo y Bajo disperso
    "Lurigancho, Lima, Peru": [
        # Zona oeste - Medio
        ((-11.940, -11.930, -76.900, -76.880), "Medio"),
        # Zona centro - Medio y Medio bajo
        ((-11.950, -11.940, -76.890, -76.870), "Medio"),
        ((-11.960, -11.950, -76.890, -76.870), "Medio bajo"),
        # Zona este - Bajo y Medio bajo
        ((-11.950, -11.940, -76.870, -76.850), "Medio bajo"),
        ((-11.960, -11.950, -76.870, -76.850), "Bajo"),
    ],
    # LURÍN - Basado en mapa: Medio en algunas zonas, predominante Medio bajo y Bajo
    "Lurín, Lima, Peru": [
        # Norte - Medio bajo
        ((-12.270, -12.260, -76.880, -76.860), "Medio bajo"),
        # Centro - Medio
        ((-12.280, -12.270, -76.875, -76.855), "Medio"),
        # Sur y disperso - Bajo y Medio bajo
        ((-12.295, -12.280, -76.880, -76.860), "Bajo"),
        ((-12.310, -12.295, -76.880, -76.860), "Medio bajo"),
    ],
    # PACHACAMAC - Basado en mapa: Muy disperso, Medio bajo y Bajo predominante
    "Pachacamac, Lima, Peru": [
        # Zona norte (poblado principal) - Medio bajo y Medio
        ((-12.250, -12.240, -76.870, -76.850), "Medio bajo"),
        ((-12.240, -12.230, -76.865, -76.845), "Medio"),
        # Zonas dispersas - Bajo y Medio bajo
        ((-12.270, -12.250, -76.880, -76.860), "Bajo"),
        ((-12.290, -12.270, -76.890, -76.870), "Medio bajo"),
        ((-12.310, -12.290, -76.900, -76.880), "Bajo"),
    ],
    # PUCUSANA - Basado en mapa: Distrito pequeño, Medio, Medio bajo y Bajo
    "Pucusana, Lima, Peru": [
        # Norte - Medio bajo
        ((-12.470, -12.465, -76.800, -76.790), "Medio bajo"),
        # Centro - Medio
        ((-12.475, -12.470, -76.800, -76.790), "Medio"),
        # Sur - Bajo y Medio bajo
        ((-12.485, -12.475, -76.800, -76.790), "Bajo"),
        ((-12.490, -12.485, -76.802, -76.792), "Medio bajo"),
    ],
    # PUENTE PIEDRA - Basado en mapa: Bajo y Medio bajo predominante, algo de Medio al sur
    "Puente Piedra, Lima, Peru": [
        # Zona norte - Bajo
        ((-11.855, -11.840, -77.090, -77.070), "Bajo"),
        ((-11.870, -11.855, -77.090, -77.070), "Medio bajo"),
        # Zona centro - Bajo predominante
        ((-11.885, -11.870, -77.090, -77.070), "Bajo"),
        ((-11.900, -11.885, -77.090, -77.070), "Bajo"),
        # Zona sur - Medio bajo y Medio
        ((-11.915, -11.900, -77.090, -77.070), "Medio bajo"),
        ((-11.930, -11.915, -77.085, -77.065), "Medio"),
    ],
    # PUNTA HERMOSA - Basado en mapa: Pequeño, diferentes NSE
    "Punta Hermosa, Lima, Peru": [
        # Norte - Medio bajo y Bajo
        ((-12.330, -12.325, -76.825, -76.815), "Medio bajo"),
        ((-12.335, -12.330, -76.825, -76.815), "Bajo"),
        # Centro/Sur - Alto y Medio
        ((-12.340, -12.335, -76.825, -76.815), "Alto"),
        ((-12.345, -12.340, -76.825, -76.815), "Medio"),
    ],
    # PUNTA NEGRA - Basado en mapa: Medio alto, Medio, Medio bajo
    "Punta Negra, Lima, Peru": [
        # Norte - Medio alto
        ((-12.355, -12.350, -76.800, -76.790), "Medio alto"),
        # Centro - Medio
        ((-12.362, -12.355, -76.800, -76.790), "Medio"),
        # Sur - Medio bajo
        ((-12.370, -12.362, -76.802, -76.792), "Medio bajo"),
    ],
    # RÍMAC - Basado en mapa: Norte Bajo, Centro Medio/Medio bajo, algunos Medio alto
    "Rímac, Lima, Peru": [
        # Norte - Bajo predominante
        ((-12.025, -12.015, -77.055, -77.040), "Bajo"),
        ((-12.035, -12.025, -77.050, -77.035), "Bajo"),
        # Centro - Medio y Medio bajo
        ((-12.045, -12.035, -77.050, -77.035), "Medio"),
        ((-12.050, -12.045, -77.045, -77.030), "Medio bajo"),
        # Algunos bolsones Medio alto
        ((-12.040, -12.035, -77.045, -77.035), "Medio alto"),
        # Sur - Medio
        ((-12.055, -12.050, -77.045, -77.035), "Medio"),
    ],
    # SAN BARTOLO - Basado en mapa: Sur Alto, norte Medio/Medio bajo
    "San Bartolo, Lima, Peru": [
        # Norte y oeste - Medio bajo
        ((-12.390, -12.385, -76.785, -76.775), "Medio bajo"),
        # Centro - Medio
        ((-12.395, -12.390, -76.785, -76.775), "Medio"),
        # Sur - Alto
        ((-12.400, -12.395, -76.785, -76.775), "Alto"),
    ],
    # SAN JUAN DE LURIGANCHO - Basado en mapa: MUY heterogéneo, Oeste Medio, Centro Medio/Bajo, Este Bajo
    "San Juan de Lurigancho, Lima, Peru": [
        # Zona oeste (cerca a Lima Centro) - Medio
        ((-11.995, -11.985, -77.015, -77.000), "Medio"),
        ((-12.005, -11.995, -77.015, -77.000), "Medio"),
        # Zona centro-oeste - Medio bajo predominante
        ((-12.015, -12.005, -77.015, -77.000), "Medio bajo"),
        ((-12.025, -12.015, -77.010, -76.995), "Medio bajo"),
        # Zona centro - Medio y Bajo
        ((-11.995, -11.985, -77.000, -76.980), "Medio"),
        ((-12.005, -11.995, -77.000, -76.980), "Medio bajo"),
        ((-12.015, -12.005, -77.000, -76.980), "Bajo"),
        ((-12.025, -12.015, -77.000, -76.980), "Bajo"),
        # Zona este (más alejada) - Predominantemente Bajo
        ((-11.995, -11.985, -76.980, -76.960), "Bajo"),
        ((-12.005, -11.995, -76.980, -76.960), "Bajo"),
        ((-12.015, -12.005, -76.980, -76.960), "Bajo"),
        ((-12.025, -12.015, -76.980, -76.960), "Bajo"),
    ],
    # SAN JUAN DE MIRAFLORES - Basado en mapa: Norte Medio, Centro Medio bajo, Sur Bajo
    "San Juan de Miraflores, Lima, Peru": [
        # Zona norte - Medio
        ((-12.160, -12.150, -76.980, -76.960), "Medio"),
        ((-12.175, -12.160, -76.980, -76.960), "Medio"),
        # Zona centro - Medio bajo
        ((-12.190, -12.175, -76.980, -76.960), "Medio bajo"),
        # Zona sur - Bajo y Medio bajo
        ((-12.200, -12.190, -76.980, -76.960), "Bajo"),
        ((-12.215, -12.200, -76.985, -76.965), "Medio bajo"),
    ],
    # SAN MARTÍN DE PORRES - Basado en mapa: Oeste Medio/Medio alto, Centro Medio, Este Medio bajo
    "San Martin de Porres, Lima, Peru": [
        # Zona oeste (cerca a costa) - Medio alto
        ((-12.010, -12.000, -77.100, -77.080), "Medio alto"),
        ((-12.020, -12.010, -77.095, -77.075), "Medio"),
        # Zona centro-oeste - Medio
        ((-12.010, -12.000, -77.080, -77.060), "Medio"),
        ((-12.020, -12.010, -77.075, -77.055), "Medio"),
        # Zona centro-este - Medio y Medio bajo
        ((-12.030, -12.020, -77.090, -77.070), "Medio bajo"),
        ((-12.040, -12.030, -77.085, -77.065), "Medio bajo"),
        # Zona este - Medio
        ((-12.030, -12.020, -77.070, -77.050), "Medio"),
        ((-12.040, -12.030, -77.065, -77.045), "Medio"),
    ],
    # SANTA ANITA - Basado en mapa: Medio alto, Medio, algo de Medio bajo
    "Santa Anita, Lima, Peru": [
        # Norte - Medio alto
        ((-12.040, -12.030, -76.980, -76.965), "Medio alto"),
        # Centro - Medio
        ((-12.050, -12.040, -76.980, -76.965), "Medio"),
        ((-12.060, -12.050, -76.980, -76.965), "Medio"),
        # Sur - Medio y Medio bajo
        ((-12.070, -12.060, -76.980, -76.965), "Medio"),
        ((-12.075, -12.070, -76.982, -76.967), "Medio bajo"),
    ],
    # SANTA ROSA - Basado en mapa: Heterogéneo con Medio, Medio bajo, Bajo
    "Santa Rosa, Lima, Peru": [
        # Norte - Medio bajo
        ((-11.795, -11.785, -77.210, -77.190), "Medio bajo"),
        # Centro - Medio
        ((-11.805, -11.795, -77.210, -77.190), "Medio"),
        # Sur y disperso - Bajo y Medio bajo
        ((-11.815, -11.805, -77.210, -77.190), "Bajo"),
        ((-11.825, -11.815, -77.212, -77.192), "Medio bajo"),
    ],
    # SANTIAGO DE SURCO - Basado en mapa: MUY heterogéneo, Oeste/Norte Alto, Centro Medio alto/Medio, Este Medio/Medio bajo
    "Santiago de Surco, Lima, Peru": [
        # Zona oeste (cerca a Miraflores/San Borja) - Predominantemente Alto
        ((-12.120, -12.110, -77.020, -77.000), "Alto"),
        ((-12.130, -12.120, -77.020, -77.000), "Alto"),
        # Zona centro-oeste - Medio alto
        ((-12.140, -12.130, -77.020, -77.000), "Medio alto"),
        ((-12.150, -12.140, -77.018, -76.998), "Medio alto"),
        # Zona centro - Medio alto y Medio
        ((-12.120, -12.110, -77.000, -76.980), "Medio alto"),
        ((-12.130, -12.120, -77.000, -76.980), "Medio"),
        ((-12.140, -12.130, -77.000, -76.980), "Medio"),
        # Zona este - Medio y Medio bajo
        ((-12.120, -12.110, -76.980, -76.960), "Medio"),
        ((-12.135, -12.120, -76.980, -76.960), "Medio"),
        ((-12.150, -12.135, -76.980, -76.960), "Medio bajo"),
    ],
    # VILLA EL SALVADOR - Basado en mapa: Predominantemente Bajo y Medio bajo
    "Villa El Salvador, Lima, Peru": [
        # Zona norte - Medio bajo
        ((-12.215, -12.200, -76.950, -76.930), "Medio bajo"),
        ((-12.215, -12.200, -76.970, -76.950), "Medio bajo"),
        # Zona centro-norte - Bajo y Medio bajo
        ((-12.230, -12.215, -76.950, -76.930), "Bajo"),
        ((-12.230, -12.215, -76.970, -76.950), "Medio bajo"),
        # Zona centro-sur - Predominantemente Bajo
        ((-12.245, -12.230, -76.950, -76.930), "Bajo"),
        ((-12.245, -12.230, -76.970, -76.950), "Medio bajo"),
        # Zona sur - Bajo
        ((-12.260, -12.245, -76.955, -76.935), "Bajo"),
    ],
    # VILLA MARÍA DEL TRIUNFO - Basado en mapa: Predominantemente Bajo y Medio bajo
    "Villa Maria del Triunfo, Lima, Peru": [
        # Zona norte - Medio bajo
        ((-12.170, -12.160, -76.960, -76.940), "Medio bajo"),
        ((-12.180, -12.170, -76.965, -76.945), "Medio bajo"),
        # Zona centro - Bajo predominante
        ((-12.195, -12.180, -76.960, -76.940), "Bajo"),
        ((-12.210, -12.195, -76.960, -76.940), "Bajo"),
        # Zona sur - Bajo
        ((-12.225, -12.210, -76.960, -76.940), "Bajo"),
    ],
    # CARABAYLLO - Basado en mapa: Heterogéneo Bajo, Medio bajo, Medio
    "Carabayllo, Lima, Peru": [
        # Zona norte - Bajo
        ((-11.855, -11.840, -77.050, -77.030), "Bajo"),
        # Zona centro-norte - Medio bajo y Bajo
        ((-11.870, -11.855, -77.050, -77.030), "Medio bajo"),
        ((-11.885, -11.870, -77.050, -77.030), "Bajo"),
        # Zona centro - Medio bajo
        ((-11.900, -11.885, -77.050, -77.030), "Medio bajo"),
        # Zona sur (más cerca a Lima) - Medio
        ((-11.915, -11.900, -77.050, -77.030), "Medio"),
        ((-11.930, -11.915, -77.055, -77.035), "Medio"),
    ],
    # ATE - Basado en mapa: Oeste Medio alto cerca a La Molina, gradiente hacia Bajo al este
    "Ate, Lima, Peru": [
        # Zona oeste (cerca a La Molina) - Medio alto
        ((-12.055, -12.040, -76.990, -76.970), "Medio alto"),
        ((-12.070, -12.055, -76.990, -76.970), "Medio"),
        # Zona centro-oeste - Medio y Medio bajo
        ((-12.055, -12.040, -76.970, -76.950), "Medio"),
        ((-12.070, -12.055, -76.970, -76.950), "Medio bajo"),
        # Zona centro-este - Medio bajo y Bajo
        ((-12.085, -12.070, -76.985, -76.965), "Medio bajo"),
        ((-12.100, -12.085, -76.985, -76.965), "Bajo"),
        # Zona este - Predominantemente Bajo
        ((-12.085, -12.070, -76.965, -76.945), "Bajo"),
        ((-12.100, -12.085, -76.965, -76.945), "Bajo"),
    ],
}


def obtener_nse_por_coordenada(lat, lon):
    """
    Dadas coordenadas, busca en todos los distritos y retorna el NSE y distrito.

    Args:
        lat: Latitud
        lon: Longitud

    Returns:
        tuple: (distrito, nse) o (None, None) si no se encuentra
    """
    # Buscar en todos los distritos
    for distrito, zonas in DISTRITOS_NSE.items():
        for bbox, nse in zonas:
            lat_min, lat_max, lon_min, lon_max = bbox
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                return (distrito, nse)

    # No se encontró en ningún distrito
    return (None, None)


def obtener_todos_distritos():
    """Retorna lista de todos los distritos configurados."""
    return list(DISTRITOS_NSE.keys())


def obtener_distribucion_nse(distrito):
    """
    Retorna la distribución de NSE en un distrito.

    Returns:
        dict: {"Alto": peso, "Medio alto": peso, ...}
    """
    if distrito in DISTRITOS_NSE:
        zonas = DISTRITOS_NSE[distrito]
        distribucion = {}
        for _, nse in zonas:
            distribucion[nse] = distribucion.get(nse, 0) + 1

        # Normalizar
        total = sum(distribucion.values())
        return {k: v / total for k, v in distribucion.items()}

    return {}


# Límites de Lima Metropolitana (bounding box aproximado)
LIMA_BOUNDS = {
    "lat_min": -12.40,
    "lat_max": -11.80,
    "lon_min": -77.15,
    "lon_max": -76.90,
}
