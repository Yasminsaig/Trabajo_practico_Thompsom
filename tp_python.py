import datetime
import os

ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_PAQUETES = "paquetes.txt"
ARCHIVO_RESERVAS = "reservas.txt"
ARCHIVO_TICKET_COUNTER = "ticket_counter.txt"

#----------------------------------------------------
#      Funciones de archivos
#----------------------------------------------------

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_siguiente_ticket():
    ultimo_ticket = 0
    archivo_contador = None
    try:
        archivo_contador = open(ARCHIVO_TICKET_COUNTER, "r")
        contenido = archivo_contador.read()
        if contenido:
            ultimo_ticket = int(contenido)
    except (FileNotFoundError, ValueError):
        ultimo_ticket = 0
    finally:
        if archivo_contador:
            archivo_contador.close()

    siguiente_ticket = ultimo_ticket + 1

    archivo_contador_escritura = None
    try:
        archivo_contador_escritura = open(ARCHIVO_TICKET_COUNTER, "w")
        archivo_contador_escritura.write(str(siguiente_ticket))
    except OSError:
        pass
    finally:
        if archivo_contador_escritura:
            archivo_contador_escritura.close()

    return siguiente_ticket

def realizar_login():
    print("--- Bienvenido/a al Sistema de Paquetes Turísticos ---")
    usuario_ingresado = input("Usuario: ")
    contrasena_ingresada = input("Contraseña: ")
    acceso_concedido = False
    archivo_usuarios = None
    try:
        archivo_usuarios = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
        for linea in archivo_usuarios:
            try:
                usuario_archivo, contrasena_archivo = linea.strip().split(";")
                if usuario_ingresado == usuario_archivo and contrasena_ingresada == contrasena_archivo:
                    acceso_concedido = True
                    break
            except ValueError:
                continue
    except FileNotFoundError:
        print(f"\nADVERTENCIA: No se encontró '{ARCHIVO_USUARIOS}'. Puede registrar un usuario.")
    except Exception:
        print(f"\nERROR: El archivo '{ARCHIVO_USUARIOS}' podría estar corrupto.")
    finally:
        if archivo_usuarios:
            archivo_usuarios.close()
    return acceso_concedido

def registrar_usuario():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    usuario_valido = False
    nuevo_usuario = ""
    while not usuario_valido:
        nuevo_usuario = input("Ingrese su nuevo nombre de usuario: ").strip()
        if not nuevo_usuario:
            print("Error: El nombre de usuario no puede estar vacío.")
            continue

        usuario_existe = False
        archivo_lectura = None
        try:
            archivo_lectura = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
            for linea in archivo_lectura:
                try:
                    if linea.strip().split(';')[0].lower() == nuevo_usuario.lower():
                        usuario_existe = True
                        break
                except (ValueError, IndexError):
                    continue
        except FileNotFoundError:
            pass
        finally:
            if archivo_lectura:
                archivo_lectura.close()

        if usuario_existe:
            print("Error: Ese nombre de usuario ya está en uso.")
        else:
            usuario_valido = True

    nueva_contrasena = input("Ingrese su nueva contraseña: ")
    archivo_escritura = None
    try:
        archivo_escritura = open(ARCHIVO_USUARIOS, "at", encoding='utf-8')
        archivo_escritura.write(f"{nuevo_usuario};{nueva_contrasena}\n")
        print("\n¡Usuario registrado con éxito!")
    except OSError as e:
        print(f"\nERROR: No se pudo registrar el usuario. {e}")
    finally:
        if archivo_escritura:
            archivo_escritura.close()

def cargar_paquetes():
    lista_de_paquetes = []
    archivo_paquetes = None
    try:
        archivo_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding='utf-8')
        paquete_actual = None
        seccion_actual = ""

        for linea in archivo_paquetes:
            linea = linea.strip()
            if not linea: continue

            if linea.startswith('#PAQUETE'):
                if paquete_actual: lista_de_paquetes.append(paquete_actual)
                paquete_actual = {}
                seccion_actual = "paquete"
            elif linea.startswith('#FIN_PAQUETE'):
                if paquete_actual:
                    lista_de_paquetes.append(paquete_actual)
                    paquete_actual = None
                seccion_actual = ""
            elif linea.startswith('#') and paquete_actual is not None:
                seccion_actual = linea[1:].lower()
                if seccion_actual not in ["excursion_base", "paquete"]:
                         paquete_actual[seccion_actual] = []
            elif seccion_actual and paquete_actual is not None:
                partes = linea.split(';')

                if seccion_actual == "paquete":
                    id_str, prov, dest, dur, precio_str, cupo_str = partes
                    paquete_actual.update({
                        "id": int(id_str), "provincia": prov, "destino": dest,
                        "duracion": dur, "precio_base": float(precio_str), "cupo": int(cupo_str)
                    })
                elif seccion_actual in ["transporte", "alojamiento"]:
                    nombre, precio, desc = partes[0], float(partes[1]), partes[2] if len(partes) > 2 else ""
                    paquete_actual[seccion_actual].append({"nombre": nombre, "precio": precio, "desc": desc})
                elif seccion_actual == "fechas":
                    nombre_fecha, valor_fecha = partes[0], partes[1]
                    paquete_actual[seccion_actual].append({"nombre": nombre_fecha, "fecha": valor_fecha})
                else:
                    nombre, precio = partes[0], float(partes[1])
                    if seccion_actual == "excursion_base":
                        paquete_actual[seccion_actual] = {"nombre": nombre, "precio": precio}
                    else:
                        if seccion_actual not in paquete_actual:
                            paquete_actual[seccion_actual] = []
                        paquete_actual[seccion_actual].append({"nombre": nombre, "precio": precio})

        if paquete_actual and paquete_actual not in lista_de_paquetes:
            lista_de_paquetes.append(paquete_actual)

    except FileNotFoundError: print(f"\nADVERTENCIA: No se encontró '{ARCHIVO_PAQUETES}'.")
    except Exception as e: print(f"\nERROR: '{ARCHIVO_PAQUETES}' parece tener un formato incorrecto. Detalle: {e}")
    finally:
        if archivo_paquetes: archivo_paquetes.close()

    return lista_de_paquetes

def guardar_paquetes(paquetes):
    archivo_paquetes = None
    try:
        archivo_paquetes = open(ARCHIVO_PAQUETES, "wt", encoding='utf-8')
        for paquete in paquetes:
            archivo_paquetes.write("#PAQUETE\n")
            archivo_paquetes.write(f"{paquete['id']};{paquete['provincia']};{paquete['destino']};{paquete['duracion']};{paquete['precio_base']};{paquete['cupo']}\n")

            for seccion, marcador in [('transporte', '#TRANSPORTE'), ('alojamiento', '#ALOJAMIENTO')]:
                if seccion in paquete and paquete[seccion]:
                    archivo_paquetes.write(f"{marcador}\n")
                    for opcion in paquete[seccion]:
                        archivo_paquetes.write(f"{opcion['nombre']};{opcion['precio']};{opcion.get('desc', '')}\n")

            if 'excursion_base' in paquete and paquete['excursion_base']:
                archivo_paquetes.write("#EXCURSION_BASE\n")
                eb = paquete['excursion_base']
                archivo_paquetes.write(f"{eb['nombre']};{eb['precio']}\n")

            if 'excursiones_adicionales' in paquete and paquete['excursiones_adicionales']:
                archivo_paquetes.write("#EXCURSIONES_ADICIONALES\n")
                for opcion in paquete['excursiones_adicionales']:
                    archivo_paquetes.write(f"{opcion['nombre']};{opcion['precio']}\n")

            if 'fechas' in paquete and paquete['fechas']:
                archivo_paquetes.write("#FECHAS\n")
                for opcion in paquete['fechas']:
                    archivo_paquetes.write(f"{opcion['nombre']};{opcion['fecha']}\n")

            archivo_paquetes.write("#FIN_PAQUETE\n\n")
    except OSError as e: print(f"\nERROR: No se pudo guardar los cambios. {e}")
    finally:
        if archivo_paquetes: archivo_paquetes.close()

def registrar_reserva_en_archivo(ticket, paquete, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final):
    archivo_reservas = None
    try:
        archivo_reservas = open(ARCHIVO_RESERVAS, "at", encoding='utf-8')
        fecha_reserva = datetime.date.today().strftime('%d/%m/%Y')

        detalles = f"Transporte: {opciones_elegidas['transporte']['nombre']} | Alojamiento: {opciones_elegidas['alojamiento']['nombre']}"
        if opciones_elegidas.get('excursion_adicional'):
            detalles += f" | Extra: {opciones_elegidas['excursion_adicional']['nombre']}"

        fecha_nombre = opcion_fecha['nombre'] if opcion_fecha and 'nombre' in opcion_fecha else 'N/A'

        linea = f"{ticket};{paquete['id']};{paquete['destino']};{nombre_cliente};{fecha_reserva};{fecha_nombre};{precio_final:.2f};ACTIVA;{detalles}\n"
        archivo_reservas.write(linea)
    except OSError as e: print(f"\nERROR: No se pudo guardar la reserva. {e}")
    finally:
        if archivo_reservas: archivo_reservas.close()

#----------------------------------------------------
#        Funciones auxiliares
#----------------------------------------------------
def agrupar_paquetes_por_provincia(paquetes_lista):
    paquetes_agrupados = {}
    for paquete in paquetes_lista:
        provincia = paquete['provincia']
        if provincia not in paquetes_agrupados:
            paquetes_agrupados[provincia] = []
        paquetes_agrupados[provincia].append(paquete)
    return paquetes_agrupados

def cumple_filtros(paquete, filtros):
    if 'destino' in filtros and filtros['destino']:
        if filtros['destino'].lower() not in paquete['destino'].lower():
            return False
    if 'precio_max' in filtros:
        if paquete['precio_base'] > filtros['precio_max']:
            return False
    return True

def buscar_recursivo(lista_paquetes, filtros, indice=0):
    if indice >= len(lista_paquetes):
        return []
    resultados_del_resto = buscar_recursivo(lista_paquetes, filtros, indice + 1)
    paquete_actual = lista_paquetes[indice]
    if cumple_filtros(paquete_actual, filtros):
        return [paquete_actual] + resultados_del_resto
    else:
        return resultados_del_resto

def seleccionar_opcion(nombre_seccion, lista_opciones, permite_ninguno=False):
    opcion_valida = False
    opcion_seleccionada = None

    if not lista_opciones:
        print(f"No hay opciones disponibles para {nombre_seccion}.")
        return None

    print(f"\n--- Opciones de {nombre_seccion} ---")
    for i, opcion in enumerate(lista_opciones, 1):
        print(f"   {i}. {opcion.get('nombre', opcion)}", end="")
        if 'precio' in opcion:
             print(f" (+${opcion['precio']:,.2f})")
        else:
             print()

    while not opcion_valida:
        try:
            prompt = f"Seleccione Nro de {nombre_seccion} (1-{len(lista_opciones)}"
            prompt += ", 0 para ninguna): " if permite_ninguno else "): "
            opcion_num_str = input(prompt)
            opcion_num = int(opcion_num_str)

            if permite_ninguno and opcion_num == 0:
                opcion_seleccionada = None
                opcion_valida = True
            elif 1 <= opcion_num <= len(lista_opciones):
                opcion_seleccionada = lista_opciones[opcion_num - 1]
                opcion_valida = True
            else:
                print("Error: Número fuera de rango.")
        except ValueError:
            print("Error: Ingrese un número válido.")

    return opcion_seleccionada

#----------------------------------------------------
#        Funciones principales del menú
#----------------------------------------------------

def mostrar_detalles_paquete(paquete):
    limpiar_consola()
    print("=" * 70)
    print(f"DETALLES DEL PAQUETE ID: {paquete['id']} - {paquete['destino']}, {paquete['provincia']}")
    print(f"Duración: {paquete['duracion']} | Cupo actual: {paquete['cupo']}")
    print(f"Precio Base: ${paquete['precio_base']:,.2f}")

    for seccion, titulo in [('transporte', 'Transporte'), ('alojamiento', 'Alojamiento')]:
        if paquete.get(seccion):
            print(f"\n--- Opciones de {titulo} ---")
            for i, opcion in enumerate(paquete[seccion], 1):
                print(f"   {i}. {opcion['nombre']} (+${opcion['precio']:,.2f})")
                if opcion.get('desc'):
                    print(f"     Descripción: {opcion['desc']}")

    if paquete.get('fechas'):
        print("\n--- Fechas ---")
        for i, opcion in enumerate(paquete['fechas'], 1):
            print(f"   {i}. {opcion['nombre']}: {opcion['fecha']}")

    excursion_base = paquete.get('excursion_base')
    if excursion_base and 'nombre' in excursion_base and 'precio' in excursion_base:
        print(f"\n--- Excursión Incluida ---")
        print(f"   - {excursion_base['nombre']} (+${excursion_base['precio']:,.2f})")

    excursiones_adicionales = paquete.get('excursiones_adicionales')
    if excursiones_adicionales:
        print("\n--- Excursiones Adicionales (Opcionales) ---")
        for i, opcion in enumerate(excursiones_adicionales, 1):
            print(f"   {i}. {opcion['nombre']} (+${opcion['precio']:,.2f})")

    print("=" * 70)

def gestionar_vista_de_paquetes(paquetes):
    if not paquetes:
        print("\nNo hay paquetes cargados."); return

    paquetes_agrupados = agrupar_paquetes_por_provincia(paquetes)
    provincias = list(paquetes_agrupados.keys())

    salir_vista = False
    while not salir_vista:
        limpiar_consola()
        print("--- VER PAQUETES (Paso 1: Provincia) ---")
        for i, prov in enumerate(provincias, 1):
            print(f"   {i}. {prov}")
        print("\n   0. Volver al Menú Principal")

        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                salir_vista = True; continue 

            if 1 <= nro_prov <= len(provincias):
                provincia_elegida = provincias[nro_prov - 1]
                paquetes_de_provincia = paquetes_agrupados[provincia_elegida]

                ver_paquetes = True
                while ver_paquetes:
                    limpiar_consola()
                    print(f"--- PAQUETES EN {provincia_elegida.upper()} ---")
                    for i, p in enumerate(paquetes_de_provincia, 1):
                        print(f"   {i}. {p['destino']}") # Muestra el número y destino
                    print("\n   0. Volver a Provincias")

                    nro_paq_str = input("\nSeleccione el Nro del Paquete para ver detalles: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            ver_paquetes = False; continue

                        if 1 <= nro_paq <= len(paquetes_de_provincia):
                            paquete_elegido = paquetes_de_provincia[nro_paq - 1]
                            mostrar_detalles_paquete(paquete_elegido) 
                            input("\nPresione Enter para volver a la lista de paquetes...") 
                        else:
                            print("Error: Número de paquete no válido."); input("...")
                    except ValueError:
                         print("Error: Ingrese un número."); input("...")
            else:
                print("Error: Número de provincia no válido."); input("...")
        except ValueError:
            print("Error: Ingrese un número."); input("...")

def iniciar_busqueda_recursiva(paquetes):
    limpiar_consola()
    print("--- BÚSQUEDA DE PAQUETES ---"); print("Deje en blanco lo que no quiera filtrar.")
    filtros = {} 

    destino_filtro = input("Ingrese destino a buscar: ").strip()
    if destino_filtro:
        filtros['destino'] = destino_filtro

    try:
        precio_max_str = input("Ingrese precio máximo base (o 0 para no filtrar): ").strip()
        if precio_max_str:
            precio_max = float(precio_max_str)
            if precio_max > 0: filtros['precio_max'] = precio_max
    except ValueError:
        print("Precio máximo inválido, no se filtrará por precio.")

    resultados = buscar_recursivo(paquetes, filtros)

    print("\n--- RESULTADOS DE LA BÚSQUEDA ---")
    if not resultados:
        print("No se encontraron paquetes que coincidan con los criterios.")
    else:
        print(f"{'NRO':<5}{'PROVINCIA':<20}{'DESTINO':<45}{'PRECIO BASE':<20}{'CUPO':<5}")
        print("-" * 100)
        for i, paquete in enumerate(resultados, 1):
            print(f"{i:<5}{paquete['provincia']:<20}{paquete['destino']:<45}${paquete['precio_base']:<19,.2f}{paquete['cupo']:<5}")

    input("\nPresione Enter para volver al menú...")

def gestionar_reserva(paquetes):
    limpiar_consola()
    print("--- REALIZAR UNA RESERVA ---")

    if not paquetes:
        print("\nNo hay paquetes para reservar.")
        input("Presione Enter para volver...")
        return

    paquetes_agrupados = agrupar_paquetes_por_provincia(paquetes)
    provincias = list(paquetes_agrupados.keys())

    paquete_elegido = None
    salir_seleccion = False

    while not salir_seleccion:
        limpiar_consola()
        print("--- REALIZAR UNA RESERVA (Paso 1: Provincia) ---")
        for i, prov in enumerate(provincias, 1):
            print(f"   {i}. {prov}")
        print("\n   0. Volver al Menú Principal")

        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0: return 

            if 1 <= nro_prov <= len(provincias):
                provincia_elegida = provincias[nro_prov - 1]
                paquetes_de_provincia = paquetes_agrupados[provincia_elegida]

                seleccionar_paquete = True
                while seleccionar_paquete: 
                    limpiar_consola()
                    print(f"--- REALIZAR UNA RESERVA (Paso 2: Paquete en {provincia_elegida.upper()}) ---")
                    for i, p in enumerate(paquetes_de_provincia, 1):
                        print(f"   {i}. {p['destino']} (Cupo: {p['cupo']})")
                    print("\n   0. Volver a Provincias")

                    nro_paq_str = input("\nSeleccione el Nro del Paquete a reservar: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            seleccionar_paquete = False; continue 

                        if 1 <= nro_paq <= len(paquetes_de_provincia):
                            paquete_elegido = paquetes_de_provincia[nro_paq - 1]
                            seleccionar_paquete = False 
                            salir_seleccion = True    
                        else:
                            print("Error: Número de paquete no válido."); input("...")
                    except ValueError:
                         print("Error: Ingrese un número."); input("...")
            else:
                print("Error: Número de provincia no válido."); input("...")
        except ValueError:
            print("Error: Ingrese un número."); input("...")
   
    if paquete_elegido:
        if paquete_elegido['cupo'] <= 0:
            print(f"\nLo sentimos, no hay cupo para {paquete_elegido['destino']}.")
            input("\nPresione Enter para volver al menú...")
            return

        mostrar_detalles_paquete(paquete_elegido)

        opcion_transporte = seleccionar_opcion("Transporte", paquete_elegido.get('transporte', []))
        opcion_alojamiento = seleccionar_opcion("Alojamiento", paquete_elegido.get('alojamiento', []))
        opcion_fecha = seleccionar_opcion("fecha", paquete_elegido.get('fechas', []))

        if not opcion_transporte or not opcion_alojamiento or not opcion_fecha:
             print("\nError: Debe seleccionar transporte, alojamiento y fecha para continuar.")
             input("\nPresione Enter para volver al menú...")
             return

        excursion_adicional_elegida = None
        excursiones_adicionales = paquete_elegido.get('excursiones_adicionales')
        if excursiones_adicionales: 
            agregar_adicional = input("\n¿Desea agregar una excursión adicional? (si/no): ").strip().lower()
            while agregar_adicional not in ["si", "no"]:
                 print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
                 agregar_adicional = input("¿Desea agregar una excursión adicional? (si/no): ").strip().lower()
            if agregar_adicional == "si":
                excursion_adicional_elegida = seleccionar_opcion("Excursión Adicional", excursiones_adicionales, permite_ninguno=True)

        conf = input("\n¿Confirma la reserva? (si/no): ").strip().lower()
        while conf not in ["si", "no"]:
            print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
            conf = input("¿Confirma la reserva? (si/no): ").strip().lower()

        if conf == "si":
            precio_final = paquete_elegido['precio_base'] + opcion_transporte['precio'] + opcion_alojamiento['precio']
            excursion_base = paquete_elegido.get('excursion_base')
            if excursion_base and 'precio' in excursion_base:
                 precio_final += excursion_base['precio']
            if excursion_adicional_elegida:
                 precio_final += excursion_adicional_elegida['precio']

            print(f"\nSubtotal del paquete personalizado: ${precio_final:,.2f}")

            if opcion_fecha and 'nombre' in opcion_fecha and opcion_fecha['nombre'].lower() == 'alta temporada':
                precio_final *= 1.20
                print(f"Por ser '{opcion_fecha['nombre']}', se aplica un recargo del 20%.")

            print(f"PRECIO FINAL: ${precio_final:,.2f}")

            nombre_cliente = input("Ingrese su nombre completo para la reserva: ").strip()
            if not nombre_cliente:
                print("\nReserva cancelada: el nombre no puede estar vacío.")
            else:
                ticket = obtener_siguiente_ticket()
                paquete_elegido['cupo'] -= 1 
                opciones_elegidas = {
                    'transporte': opcion_transporte,
                    'alojamiento': opcion_alojamiento,
                    'excursion_adicional': excursion_adicional_elegida
                }

                registrar_reserva_en_archivo(ticket, paquete_elegido, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final)

                print(f"\n¡Reserva confirmada con éxito!")
                print(f"Su número de ticket es: {str(ticket).zfill(8)}")

                guardar_paquetes(paquetes)
        else:
            print("\nReserva no confirmada.")

        input("\nPresione Enter para volver al menú...")


def gestionar_cancelacion(paquetes):
    limpiar_consola()
    print("--- CANCELAR UNA RESERVA ---")
    try:
        ticket_a_cancelar_str = input("Ingrese el número de ticket de la reserva a cancelar (o 0 para volver): ")
        ticket_a_cancelar = int(ticket_a_cancelar_str)
        if ticket_a_cancelar == 0:
            return 
    except ValueError:
        print("Error: El ticket debe ser un número."); input("\nPresione Enter..."); return

    reservas_actualizadas = [] 
    reserva_encontrada = False
    reserva_ya_cancelada = False
    id_paquete_a_reponer = -1 

    archivo_reservas_lectura = None
    try:
        archivo_reservas_lectura = open(ARCHIVO_RESERVAS, "rt", encoding='utf-8')
        for linea in archivo_reservas_lectura:
            try:
                partes = linea.strip().split(';')
                if int(partes[0]) == ticket_a_cancelar:
                    reserva_encontrada = True
                    if partes[7].upper() == "CANCELADA":
                        reserva_ya_cancelada = True
                        reservas_actualizadas.append(linea) # 
                    else:
                        id_paquete_a_reponer = int(partes[1])
                        partes[7] = "CANCELADA" 
                        reservas_actualizadas.append(";".join(partes) + "\n") 
                else:
                    reservas_actualizadas.append(linea)
            except (ValueError, IndexError):
                reservas_actualizadas.append(linea)
    except FileNotFoundError:
        print("Aún no existen reservas para cancelar."); input("\nPresione Enter..."); return
    finally:
        if archivo_reservas_lectura: archivo_reservas_lectura.close()

    if not reserva_encontrada:
        print("Error: No se encontró ninguna reserva con ese número de ticket.")
    elif reserva_ya_cancelada:
        print("Esa reserva ya había sido cancelada anteriormente.")
    else:
        archivo_reservas_escritura = None
        try:
            archivo_reservas_escritura = open(ARCHIVO_RESERVAS, "wt", encoding='utf-8')
            archivo_reservas_escritura.writelines(reservas_actualizadas) # Escribe las líneas actualizadas

            cupo_repuesto = False
            for paquete in paquetes:
                if paquete['id'] == id_paquete_a_reponer:
                    paquete['cupo'] += 1
                    cupo_repuesto = True
                    break 

            if cupo_repuesto:
                 guardar_paquetes(paquetes)

            print(f"\n¡Reserva del ticket {str(ticket_a_cancelar).zfill(8)} cancelada con éxito!")
            if cupo_repuesto:
                print("Se ha restaurado y guardado un cupo al paquete correspondiente.")
            else:
                print("ADVERTENCIA: No se encontró el paquete original para reponer el cupo.")

        except OSError as e:
            print(f"Error al actualizar el archivo de reservas: {e}")
        finally:
            if archivo_reservas_escritura: archivo_reservas_escritura.close()

    input("\nPresione Enter para volver al menú...")

#----------------------------------------------------
#      Función que controla el menú principal
#----------------------------------------------------

def mostrar_menu_principal(paquetes):
    salir = False
    while not salir:
        limpiar_consola()
        print("--- MENÚ PRINCIPAL ---")
        print("1. Ver Paquetes Turísticos")
        print("2. Buscar Paquete por Criterios")
        print("3. Realizar una Reserva")
        print("4. Cancelar una Reserva")
        print("5. Guardar Cambios y Salir")
        opcion_str = input("Seleccione una opción: ")
        try:
            opcion = int(opcion_str)
            if opcion == 1: gestionar_vista_de_paquetes(paquetes)
            elif opcion == 2: iniciar_busqueda_recursiva(paquetes)
            elif opcion == 3: gestionar_reserva(paquetes)
            elif opcion == 4: gestionar_cancelacion(paquetes)
            elif opcion == 5:
                guardar_paquetes(paquetes)
                print("\nDatos guardados correctamente.")
                input("Presione Enter para salir...")
                salir = True 
            else:
                print("\nError: Opción no válida.")
                input("\nPresione Enter para continuar...")
        except ValueError:
            print("\nError: Por favor, ingrese solo números.")
            input("\nPresione Enter para continuar...")

#----------------------------------------------------
#        PROGRAMA PRINCIPAL
#----------------------------------------------------

salir_del_sistema = False
while not salir_del_sistema:
    limpiar_consola()
    print("--- SISTEMA DE GESTIÓN TURÍSTICA ---")
    print("1. Iniciar Sesión")
    print("2. Registrar Nuevo Usuario")
    print("3. Salir")
    opcion_inicio = input("Seleccione una opción: ")

    if opcion_inicio == '1':
        if realizar_login():
            limpiar_consola(); print("¡Acceso concedido!")
            paquetes_turisticos = cargar_paquetes() 
            if paquetes_turisticos is not None: 
                 if not paquetes_turisticos:
                      print("ADVERTENCIA: No hay paquetes definidos en el archivo.")
                 mostrar_menu_principal(paquetes_turisticos)
            else:
                 print("Error grave al cargar los paquetes. No se puede continuar.")
                 input("Presione Enter para salir.")

            salir_del_sistema = True 
        else:
            print("\nUsuario o contraseña incorrectos.")
            input("Presione Enter para continuar...")

    elif opcion_inicio == '2':
        registrar_usuario()
        input("\nPresione Enter para volver al menú de inicio...")

    elif opcion_inicio == '3':
        print("\nGracias por usar el sistema.")
        salir_del_sistema = True 

    else:
        print("\nOpción no válida. Por favor, intente de nuevo.")
        input("\nPresione Enter para continuar...") 
