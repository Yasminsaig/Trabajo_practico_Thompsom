import datetime
import os

# --- Constantes Globales ---
ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_PAQUETES = "paquetes.txt"
ARCHIVO_RESERVAS = "reservas.txt"
ARCHIVO_CONTADOR_TICKET = "contador_ticket.txt"

# --- Funciones Utilitarias (Limpieza, Tickets, Login) ---

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_siguiente_ticket():
    ultimo_ticket = 0
    f_contador_lectura = None
    try:
        f_contador_lectura = open(ARCHIVO_CONTADOR_TICKET, "r")
        contenido = f_contador_lectura.read(100) 
        if contenido:
            ultimo_ticket = int(contenido)
    except (FileNotFoundError, ValueError):
        ultimo_ticket = 0
    finally:
        if f_contador_lectura:
            f_contador_lectura.close() 

    siguiente_ticket = ultimo_ticket + 1

    f_contador_escritura = None
    try:
        f_contador_escritura = open(ARCHIVO_CONTADOR_TICKET, "w")
        f_contador_escritura.write(str(siguiente_ticket))
    except OSError:
        pass 
    finally:
        if f_contador_escritura:
            f_contador_escritura.close()

    return siguiente_ticket

def realizar_login():
    print("--- Bienvenido/a al Sistema de Paquetes Turísticos ---")
    usuario_ingresado = input("Usuario: ")
    contrasena_ingresada = input("Contraseña: ")
    acceso_concedido = False
    f_usuarios = None
    try:
        f_usuarios = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
        for linea in f_usuarios:
            try:
                usuario_archivo, contrasena_archivo = linea.strip().split(";")
                if usuario_ingresado == usuario_archivo and contrasena_ingresada == contrasena_archivo:
                    acceso_concedido = True
                    break
            except ValueError:
                continue 
    except FileNotFoundError:
        print(f"\nADVERTENCIA: No se encontró '{ARCHIVO_USUARIOS}'. Puede registrar un usuario.")
    except OSError as e: 
        print(f"\nERROR: No se pudo leer el archivo '{ARCHIVO_USUARIOS}'. {e}")
    finally:
        if f_usuarios:
            f_usuarios.close() 
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
        f_lectura = None
        try:
            f_lectura = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
            for linea in f_lectura:
                try:
                    if linea.strip().split(';')[0].lower() == nuevo_usuario.lower():
                        usuario_existe = True
                        break
                except (ValueError, IndexError):
                    continue 
        except FileNotFoundError:
            pass 
        finally:
            if f_lectura:
                f_lectura.close() 

        if usuario_existe:
            print("Error: Ese nombre de usuario ya está en uso.")
        else:
            usuario_valido = True

    nueva_contrasena = input("Ingrese su nueva contraseña: ")
    f_escritura = None
    try:
        f_escritura = open(ARCHIVO_USUARIOS, "at", encoding='utf-8')
        f_escritura.write(f"{nuevo_usuario};{nueva_contrasena}\n") 
        print("\n¡Usuario registrado con éxito!")
    except OSError as e:
        print(f"\nERROR: No se pudo registrar el usuario. {e}")
    finally:
        if f_escritura:
            f_escritura.close() 

# --- Funciones de Lógica de Paquetes ---

def modificar_cupo_paquete_en_archivo(id_paquete_modificar, cantidad_a_sumar):
    """
    (Escritura Eficiente - Clase 9, Ejemplo 5)
    Modifica el cupo de un paquete directamente en paquetes.txt
    usando la técnica de archivo temporal.
    Devuelve True si tuvo éxito, False si no.
    """
    f_lectura = None
    f_escritura = None
    paquete_encontrado = False
    archivo_temporal_nombre = "paquetes_temp.txt" 

    try:
        f_lectura = open(ARCHIVO_PAQUETES, "rt", encoding='utf-8')
        f_escritura = open(archivo_temporal_nombre, "wt", encoding='utf-8')

        linea = f_lectura.readline()
        while linea:
            linea_stripped = linea.strip()
            f_escritura.write(linea) 

            if linea_stripped and linea_stripped[0:8] == "#PAQUETE":
                linea_datos = f_lectura.readline()
                if not linea_datos:
                    break 

                try:
                    partes = linea_datos.strip().split(';')
                    id_actual = int(partes[0])

                    if id_actual == id_paquete_modificar:
                        paquete_encontrado = True
                        cupo_actual = int(partes[5])
                        nuevo_cupo = cupo_actual + cantidad_a_sumar
                        partes[5] = str(nuevo_cupo) 
                        
                        linea_datos_modificada = ";".join(partes) + "\n"
                        f_escritura.write(linea_datos_modificada)
                    else:
                        f_escritura.write(linea_datos)
                
                except (ValueError, IndexError):
                    f_escritura.write(linea_datos)
            
            linea = f_lectura.readline() 

    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo '{ARCHIVO_PAQUETES}'.")
        return False 
    except OSError as e:
        print(f"ERROR: No se pudo leer/escribir archivo de paquetes. {e}")
        return False 
    finally:
        if f_lectura: f_lectura.close()
        if f_escritura: f_escritura.close()

    if paquete_encontrado:
        f_lectura_temp = None
        f_escritura_orig = None
        try:
            f_lectura_temp = open(archivo_temporal_nombre, "rt", encoding='utf-8')
            f_escritura_orig = open(ARCHIVO_PAQUETES, "wt", encoding='utf-8')
            for linea_temp in f_lectura_temp:
                f_escritura_orig.write(linea_temp)
        except OSError as e:
            print(f"ERROR: No se pudo sobreescribir '{ARCHIVO_PAQUETES}'. {e}")
            return False 
        finally:
            if f_lectura_temp: f_lectura_temp.close()
            if f_escritura_orig: f_escritura_orig.close()
            try: os.remove(archivo_temporal_nombre) 
            except OSError: pass
        return True
    else:
        print(f"ADVERTENCIA: No se encontró el paquete ID {id_paquete_modificar} para actualizar cupo.")
        try: os.remove(archivo_temporal_nombre) 
        except OSError: pass
        return False

def _parsear_paquete_desde_linea(f_paquetes, linea_datos_leida):
    """
    (Función Unificada - Clase 2)
    Función ÚNICA de parseo. Recibe la línea de datos (ej: 1;Chubut;...)
    y el manejador del archivo, y parsea el resto del paquete.
    Devuelve (paquete_actual, proxima_linea)
    """
    paquete_actual = {}
    try:
        partes = linea_datos_leida.strip().split(";")
        id_str, prov, dest, dur, precio_str, cupo_str = partes
        paquete_actual["id"] = int(id_str); paquete_actual["provincia"] = prov
        paquete_actual["destino"] = dest; paquete_actual["duracion"] = dur
        paquete_actual["precio_base"] = float(precio_str); paquete_actual["cupo"] = int(cupo_str)
    except (ValueError, IndexError, TypeError) as e:
        print(f"ADVERTENCIA: Se omitió un paquete con cabecera corrupta. Error: {e}")
        return None, f_paquetes.readline() 

    seccion_actual = ""
    linea = f_paquetes.readline()
    while linea:
        linea_stripped = linea.strip()
        if len(linea_stripped) > 0:
            if len(linea_stripped) >= 12 and linea_stripped[0:12] == "#FIN_PAQUETE":
                return paquete_actual, f_paquetes.readline() 
            elif linea_stripped[0] == "#":
                seccion_actual = linea_stripped[1:].lower()
                if seccion_actual not in ["excursion_base", "paquete"]:
                    paquete_actual[seccion_actual] = []
            elif seccion_actual != "":
                try:
                    partes = linea_stripped.split(";")
                    if seccion_actual == "transporte" or seccion_actual == "alojamiento":
                        nombre = partes[0]; precio = float(partes[1]); desc = partes[2] if len(partes) > 2 else ""
                        paquete_actual[seccion_actual].append({"nombre": nombre, "precio": precio, "desc": desc})
                    elif seccion_actual == "excursion_base":
                        paquete_actual[seccion_actual] = {"nombre": partes[0], "precio": float(partes[1])}
                    elif seccion_actual == "excursiones_adicionales":
                        paquete_actual[seccion_actual].append({"nombre": partes[0], "precio": float(partes[1])})
                    elif seccion_actual == "fechas":
                        paquete_actual[seccion_actual].append({"nombre": partes[0], "fecha": partes[1]})
                except (ValueError, IndexError, TypeError) as e:
                    print(f"ADVERTENCIA: Se omitió una línea corrupta en la sección '{seccion_actual}'. Error: {e}")
        linea = f_paquetes.readline()
        
    return paquete_actual, "" 

def _obtener_provincias_unicas():
    """
    (Vuelta 1 - Eficiente, Clase 9)
    Lee paquetes.txt para obtener una lista de provincias únicas.
    Usa un 'set' (Clase 7) para evitar duplicados.
    """
    provincias = set()
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        linea = f_paquetes.readline()
        while linea:
            if linea.strip() and linea.strip()[0:8] == "#PAQUETE":
                linea_datos = f_paquetes.readline()
                if not linea_datos:
                    break
                try:
                    provincia = linea_datos.strip().split(';')[1]
                    provincias.add(provincia)
                except (IndexError, TypeError):
                    print("ADVERTENCIA: Se omitió un paquete con formato incorrecto.")
            linea = f_paquetes.readline()
    except FileNotFoundError:
        print(f"ERROR: No se encontró '{ARCHIVO_PAQUETES}'.")
    except OSError as e:
        print(f"ERROR: No se pudo leer '{ARCHIVO_PAQUETES}'. {e}")
    finally:
        if f_paquetes:
            f_paquetes.close()
            
    return list(provincias)

def _obtener_paquetes_de_provincia(provincia_buscada):
    """
    (Vuelta 2 - Eficiente, Clase 9)
    Lee paquetes.txt y carga en memoria SOLAMENTE los paquetes
    que coinciden con la provincia buscada.
    """
    paquetes_encontrados = []
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        linea = f_paquetes.readline()
        while linea:
            if linea.strip() and linea.strip()[0:8] == "#PAQUETE":
                linea_datos = f_paquetes.readline()
                if not linea_datos:
                    break
                
                paquete_parseado = None
                try:
                    if linea_datos.strip().split(';')[1] == provincia_buscada:
                        paquete_parseado, proxima_linea = _parsear_paquete_desde_linea(f_paquetes, linea_datos)
                        if paquete_parseado:
                            paquetes_encontrados.append(paquete_parseado)
                        linea = proxima_linea 
                        continue 
                
                except (IndexError, TypeError):
                    print("ADVERTENCIA: Se omitió un paquete con formato incorrecto.")
            
            linea = f_paquetes.readline()
            
    except FileNotFoundError:
        print(f"ERROR: No se encontró '{ARCHIVO_PAQUETES}'.")
    except OSError as e:
        print(f"ERROR: No se pudo leer '{ARCHIVO_PAQUETES}'. {e}")
    finally:
        if f_paquetes:
            f_paquetes.close()
            
    return paquetes_encontrados

def _seleccionar_paquete_interactivo():
    
    provincias = _obtener_provincias_unicas()
    
    if not provincias:
        print("\nNo hay paquetes cargados.");
        return None

    while True: 
        limpiar_consola()
        print("--- SELECCIÓN DE PAQUETE (Paso 1: Provincia) ---")
        for i, prov in enumerate(provincias):
            print(f"   {i+1}. {prov}")
        print("\n   0. Volver al Menú Principal")

        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                return None 

            if 1 <= nro_prov <= len(provincias):
                provincia_elegida = provincias[nro_prov - 1]
                
                paquetes_de_provincia = _obtener_paquetes_de_provincia(provincia_elegida)
                
                if not paquetes_de_provincia:
                    print(f"\nNo se encontraron paquetes para {provincia_elegida}.")
                    input("Presione Enter...")
                    continue 

                while True: 
                    limpiar_consola()
                    print(f"--- SELECCIÓN DE PAQUETE (Paso 2: Paquete en {provincia_elegida.upper()}) ---")
                    for i, p in enumerate(paquetes_de_provincia):
                        print(f"   {i+1}. {p['destino']} (Cupo: {p['cupo']})")
                    print("\n   0. Volver a Provincias")

                    nro_paq_str = input("\nSeleccione el Nro del Paquete: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            break 

                        if 1 <= nro_paq <= len(paquetes_de_provincia):
                            return paquetes_de_provincia[nro_paq - 1] 
                        else:
                            print("Error: Número de paquete no válido."); input("...")
                    except ValueError:
                         print("Error: Ingrese un número."); input("...")
            else:
                print("Error: Número de provincia no válido."); input("...")
        except ValueError:
            print("Error: Ingrese un número."); input("...")

# --- Funciones de Lógica de Reservas ---

def registrar_reserva_en_archivo(ticket, paquete, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final):
    f_reservas = None
    try:
        f_reservas = open(ARCHIVO_RESERVAS, "at", encoding='utf-8') 
        fecha_hoy = datetime.date.today()
        fecha_reserva = f"{fecha_hoy.day}/{fecha_hoy.month}/{fecha_hoy.year}" 

        detalles = f"Transporte: {opciones_elegidas['transporte']['nombre']} | Alojamiento: {opciones_elegidas['alojamiento']['nombre']}"
        lista_excursiones = opciones_elegidas.get('excursiones_adicionales')
        if lista_excursiones:
            nombres_excursiones = ", ".join([exc['nombre'] for exc in lista_excursiones])
            detalles += f" | Extras: [{nombres_excursiones}]"

        fecha_nombre = opcion_fecha['nombre'] if opcion_fecha and 'nombre' in opcion_fecha else 'N/A'

        linea = f"{ticket};{paquete['id']};{paquete['destino']};{nombre_cliente};{fecha_reserva};{fecha_nombre};{precio_final:.2f};ACTIVA;{detalles}\n"
        f_reservas.write(linea) 
    except OSError as e: 
        print(f"\nERROR: No se pudo guardar la reserva. {e}")
    finally:
        if f_reservas: f_reservas.close() 

def normalizar_cadena_simple(cadena):
    cadena = cadena.lower() 
    reemplazos = { 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u' }
    for acentuada, sin_acento in reemplazos.items():
        cadena = cadena.replace(acentuada, sin_acento) 
    return cadena

def cumple_filtros(paquete, filtros):
    if 'texto_buscar' in filtros and filtros['texto_buscar']:
        texto_a_buscar_normalizado = normalizar_cadena_simple(filtros['texto_buscar'])
        destino_normalizado = normalizar_cadena_simple(paquete['destino'])
        provincia_normalizada = normalizar_cadena_simple(paquete['provincia'])
        if texto_a_buscar_normalizado not in destino_normalizado and \
           texto_a_buscar_normalizado not in provincia_normalizada:
            return False
    if 'precio_max' in filtros and paquete['precio_base'] > filtros['precio_max']:
        return False
    return True

def seleccionar_opcion(nombre_seccion, lista_opciones, permite_ninguno=False):
    opcion_valida = False
    opcion_seleccionada = None
    if not lista_opciones:
        print(f"No hay opciones disponibles para {nombre_seccion}.")
        return None
    
    print(f"\n--- Opciones de {nombre_seccion} ---")
    for i, opcion in enumerate(lista_opciones):
        print(f"   {i+1}. {opcion.get('nombre', opcion)}", end="")
        if 'precio' in opcion:
             print(f" (+${opcion['precio']:.2f})")
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

def seleccionar_multiples_opciones(nombre_seccion, lista_opciones):
    opciones_seleccionadas = []
    opciones_disponibles = list(lista_opciones) 
    if not opciones_disponibles:
        print(f"No hay opciones disponibles para {nombre_seccion}.")
        return opciones_seleccionadas 
    
    print(f"\n--- Opciones de {nombre_seccion} (Puede elegir varias) ---")
    while True:
        print(f"\n--- Seleccione {nombre_seccion} ---")
        if not opciones_disponibles:
            print("No quedan más opciones por agregar.")
            break
        for i, opcion in enumerate(opciones_disponibles):
            print(f"   {i+1}. {opcion.get('nombre', opcion)} (+${opcion['precio']:.2f})")
        print("\n   0. Terminar selección de excursiones")
        try:
            prompt = f"Seleccione Nro de {nombre_seccion} para AGREGAR (1-{len(opciones_disponibles)}) o 0 para terminar: "
            opcion_num_str = input(prompt)
            opcion_num = int(opcion_num_str)
            if opcion_num == 0:
                break 
            elif 1 <= opcion_num <= len(opciones_disponibles):
                opcion_elegida = opciones_disponibles.pop(opcion_num - 1) 
                opciones_seleccionadas.append(opcion_elegida)
                print(f"'{opcion_elegida['nombre']}' agregada.")
            else:
                print("Error: Número fuera de rango.")
        except ValueError:
            print("Error: Ingrese un número válido.")
            
    print("\nExcursiones seleccionadas:")
    if not opciones_seleccionadas:
        print(" - Ninguna")
    else:
        for excursion in opciones_seleccionadas:
            print(f" - {excursion['nombre']} (+${excursion['precio']:.2f})")
    return opciones_seleccionadas

def mostrar_detalles_paquete(paquete):
    limpiar_consola()
    print("=" * 70)
    print(f"DETALLES DEL PAQUETE ID: {paquete['id']} - {paquete['destino']}, {paquete['provincia']}")
    print(f"Duración: {paquete['duracion']} | Cupo actual: {paquete['cupo']}")
    print(f"Precio Base: ${paquete['precio_base']:.2f}")
    for seccion, titulo in [('transporte', 'Transporte'), ('alojamiento', 'Alojamiento')]:
        if paquete.get(seccion):
            print(f"\n--- Opciones de {titulo} ---")
            for i, opcion in enumerate(paquete[seccion]):
                print(f"   {i+1}. {opcion['nombre']} (+${opcion['precio']:.2f})")
                if opcion.get('desc'):
                    print(f"     Descripción: {opcion['desc']}")
    if paquete.get('fechas'):
        print("\n--- Fechas ---")
        for i, opcion in enumerate(paquete['fechas']):
            print(f"   {i+1}. {opcion['nombre']}: {opcion['fecha']}")
    excursion_base = paquete.get('excursion_base')
    if excursion_base and 'nombre' in excursion_base and 'precio' in excursion_base:
        print(f"\n--- Excursión Incluida ---")
        print(f"   - {excursion_base['nombre']} (+${excursion_base['precio']:.2f})")
    excursiones_adicionales = paquete.get('excursiones_adicionales')
    if excursiones_adicionales:
        print("\n--- Excursiones Adicionales (Opcionales) ---")
        for i, opcion in enumerate(excursiones_adicionales):
            print(f"   {i+1}. {opcion['nombre']} (+${opcion['precio']:.2f})")
    print("=" * 70)

# --- Funciones de Menú Principal (Opciones 1-5) ---

def gestionar_vista_de_paquetes(): 
    """ (Opción 1) Llama al selector interactivo y solo muestra detalles. """
    
    print("Cargando paquetes...")
    paquete_elegido = _seleccionar_paquete_interactivo()
    
    if paquete_elegido:
        mostrar_detalles_paquete(paquete_elegido)
        input("\nPresione Enter para volver al menú...")

def buscar_recursivo_interactivo(f_paquetes, filtros, linea_actual):
    """ (Motor de la Opción 2) Función recursiva (Clase 10). """
    
    # Caso base: fin de archivo
    while linea_actual and not (linea_actual.strip() and linea_actual.strip()[0:8] == "#PAQUETE"):
        linea_actual = f_paquetes.readline()

    if not linea_actual:
        print("\n--- No se encontraron más resultados. ---")
        return 
    
    linea_datos = f_paquetes.readline()
    if not linea_datos:
        buscar_recursivo_interactivo(f_paquetes, filtros, "") 
        return
        
    paquete_actual, proxima_linea = _parsear_paquete_desde_linea(f_paquetes, linea_datos)
    
    if paquete_actual and cumple_filtros(paquete_actual, filtros):
        print("\n--- Paquete Encontrado ---")
        print(f"ID: {paquete_actual['id']} - {paquete_actual['destino']}, {paquete_actual['provincia']}")
        print(f"Precio Base: ${paquete_actual['precio_base']:.2f} | Cupo: {paquete_actual['cupo']}")
        
        continuar = input("¿Desea buscar el siguiente? (si/no): ").lower().strip()
        
        if continuar in ["s", "si", "sí"]:
            # Llamada recursiva (Clase 10)
            buscar_recursivo_interactivo(f_paquetes, filtros, proxima_linea)
        else:
            return 
    else:
        # Llamada recursiva (Clase 10)
        buscar_recursivo_interactivo(f_paquetes, filtros, proxima_linea)

def iniciar_busqueda_recursiva(): 
    """ (Opción 2) Pide filtros y lanza la búsqueda recursiva. """
    
    limpiar_consola()
    print("--- BÚSQUEDA DE PAQUETES ---"); print("Ingrese al menos un criterio. Ingrese 0 si no desea filtrar por ese criterio.")
    filtros = {}

    texto_filtro = input("Ingrese Destino o Provincia a buscar: ").strip()
    if texto_filtro:
        filtros['texto_buscar'] = texto_filtro

    try:
        precio_max_str = input("Ingrese precio máximo base (o 0 para no filtrar): ").strip()
        if precio_max_str:
            precio_max = float(precio_max_str)
            if precio_max > 0: filtros['precio_max'] = precio_max
    except ValueError:
        print("Precio máximo inválido, no se filtrará por precio.")

    if not filtros:
        print("\nError: Debe ingresar al menos un criterio de búsqueda.")
        input("\nPresione Enter para volver al menú...")
        return
    
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        primera_linea = f_paquetes.readline() 
        buscar_recursivo_interactivo(f_paquetes, filtros, primera_linea)
    except FileNotFoundError as mensaje:
        print(f"No se puede abrir el archivo: {mensaje}")
    except OSError as mensaje:
        print(f"No se puede leer el archivo: {mensaje}")
    finally:
        if f_paquetes:
            f_paquetes.close() 
    
    input("\nPresione Enter para volver al menú...")

def gestionar_reserva(): 
    """ (Opción 3) Llama al selector y luego procesa la reserva. """

    print("Cargando paquetes...")
    paquete_elegido = _seleccionar_paquete_interactivo()

    if not paquete_elegido:
        return 

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
    excursiones_adicionales_elegidas = [] 
    excursiones_adicionales = paquete_elegido.get('excursiones_adicionales')
    
    if excursiones_adicionales:
        agregar_adicional = input("\n¿Desea agregar excursiones adicionales? (si/no): ").strip().lower()
        while agregar_adicional not in ["si", "no"]:
             print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
             agregar_adicional = input("¿Desea agregar excursiones adicionales? (si/no): ").strip().lower()
        if agregar_adicional == "si":
            excursiones_adicionales_elegidas = seleccionar_multiples_opciones("Excursión Adicional", excursiones_adicionales)

    conf = input("\n¿Confirma la reserva? (si/no): ").strip().lower()
    while conf not in ["si", "no"]:
        print("Respuesta no válida. Por favor, ingrese 'si' o 'no'.")
        conf = input("¿Confirma la reserva? (si/no): ").strip().lower()

    if conf == "si":
        precio_final = paquete_elegido['precio_base'] + opcion_transporte['precio'] + opcion_alojamiento['precio']
        excursion_base = paquete_elegido.get('excursion_base')
        if excursion_base and 'precio' in excursion_base:
             precio_final += excursion_base['precio']
        if excursiones_adicionales_elegidas:
            for excursion in excursiones_adicionales_elegidas:
                precio_final += excursion['precio']

        print(f"\nSubtotal del paquete personalizado: ${precio_final:.2f}")

        if opcion_fecha and 'nombre' in opcion_fecha and opcion_fecha['nombre'].lower() == 'alta temporada':
            precio_final *= 1.20
            print(f"Por ser '{opcion_fecha['nombre']}', se aplica un recargo del 20%.")

        print(f"PRECIO FINAL: ${precio_final:.2f}")

        nombre_cliente = input("Ingrese su nombre completo para la reserva: ").strip()
        if not nombre_cliente:
            print("\nReserva cancelada: el nombre no puede estar vacío.")
        else:
            ticket = obtener_siguiente_ticket()
            opciones_elegidas = {
                'transporte': opcion_transporte,
                'alojamiento': opcion_alojamiento,
                'excursiones_adicionales': excursiones_adicionales_elegidas
            }
            registrar_reserva_en_archivo(ticket, paquete_elegido, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final)
            print(f"\n¡Reserva confirmada con éxito!")
            print(f"Su número de ticket es: {ticket:08d}")
            
            if modificar_cupo_paquete_en_archivo(paquete_elegido['id'], -1):
                print("Se ha descontado un cupo del paquete.")
            else:
                print("ADVERTENCIA: No se pudo actualizar el cupo en el archivo.")
    else:
        print("\nReserva no confirmada.")

    input("\nPresione Enter para volver al menú...")

def gestionar_cancelacion(): 
    """ (Opción 4) Lee 'reservas.txt' eficientemente. """
    
    print("--- CANCELAR UNA RESERVA ---")
    
    if not os.path.exists(ARCHIVO_RESERVAS):
       print("Aún no existen reservas para cancelar.") 
       input("\nPresione Enter..."); return 

    try:
        ticket_a_cancelar_str = input("Ingrese el número de ticket de la reserva a cancelar (o 0 para volver): ") 
        ticket_a_cancelar = int(ticket_a_cancelar_str)
        if ticket_a_cancelar == 0:
            return
    except ValueError:
        print("Error: El ticket debe ser un número."); input("\nPresione Enter..."); return 

    f_lectura = None
    f_escritura = None
    reserva_encontrada = False
    reserva_ya_cancelada = False
    id_paquete_a_reponer = -1
    
    archivo_temporal_nombre = "reservas_temp.txt" 

    try:
        f_lectura = open(ARCHIVO_RESERVAS, "rt", encoding='utf-8')
        f_escritura = open(archivo_temporal_nombre, "wt", encoding='utf-8')

        for linea in f_lectura:
            try:
                partes = linea.strip().split(';')
                ticket_actual = int(partes[0])
                if ticket_actual == ticket_a_cancelar:
                    reserva_encontrada = True
                    if partes[7].upper() == "CANCELADA":
                        reserva_ya_cancelada = True
                        f_escritura.write(linea) 
                    else:
                        partes[7] = "CANCELADA" 
                        id_paquete_a_reponer = int(partes[1])
                        linea_modificada = ";".join(partes) + "\n"
                        f_escritura.write(linea_modificada)
                else:
                    f_escritura.write(linea) 
            except (ValueError, IndexError):
                f_escritura.write(linea) 
    
    except FileNotFoundError:
        print("Aún no existen reservas para cancelar."); input("\nPresione Enter..."); return 
    except OSError as e:
        print(f"Error al leer el archivo de reservas: {e}"); input("\nPresione Enter..."); return 
    finally:
        if f_lectura: f_lectura.close()
        if f_escritura: f_escritura.close()

    if reserva_encontrada and not reserva_ya_cancelada:
        cupo_repuesto = modificar_cupo_paquete_en_archivo(id_paquete_a_reponer, 1)

        f_lectura_temp = None
        f_escritura_orig = None
        try:
            f_lectura_temp = open(archivo_temporal_nombre, "rt", encoding='utf-8')
            f_escritura_orig = open(ARCHIVO_RESERVAS, "wt", encoding='utf-8')
            for linea in f_lectura_temp:
                f_escritura_orig.write(linea)
            print(f"\n¡Reserva del ticket {ticket_a_cancelar:08d} cancelada con éxito!")
            if cupo_repuesto:
                print("Se ha restaurado y guardado un cupo al paquete correspondiente.")
            else:
                print("ADVERTENCIA: No se pudo reponer el cupo al paquete (pudo ser borrado o hubo un error al cargar).")
        except OSError as e:
            print(f"Error al guardar los cambios en el archivo de reservas: {e}")
        finally:
            if f_lectura_temp: f_lectura_temp.close()
            if f_escritura_orig: f_escritura_orig.close()
            
        try: os.remove(archivo_temporal_nombre) 
        except OSError: pass
    
    elif not reserva_encontrada:
        print("Error: No se encontró ninguna reserva con ese número de ticket.")
        try: os.remove(archivo_temporal_nombre) 
        except OSError: pass
    elif reserva_ya_cancelada:
        print("Esa reserva ya había sido cancelada anteriormente.")
        try: os.remove(archivo_temporal_nombre) 
        except OSError: pass

    input("\nPresione Enter para volver al menú...")

def solicitar_opcion_menu_recursivo():
    """ (Función Recursiva - Clase 10) """
    
    opcion_str = input("Seleccione una opción: ")
    
    try:
        opcion_num = int(opcion_str) 
        
        if 1 <= opcion_num <= 5:
            return opcion_num # Caso Base
        else:
            print("\nError: Opción no válida (debe ser entre 1 y 5).")
            input("\nPresione Enter para continuar...")
            return solicitar_opcion_menu_recursivo() # Llamada Recursiva
            
    except ValueError:
        print("\nError: Por favor, ingrese solo números.")
        input("\nPresione Enter para continuar...")
        return solicitar_opcion_menu_recursivo() # Llamada Recursiva

def mostrar_menu_principal(): 
    
    # --- Matriz de Opciones  ---
    opciones_matriz = [
        [1, "Ver Paquetes Turísticos"],
        [2, "Buscar Paquete por Criterios"],
        [3, "Realizar una Reserva"],
        [4, "Cancelar una Reserva"],
        [5, "Salir"] 
    ]
    
    salir = False
    while not salir:
        limpiar_consola()
        print("--- MENÚ PRINCIPAL ---")
        
        for fila in opciones_matriz:
            numero_opcion = fila[0]
            texto_opcion = fila[1]
            print(f"{numero_opcion}. {texto_opcion}")
        
        opcion = solicitar_opcion_menu_recursivo() 

        if opcion == 1: gestionar_vista_de_paquetes() 
        elif opcion == 2: iniciar_busqueda_recursiva() 
        elif opcion == 3: gestionar_reserva() 
        elif opcion == 4: gestionar_cancelacion() 
        elif opcion == 5:
            print("\nGracias por usar el sistema.")
            input("Presione Enter para salir...")
            salir = True

# --- Programa Principal ---

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
            mostrar_menu_principal() 
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


