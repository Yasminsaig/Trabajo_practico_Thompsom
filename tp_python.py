paquetes = [
    # Chubut - 1
    [1, 1, "Puerto Madryn", "8d/7n",    
    [["Vuelo Aerolíneas Argentinas", 654879, "Vuelo ida y vuelta (2 hs). Incluye mochila, carry-on, equipaje a despachar y asiento a elección"],
    ["Vuelo Flybondi", 535000, "Vuelo ida y vuelta (2 hs). Incluye mochila, carry-on, equipaje a despachar y asiento a elección"],
    ["Micro Plusmar semicama", 75000, "Ida y vuelta (19 hs). Incluye mochila y valija mediana"],
    ["Micro Plusmar cama", 100000, "Ida y vuelta (19 hs). Incluye mochila y valija mediana"]],
    [["Hotel Dazzle by Wyndham ★★★★", 1000904, "Incluye desayuno, spa, gimnasio, admite mascotas, traslados al aeropuerto, vista al mar, cancelación gratis. Costo + impuestos"],
    ["Hotel Rayentray Hostal ★★", 420005, "Incluye desayuno, cancelación gratis. Costo + impuestos"]],
    ["Península Valdés + avistaje de ballenas", 170000,
    [
    ["Snorkel con lobos marinos y peces", 205000],
    ["Excursión terrestre a Trelew y Gaiman", 175000],
    ["Punta Tombo por crucero (pingüinos)", 198000],
    ["Paseo náutico (avistaje de delfines)", 167000]]
    ],
     1500000, False]
]

def mostrar_paquete(fila, indice=1):
    destino = fila[2]
    transporte = fila[4][0]  
    alojamiento = fila[5][0]  
    excursion_principal = fila[6] 

    print("-" * 60)
    titulo = f"PAQUETE {indice}"
    print(titulo.rjust((60 + len(titulo)) // 2))
    print("-" * 60)

    print("Destino:".ljust(20), destino)
    print("Duración:".ljust(20), fila[3])

    print("\nTransporte:")
    for j, t in enumerate(fila[4], 1):
        print(f"  {j}. {t[0]} - ${t[1]} - {t[2]}")

    print("\nAlojamiento:")
    for j, h in enumerate(fila[5], 1):
        print(f"  {j}. {h[0]} - ${h[1]} - {h[2]}")

    print("\nExcursión principal:".ljust(20), f"{excursion_principal[0]} - ${excursion_principal[1]}")

    if len(excursion_principal) > 2 and isinstance(excursion_principal[2], list):
        print("\nExcursiones opcionales:")
        for j, e in enumerate(excursion_principal[2], 1):
            print(f"  {j}. {e[0]} - ${e[1]}")

    precio_aprox = transporte[1] + alojamiento[1] + excursion_principal[1]
    print("\nPrecio aproximado del paquete: $", precio_aprox)
    print("-" * 60)
    print()


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
            t_sel = -1
            while t_sel < 0 or t_sel >= len(fila[4]):
                t_sel = int(input("Ingrese número de transporte: "))-1
                if t_sel < 0 or t_sel >= len(fila[4]):
                    print("Opción inválida. Intente nuevamente.")

            print("\nElija una opción de alojamiento:")
            for i, h in enumerate(fila[5], 1):
                print(f"{i}. {h[0]} - ${h[1]} - {h[2]}")
            h_sel = -1
            while h_sel < 0 or h_sel >= len(fila[5]):
                h_sel = int(input("Ingrese número de alojamiento: ")) - 1
                if h_sel < 0 or h_sel >= len(fila[5]):
                    print("Opción inválida. Intente nuevamente.")

            print("\nElija excursiones opcionales (separadas por coma, o 0 para ninguna):")
            for i, e in enumerate(fila[6][2], 1):
                print(f"{i}. {e[0]} - ${e[1]}")
            excursiones_extra = []
            opcionales = input("Ingrese números de excursiones: ").strip()
            while True:
                if opcionales == "0" or opcionales == "":
                    break
                indices = opcionales.split(",")
                if all(x.isdigit() and 1 <= int(x) <= len(fila[6][2]) for x in indices):
                    excursiones_extra = [fila[6][2][int(i)-1] for i in indices]
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
                    opcionales = input("Ingrese números de excursiones: ").strip()

            fila[8] = True
            fila.append(fila[4][t_sel])
            fila.append(fila[5][h_sel])
            fila.append(excursiones_extra)

            print(f"\nReserva confirmada para: {fila[2]}")
            print(f"Transporte elegido: {fila[4][t_sel][0]} - ${fila[4][t_sel][1]}")
            print(f"Alojamiento elegido: {fila[5][h_sel][0]} - ${fila[5][h_sel][1]}")
            if excursiones_extra:
                print("Excursiones adicionales elegidas:")
                for e in excursiones_extra:
                    print(f" - {e[0]} - ${e[1]}")
            else:
                print("No se eligieron excursiones adicionales.")
            return

    print("\nNo se encontró el paquete.")

def paquete_reservado(matriz, nro_provincia, nro_paquete):
    for fila in matriz:
        if fila[0] == nro_provincia and fila[1] == nro_paquete and fila[8]:
            destino = fila[2]
            transporte = fila[9]
            alojamiento = fila[10]
            excursion_principal = fila[6]  

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
            print("Excursión principal:".ljust(20), f"{excursion_principal[0]} (${excursion_principal[1]})")

            total_excursiones = excursion_principal[1]  
            print("Excursiones opcionales elegidas:")
            if len(fila) > 11 and fila[11]:
                for e in fila[11]:
                    print(f" - {e[0]} (${e[1]})")
                    total_excursiones += e[1]
            else:
                print(" - Ninguna")

            monto_total = transporte[1] + alojamiento[1] + total_excursiones
            print("-" * 40)
            print(f"Monto total: ${monto_total}")
            print("-" * 40)

            print("Para realizar el pago final comuníquese con el número en pantalla")
            conf = input("¿Confirma la reserva? (si/no): ").strip().lower()

            if conf == "si":
                print("\n✅ Reserva confirmada con éxito. ¡Buen viaje!")
            else:
                print("\n⚠ Reserva cancelada. Vuelva a seleccionar opciones.")
                fila[8] = False 
                reservar_paquete(matriz, nro_provincia, nro_paquete)
                paquete_reservado(matriz, nro_provincia, nro_paquete) 
            return
    print("\n❌ No hay ninguna reserva para mostrar.")


# Programa principal
opcion = 0
while opcion != 3:
    print("\n" + "-" * 50)
    print("SISTEMA DE PAQUETES TURÍSTICOS".rjust(35))  
    print("-" * 50)
    print("1. Ver paquetes por provincia".rjust(35))
    print("2. Reservar un paquete".rjust(35))
    print("3. Salir".rjust(35))
    print("-" * 50)
    
    opcion = int(input("Seleccione una opción (1-3): "))

    if opcion == 1:
        print("1=Chubut, 2=Santa Cruz, 3=Tierra del Fuego, 4=Neuquén, 5=Río Negro")
        prov = int(input("Ingrese número de provincia: "))
        resultados = buscar_por_provincia(paquetes, prov)
        if resultados:
            for i, r in enumerate(resultados, start=1):
                mostrar_paquete(r, i)

        else:
            print("No hay paquetes para esa provincia.")
    elif opcion == 2:
        print("1=Chubut, 2=Santa Cruz, 3=Tierra del Fuego, 4=Neuquén, 5=Río Negro")
        prov = int(input("Ingrese número de provincia: "))
        nro = int(input("Ingrese número de paquete: "))
        reservar_paquete(paquetes, prov, nro)
        paquete_reservado(paquetes, prov, nro)

    elif opcion == 3:
        print("¡Hasta luego!")
    else:
        print("Opción inválida.")
