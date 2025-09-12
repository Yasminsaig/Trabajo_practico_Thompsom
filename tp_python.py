paquetes = [
    # Chubut - 1
    [1, 1, "Puerto Madryn", "8d/7n",
     [["Vuelo Aerolíneas", 800000, "Vuelo directo con snack incluido"],
      ["Bus Plusmar", 400000, "Bus cama, con comidas y bebidas incluidas"]],
     [["Hotel Dazzle ★★★★", 900000, "Habitación doble, desayuno incluido, pileta"],
      ["Hostal Rayentray ★★", 500000, "Habitación compartida, desayuno básico"]],
     "Avistaje de ballenas", 1500000, False],
    [1, 2, "Esquel", "8d/7n",
     [["Vuelo Aerolíneas", 700000, "Vuelo directo con snack"],
      ["Bus Plusmar", 300000, "Bus semi-cama con bebida"]],
     [["My Pod House ★★", 350000, "Habitación privada, desayuno incluido"],
      ["Depto Antigua Estación ★★★", 400000, "Departamento completo, cocina equipada"]],
     "La Hoya Ski Resort", 700000, False],
    [1, 3, "Trelew", "8d/7n",
     [["Vuelo Aerolíneas", 750000, "Vuelo directo, bebida incluida"],
      ["Bus Plusmar", 250000, "Bus con snack y bebida"]],
     [["Hotel Libertador ★★★", 600000, "Habitación doble, desayuno incluido"],
      ["Cabañas El Colibrí ★★", 400000, "Cabaña básica, cocina equipada"]],
     "Paseo aéreo Aeroclub", 1000000, False],
    [1, 4, "Comodoro Rivadavia", "8d/7n",
     [["Vuelo Aerolíneas", 800000, "Vuelo directo con snack"],
      ["Bus Plusmar", 400000, "Bus semi-cama, bebidas incluidas"]],
     [["Lucania Palazzo Hotel ★★★★", 900000, "Habitación doble, desayuno incluido, pileta"],
      ["Depto Paisaje 1 ★★", 300000, "Departamento básico, cocina equipada"]],
     "Patagonia Salvaje 4x4", 1200000, False],

    # Santa Cruz - 2
    [2, 1, "El Calafate", "8d/7n",
     [["Vuelo Aerolíneas", 900000, "Vuelo directo, snack y bebida"],
      ["Bus", 300000, "Bus semi-cama, refrigerios"]],
     [["Hotel Los Álamos ★★★★", 1000000, "Habitación doble, desayuno buffet, pileta"],
      ["Hostal Lago Argentino ★★", 500000, "Habitación sencilla, desayuno incluido"]],
     "Glaciar Perito Moreno", 1300000, False],
    [2, 2, "Río Gallegos", "8d/7n",
     [["Vuelo Jetsmart", 700000, "Vuelo low cost con snack"],
      ["Bus", 300000, "Bus semi-cama con bebida"]],
     [["Hotel Patagonia ★★★★", 900000, "Habitación doble, desayuno buffet"],
      ["Depto céntrico ★★", 400000, "Departamento básico, cocina equipada"]],
     "Reserva Cabo Vírgenes", 1000000, False],
    [2, 3, "El Chaltén", "8d/7n",
     [["Vuelo a Calafate + Transfer", 800000, "Vuelo + transfer incluido"],
      ["Bus", 250000, "Bus semi-cama con snack"]],
     [["Hostería Fitz Roy ★★★★", 850000, "Habitación doble, desayuno incluido"],
      ["Camping El Relincho ★", 100000, "Tienda básica, acceso a baño compartido"]],
     "Trekking Laguna de los Tres", 950000, False],
    [2, 4, "Puerto Deseado", "8d/7n",
     [["Vuelo a Comodoro + Bus", 700000, "Vuelo + bus con snack"],
      ["Bus directo", 200000, "Bus semi-cama con bebida"]],
     [["Hotel Los Acantilados ★★★", 650000, "Habitación doble, desayuno incluido"],
      ["Hostería El Puerto ★★", 400000, "Habitación básica, desayuno incluido"]],
     "Avistaje de toninas overas", 850000, False],

    # Tierra del Fuego - 3
    [3, 1, "Ushuaia", "8d/7n",
     [["Vuelo Aerolíneas", 950000, "Vuelo directo con snack"],
      ["Vuelo Jetsmart", 850000, "Vuelo low cost, bebida incluida"]],
     [["Hotel Arakur ★★★★★", 1300000, "Habitación doble, desayuno buffet, spa"],
      ["Hostería Foque ★★", 500000, "Habitación básica, desayuno incluido"]],
     "Parque Nacional Tierra del Fuego", 1400000, False],
    [3, 2, "Tolhuin", "8d/7n",
     [["Vuelo a Ushuaia + Transfer", 800000, "Vuelo + transfer"],
      ["Bus", 250000, "Bus semi-cama con snack"]],
     [["Posada de la Madera ★★★", 600000, "Habitación doble, desayuno incluido"],
      ["Cabañas Altos de Tolhuin ★★", 400000, "Cabaña básica, cocina equipada"]],
     "Lago Fagnano", 900000, False],
    [3, 3, "Río Grande", "8d/7n",
     [["Vuelo directo", 750000, "Vuelo directo con snack"],
      ["Bus", 250000, "Bus semi-cama con bebida"]],
     [["Gran Hotel Río Grande ★★★★", 700000, "Habitación doble, desayuno incluido"],
      ["Depto céntrico ★★", 350000, "Departamento básico, cocina equipada"]],
     "Pesca deportiva", 850000, False],
    [3, 4, "Cabo San Pablo", "8d/7n",
     [["Vuelo a Río Grande + Transfer", 800000, "Vuelo + transfer"],
      ["Bus", 250000, "Bus semi-cama con snack"]],
     [["Estancia San Pablo ★★★", 600000, "Habitación doble, desayuno incluido"],
      ["Hostería Cabo ★★", 400000, "Habitación básica, desayuno incluido"]],
     "Excursión Faro + Desdémona", 950000, False],

    # Neuquén - 4
    [4, 1, "San Martín de los Andes", "8d/7n",
     [["Vuelo Aerolíneas", 800000, "Vuelo directo con snack"],
      ["Bus", 400000, "Bus semi-cama con bebida"]],
     [["Hotel Patagonia Plaza ★★★★", 900000, "Habitación doble, desayuno incluido"],
      ["Cabañas Arrayanes ★★", 450000, "Cabaña básica, cocina equipada"]],
     "Chapelco Ski Resort", 1200000, False],
    [4, 2, "Villa La Angostura", "8d/7n",
     [["Vuelo a Bariloche + Bus", 750000, "Vuelo + transfer en bus"],
      ["Bus", 350000, "Bus semi-cama con snack"]],
     [["Hostería El Faro ★★★★", 850000, "Habitación doble, desayuno incluido"],
      ["Cabañas Los Ñires ★★", 400000, "Cabaña básica, cocina equipada"]],
     "Bosque de Arrayanes", 1100000, False],
    [4, 3, "Caviahue", "8d/7n",
     [["Vuelo a Neuquén + Transfer", 700000, "Vuelo + transfer"],
      ["Bus", 250000, "Bus semi-cama con snack"]],
     [["Hotel Nevado ★★★★", 800000, "Habitación doble, desayuno incluido"],
      ["Hostel Caviahue ★★", 400000, "Habitación básica, desayuno incluido"]],
     "Termas + Volcán Copahue", 950000, False],
    [4, 4, "Zapala", "8d/7n",
     [["Vuelo a Neuquén + Bus", 700000, "Vuelo + bus semi-cama con snack"]],
     [["Hotel Portal del Pehuén ★★★", 600000, "Habitación doble, desayuno incluido"],
      ["Depto céntrico ★★", 350000, "Departamento básico, cocina equipada"]],
     "Parque Laguna Blanca", 850000, False],

    # Río Negro - 5
    [5, 1, "Bariloche", "8d/7n",
     [["Vuelo Aerolíneas", 900000, "Vuelo directo con snack"],
      ["Bus", 400000, "Bus semi-cama con bebida"]],
     [["Hotel Edelweiss ★★★★", 1000000, "Habitación doble, desayuno incluido"],
      ["Hostel Pioneros ★★", 450000, "Habitación básica, desayuno incluido"]],
     "Circuito Chico + Cerro Catedral", 1300000, False],
    [5, 2, "El Bolsón", "8d/7n",
     [["Vuelo a Bariloche + Bus", 750000, "Vuelo + bus"],
      ["Bus", 350000, "Bus semi-cama con snack"]],
     [["Cabañas Piltriquitrón ★★★", 500000, "Habitación doble, desayuno incluido"],
      ["Hostel Mandala ★★", 350000, "Habitación básica, desayuno incluido"]],
     "Cajón del Azul", 800000, False],
    [5, 3, "Las Grutas", "8d/7n",
     [["Vuelo a Viedma + Bus", 700000, "Vuelo + bus semi-cama"],
      ["Bus", 300000, "Bus semi-cama con snack"]],
     [["Hotel Acantilados ★★★", 550000, "Habitación doble, desayuno incluido"],
      ["Depto frente al mar ★★", 400000, "Departamento básico, cocina equipada"]],
     "Avistaje de fauna marina", 900000, False],
    [5, 4, "Viedma", "8d/7n",
     [["Vuelo Aerolíneas", 650000, "Vuelo directo con snack"],
      ["Bus", 250000, "Bus semi-cama con bebida"]],
     [["Hotel Austral ★★★", 500000, "Habitación doble, desayuno incluido"],
      ["Depto céntrico ★★", 350000, "Departamento básico, cocina equipada"]],
     "Balneario El Cóndor", 750000, False]
]

def mostrar_paquete(paquete):
    print("\n ★ Paquete", paquete[1], "★")
    print("Destino:", paquete[2])
    print("Duración:", paquete[3])
    print("Opciones de transporte:")
    for i, t in enumerate(paquete[4], 1):
        print(f"  {i}. {t[0]} - ${t[1]} - {t[2]}")
    print("Opciones de alojamiento:")
    for i, h in enumerate(paquete[5], 1):
        print(f"  {i}. {h[0]} - ${h[1]} - {h[2]}")
    print("Excursión principal:", paquete[6])
    print("Excursiones opcionales:")
    print("Costo total aprox por persona:", paquete[7])
    print("Estado:", "Reservado" if paquete[8] else "Disponible")


def buscar_por_provincia(matriz, nro_provincia):
    return [fila for fila in matriz if fila[0] == nro_provincia]


def reservar_paquete(matriz, nro_provincia, nro_paquete):
    for fila in matriz:
        if fila[0] == nro_provincia and fila[1] == nro_paquete:
            if fila[8]:
                print("\nEse paquete ya está reservado.")
                return
            print("\nElija una opción de transporte:")
            for i, t in enumerate(fila[4], 1):
                print(f"{i}. {t[0]} - ${t[1]} - {t[2]}")
            t_sel = int(input("Ingrese número de transporte: ")) - 1

            print("\nElija una opción de alojamiento:")
            for i, h in enumerate(fila[5], 1):
                print(f"{i}. {h[0]} - ${h[1]} - {h[2]}")
            h_sel = int(input("Ingrese número de alojamiento: ")) - 1

            fila[8] = True
            fila.append(fila[4][t_sel])  # transporte elegido
            fila.append(fila[5][h_sel])  # alojamiento elegido

            print(f"\nReserva confirmada para: {fila[2]}")
            print(f"Transporte elegido: {fila[4][t_sel][0]} - ${fila[4][t_sel][1]}")
            print(f"Alojamiento elegido: {fila[5][h_sel][0]} - ${fila[5][h_sel][1]}")
            return
    print("\nNo se encontró el paquete.")

def paquete_reservado (matriz, nro_provincia, nro_paquete):
    for fila in matriz:
        if fila[0] == nro_provincia and fila[1] == nro_paquete and fila[8]:
            # Info elegida en la reserva
            destino = fila[2]
            transporte = fila[9]
            alojamiento = fila[10]

            # Formato tipo ticket
            print("-" * 40)
            print("Agencia de Viajes".center(40))
            print()
            print("Av. 9 de julio 279".ljust(20), end="**")
            print("Tel. 46019-1146".rjust(20))
            print()
            print("Reserva N°", str(fila[1]).zfill(8))
            print()
            print("Destino:".ljust(15), destino)
            print("Transporte:".ljust(15), f"{transporte[0]} (${transporte[1]})")
            print("Alojamiento:".ljust(15), f"{alojamiento[0]} (${alojamiento[1]})")
            print("-" * 40)

            print("Para realizar el pago final comuniquese con el numero en pantalla")
            conf = input("¿Confirma la reserva? (s/n): ").strip().lower()
            if conf == "s":
                print("\n✅ Reserva confirmada con éxito. ¡Buen viaje!")
            else:
                print("\n⚠ Reserva cancelada. Vuelva a seleccionar opciones.")
                fila[8] = False 
                reservar_paquete(matriz, nro_provincia, nro_paquete)
            return
    print("\n❌ No hay ninguna reserva para mostrar.")


# Programa principal
opcion = 0
while opcion != 4:
    print("\n   Sistema de Paquetes Turísticos ")
    print("1. Ver paquetes por provincia")
    print("2. Reservar un paquete")
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
            print("No hay paquetes para esa provincia.")

    elif opcion == 2:
        print("1=Chubut, 2=Santa Cruz, 3=Tierra del Fuego, 4=Neuquén, 5=Río Negro")
        prov = int(input("Ingrese número de provincia: "))
        resultados = buscar_por_provincia(paquetes, prov)
        nro = int(input("Ingrese número de paquete: "))
        reservar_paquete(paquetes, prov, nro)
        paquete_reservado(paquetes, prov, nro)

    elif opcion == 3:
        print("¡Hasta luego!")
    else:
        print("Opción inválida.")


