paquetes = [
    # CHUBUT (1)
    [1, 1, "Puerto Madryn", "8d/7n",
     "Vuelo Aerolíneas ($654.879) o Flybondi ($535.000) / Bus Plusmar ($75.000-$100.000)",
     "Hotel Dazzle ($1.000.904) o Rayentray Hostal ($420.005)",
     "Península Valdés + avistaje de ballenas", 1500000],

    [1, 2, "Esquel", "8d/7n",
     "Vuelo Aerolíneas ($420.699) o Flybondi ($360.000) / Bus Plusmar ($85.000-$110.000)",
     "My Pod House ($145.000) o Depto Antigua Estación ($665.046)",
     "La Hoya (Esquí y Snowboard)", 700000],

    [1, 3, "Trelew", "8d/7n",
     "Vuelo Aerolíneas ($734.000) o Jetsmart ($580.058) / Bus Plusmar ($80.000-$110.000)",
     "Hotel Libertador ($498.980) o Cabañas El Colibrí ($693.798)",
     "Paseo aéreo Aeroclub Trelew", 1000000],

    [1, 4, "Comodoro Rivadavia", "8d/7n",
     "Vuelo Aerolíneas ($270.058) o Jetsmart ($230.000) / Bus Plusmar ($90.000-$130.000)",
     "Lucania Palazzo Hotel ($1.346.000) o Depto Paisaje 1 ($466.232)",
     "Patagonia Salvaje 4x4", 1200000],

    # SANTA CRUZ (2)
    [2, 1, "El Calafate", "8d/7n",
     "Vuelo Aerolíneas ($500.000) o Bus ($120.000)",
     "Hotel Los Álamos ($950.000) o Hostal Lago Argentino ($400.000)",
     "Glaciar Perito Moreno", 1300000],

    [2, 2, "Río Gallegos", "8d/7n",
     "Vuelo Jetsmart ($450.000) o Bus ($100.000)",
     "Hotel Patagonia ($800.000) o Depto céntrico ($300.000)",
     "Reserva Cabo Vírgenes", 1000000],

    [2, 3, "El Chaltén", "8d/7n",
     "Vuelo a El Calafate + transfer ($550.000) o Bus ($150.000)",
     "Hostería Fitz Roy ($750.000) o Camping El Relincho ($200.000)",
     "Trekking Laguna de los Tres", 950000],

    [2, 4, "Puerto Deseado", "8d/7n",
     "Vuelo a Comodoro + bus ($400.000) o Bus directo ($180.000)",
     "Hotel Los Acantilados ($600.000) o Hostería El Puerto ($250.000)",
     "Avistaje de toninas overas", 850000],

    # TIERRA DEL FUEGO (3)
    [3, 1, "Ushuaia", "8d/7n",
     "Vuelo Aerolíneas ($600.000) o Jetsmart ($520.000)",
     "Hotel Arakur ($1.200.000) o Hostería Foque ($450.000)",
     "Parque Nacional Tierra del Fuego", 1400000],

    [3, 2, "Tolhuin", "8d/7n",
     "Vuelo a Ushuaia + transfer ($620.000) o Bus ($200.000)",
     "Posada de la Madera ($500.000) o Cabañas Altos de Tolhuin ($300.000)",
     "Lago Fagnano + actividades náuticas", 900000],

    [3, 3, "Río Grande", "8d/7n",
     "Vuelo a Río Grande ($550.000) o Bus ($220.000)",
     "Gran Hotel Río Grande ($700.000) o Depto céntrico ($280.000)",
     "Pesca deportiva en el río", 850000],

    [3, 4, "Cabo San Pablo", "8d/7n",
     "Vuelo a Río Grande + transfer ($600.000) o Bus ($250.000)",
     "Estancia San Pablo ($650.000) o Hostería Cabo ($300.000)",
     "Excursión Faro + Desembarco Desdémona", 950000],

    # NEUQUÉN (4)
    [4, 1, "San Martín de los Andes", "8d/7n",
     "Vuelo Aerolíneas ($500.000) o Bus ($180.000)",
     "Hotel Patagonia Plaza ($900.000) o Cabañas Arrayanes ($400.000)",
     "Chapelco Ski Resort", 1200000],

    [4, 2, "Villa La Angostura", "8d/7n",
     "Vuelo a Bariloche + bus ($520.000) o Bus ($200.000)",
     "Hostería El Faro ($800.000) o Cabañas Los Ñires ($350.000)",
     "Bosque de Arrayanes", 1100000],

    [4, 3, "Caviahue", "8d/7n",
     "Vuelo a Neuquén + transfer ($480.000) o Bus ($190.000)",
     "Hotel Nevado ($700.000) o Hostel Caviahue ($250.000)",
     "Termas + volcán Copahue", 950000],

    [4, 4, "Zapala", "8d/7n",
     "Vuelo a Neuquén + bus ($460.000) o Bus ($170.000)",
     "Hotel Portal del Pehuén ($600.000) o Depto céntrico ($280.000)",
     "Parque Laguna Blanca", 850000],

    # RÍO NEGRO (5)
    [5, 1, "Bariloche", "8d/7n",
     "Vuelo Aerolíneas ($550.000) o Jetsmart ($480.000) / Bus ($180.000)",
     "Hotel Edelweiss ($1.000.000) o Hostel Pioneros ($350.000)",
     "Circuito Chico + Cerro Catedral", 1300000],

    [5, 2, "El Bolsón", "8d/7n",
     "Vuelo a Bariloche + bus ($500.000) o Bus ($200.000)",
     "Cabañas Piltriquitrón ($450.000) o Hostel Mandala ($200.000)",
     "Cajón del Azul", 800000],

    [5, 3, "Las Grutas", "8d/7n",
     "Vuelo a Viedma + bus ($450.000) o Bus ($220.000)",
     "Hotel Acantilados ($600.000) o Depto frente al mar ($300.000)",
     "Avistaje de fauna marina", 900000],

    [5, 4, "Viedma", "8d/7n",
     "Vuelo Aerolíneas ($400.000) o Bus ($180.000)",
     "Hotel Austral ($500.000) o Depto céntrico ($250.000)",
     "Balneario El Cóndor", 750000]
]

def mostrar_paquete(paquete):
    print("\n--- Paquete", paquete[1], "---")
    print("Destino:", paquete[2])
    print("Duración:", paquete[3])
    print("Transporte:", paquete[4])
    print("Alojamiento:", paquete[5])
    print("Excursión principal:", paquete[6])
    print("Costo total aprox:", paquete[7])

def buscar_por_provincia(matriz, nro_provincia, i=0, resultados=None):
    if resultados is None:
        resultados = []
    if i >= len(matriz):
        return resultados
    if matriz[i][0] == nro_provincia:
        resultados.append(matriz[i])
    return buscar_por_provincia(matriz, nro_provincia, i+1, resultados)

#Programa Principal
opcion = 0
while opcion != 3:
    print("\n--- Sistema de Paquetes Turísticos ---")
    print("1. Ver paquetes por provincia")
    print("2. Ver todos los destinos")
    print("3. Salir")

    opcion = int(input("Elija una opción: "))

    if opcion == 1:
        print("1=Chubut, 2=Santa Cruz, 3=Tierra del Fuego, 4=Neuquén, 5=Río Negro")
        prov = int(input("Ingrese número de provincia: "))
        resultados = buscar_por_provincia(paquetes, prov)
        if resultados:
            for r in resultados:
                mostrar_paquete(r)
        else:
            print("No hay paquetes para esa provincia")

    elif opcion == 2:
        print("\n--- Todos los destinos ---")
        for fila in paquetes:
            print(fila[2], "→", fila[7], "aprox")


