paquetes = [
    # Chubut - 1
    [1, 1, "Puerto Madryn", "8d/7n", "Vuelo Aerolíneas / Bus Plusmar",
     "Hotel Dazzle ★★★★ / Hostal Rayentray ★★", "Avistaje de ballenas", 1500000, False],

    [1, 2, "Esquel", "8d/7n", "Vuelo Aerolíneas / Bus Plusmar",
     "My Pod House ★★ / Depto Antigua Estación ★★★", "La Hoya Ski Resort", 700000, False],

    [1, 3, "Trelew", "8d/7n", "Vuelo Aerolíneas / Bus Plusmar",
     "Hotel Libertador ★★★ / Cabañas El Colibrí ★★", "Paseo aéreo Aeroclub", 1000000, False],

    [1, 4, "Comodoro Rivadavia", "8d/7n", "Vuelo Aerolíneas / Bus Plusmar",
     "Lucania Palazzo Hotel ★★★★ / Depto Paisaje 1 ★★", "Patagonia Salvaje 4x4", 1200000, False],

    # Santa Cruz - 2
    [2, 1, "El Calafate", "8d/7n", "Vuelo Aerolíneas / Bus",
     "Hotel Los Álamos ★★★★ / Hostal Lago Argentino ★★", "Glaciar Perito Moreno", 1300000, False],

    [2, 2, "Río Gallegos", "8d/7n", "Vuelo Jetsmart / Bus",
     "Hotel Patagonia ★★★★ / Depto céntrico ★★", "Reserva Cabo Vírgenes", 1000000, False],

    [2, 3, "El Chaltén", "8d/7n", "Vuelo a Calafate + Transfer / Bus",
     "Hostería Fitz Roy ★★★★ / Camping El Relincho ★", "Trekking Laguna de los Tres", 950000, False],

    [2, 4, "Puerto Deseado", "8d/7n", "Vuelo a Comodoro + Bus / Bus directo",
     "Hotel Los Acantilados ★★★ / Hostería El Puerto ★★", "Avistaje de toninas overas", 850000, False],

    # Tierra del Fuego - 3
    [3, 1, "Ushuaia", "8d/7n", "Vuelo Aerolíneas / Jetsmart",
     "Hotel Arakur ★★★★★ / Hostería Foque ★★", "Parque Nacional Tierra del Fuego", 1400000, False],

    [3, 2, "Tolhuin", "8d/7n", "Vuelo a Ushuaia + Transfer / Bus",
     "Posada de la Madera ★★★ / Cabañas Altos de Tolhuin ★★", "Lago Fagnano", 900000, False],

    [3, 3, "Río Grande", "8d/7n", "Vuelo directo / Bus",
     "Gran Hotel Río Grande ★★★★ / Depto céntrico ★★", "Pesca deportiva", 850000, False],

    [3, 4, "Cabo San Pablo", "8d/7n", "Vuelo a Río Grande + Transfer / Bus",
     "Estancia San Pablo ★★★ / Hostería Cabo ★★", "Excursión Faro + Desdémona", 950000, False],

    # Neuquén - 4
    [4, 1, "San Martín de los Andes", "8d/7n", "Vuelo Aerolíneas / Bus",
     "Hotel Patagonia Plaza ★★★★ / Cabañas Arrayanes ★★", "Chapelco Ski Resort", 1200000, False],

    [4, 2, "Villa La Angostura", "8d/7n", "Vuelo a Bariloche + Bus / Bus",
     "Hostería El Faro ★★★★ / Cabañas Los Ñires ★★", "Bosque de Arrayanes", 1100000, False],

    [4, 3, "Caviahue", "8d/7n", "Vuelo a Neuquén + Transfer / Bus",
     "Hotel Nevado ★★★★ / Hostel Caviahue ★★", "Termas + Volcán Copahue", 950000, False],

    [4, 4, "Zapala", "8d/7n", "Vuelo a Neuquén + Bus / Bus",
     "Hotel Portal del Pehuén ★★★ / Depto céntrico ★★", "Parque Laguna Blanca", 850000, False],

    # Rio Negro - 5
    [5, 1, "Bariloche", "8d/7n", "Vuelo Aerolíneas / Bus",
     "Hotel Edelweiss ★★★★ / Hostel Pioneros ★★", "Circuito Chico + Cerro Catedral", 1300000, False],

    [5, 2, "El Bolsón", "8d/7n", "Vuelo a Bariloche + Bus / Bus",
     "Cabañas Piltriquitrón ★★★ / Hostel Mandala ★★", "Cajón del Azul", 800000, False],

    [5, 3, "Las Grutas", "8d/7n", "Vuelo a Viedma + Bus / Bus",
     "Hotel Acantilados ★★★ / Depto frente al mar ★★", "Avistaje de fauna marina", 900000, False],

    [5, 4, "Viedma", "8d/7n", "Vuelo Aerolíneas / Bus",
     "Hotel Austral ★★★ / Depto céntrico ★★", "Balneario El Cóndor", 750000, False]
]

def mostrar_paquete(paquete):
    print("\n ★ Paquete", paquete[1], "★")
    print("Destino:", paquete[2])
    print("Duración:", paquete[3])
    print("Transporte:", paquete[4])
    print("Alojamiento:", paquete[5])
    print("Excursión principal:", paquete[6])
    print("Costo total aprox:", paquete[7])
    print("Estado:", "Reservado" if paquete[8] else "Disponible")

def buscar_por_provincia(matriz, nro_provincia):
    resultados = []
    for fila in matriz:
        if fila[0] == nro_provincia:
            resultados.append(fila)
    return resultados

def reservar_paquete(matriz, nro_provincia, nro_paquete):
    for fila in matriz:
        if fila[0] == nro_provincia and fila[1] == nro_paquete:
            if not fila[8]:
                fila[8] = True
                print("\n Reserva confirmada para:", fila[2])
            else:
                print("\n Ese paquete ya está reservado.")
            return
    print("\n No se encontró el paquete.")

# Programa principal
opcion = 0
while opcion != 4:
    print("\n  ★  Sistema de Paquetes Turísticos ★")
    print("1. Ver paquetes por provincia")
    print("2. Ver todos los destinos")
    print("3. Reservar un paquete")
    print("4. Salir")

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
        print("\n ★ Todos los destinos ★")
        for fila in paquetes:
            print(fila[2], "→", fila[7], "aprox", "(", "Reservado" if fila[8] else "Disponible", ")")

    elif opcion == 3:
        prov = int(input("Ingrese número de provincia: "))
        nro = int(input("Ingrese número de paquete: "))
        reservar_paquete(paquetes, prov, nro)
    else:
        print("¡Hasta luego!")
