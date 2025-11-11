import datetime
import os

ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_PAQUETES = "paquetes.txt"
ARCHIVO_RESERVAS = "reservas.txt"
ARCHIVO_CONTADOR_TICKET = "contador_ticket.txt"

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
    print("--- Bienvenido/a al Sistema de Paquetes Turisticos ---")
    usuario_ingresado = input("Usuario: ")
    contrasena_ingresada = input("Contrasena: ")
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
        print(f"\nADVERTENCIA: No se encontro '{ARCHIVO_USUARIOS}'. Puede registrar un usuario.")
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
            print("Error: El nombre de usuario no puede estar vacio.")
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
            print("Error: Ese nombre de usuario ya esta en uso.")
        else:
            usuario_valido = True

    nueva_contrasena = input("Ingrese su nueva contrasena: ")
    f_escritura = None
    try:
        f_escritura = open(ARCHIVO_USUARIOS, "at", encoding='utf-8')
        f_escritura.write(f"{nuevo_usuario};{nueva_contrasena}\n")
        print("\nUsuario registrado con exito!")
    except OSError as e:
        print(f"\nERROR: No se pudo registrar el usuario. {e}")
    finally:
        if f_escritura:
            f_escritura.close()

def contar_paquetes():
    contador = 0
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        for linea in f_paquetes:
            if linea.strip() == "#PAQUETE":
                contador = contador + 1
    except FileNotFoundError:
        pass
    except OSError:
        pass
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    return contador

def cargar_matriz_cupos():
    cantidad_paquetes = contar_paquetes()
    
    if cantidad_paquetes == 0:
        return []
    
    # CREA MATRIZ REGULAR
    matriz = [[0] * 2 for i in range(cantidad_paquetes)]
    
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        indice_fila = 0
        leyendo_primera_linea = False
        
        for linea in f_paquetes:
            linea = linea.strip()
            
            if linea == "#PAQUETE":
                leyendo_primera_linea = True
                continue
            
            if leyendo_primera_linea and linea != "" and linea[0] != "#":
                partes = linea.split(";")
                matriz[indice_fila][0] = int(partes[0])  # id
                matriz[indice_fila][1] = int(partes[5])  # cupo
                indice_fila = indice_fila + 1
                leyendo_primera_linea = False
        
        print("Matriz de cupos cargada correctamente.")
        
    except FileNotFoundError:
        print("No se encontro el archivo de paquetes.")
    except (ValueError, IndexError) as e:
        print(f"Error de formato en archivo: {e}")
    except OSError as e:
        print(f"Error al leer archivo: {e}")
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    
    return matriz

def obtener_cupo_de_matriz(matriz_cupos, id_paquete):
    filas = len(matriz_cupos)
    for f in range(filas):
        if matriz_cupos[f][0] == id_paquete:
            return matriz_cupos[f][1]
    return 0

def actualizar_cupo_en_matriz(matriz_cupos, id_paquete, incremento):
    filas = len(matriz_cupos)
    for f in range(filas):
        if matriz_cupos[f][0] == id_paquete:
            matriz_cupos[f][1] = matriz_cupos[f][1] + incremento
            return True
    return False

def guardar_cupos_en_archivo(matriz_cupos):

    dict_cupos = {}
    filas = len(matriz_cupos)
    for f in range(filas):
        dict_cupos[matriz_cupos[f][0]] = matriz_cupos[f][1]
    
    # Archivo temporal
    nombre_temp = "temp_paquetes.txt"
    
    f_lectura = None
    f_escritura = None
    
    try:
        f_lectura = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        f_escritura = open(nombre_temp, "wt", encoding="utf-8")
        
        leyendo_primera_linea = False
        
        for linea in f_lectura:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera_linea = True
                f_escritura.write(linea)
                continue
            
            if leyendo_primera_linea and linea_strip != "" and linea_strip[0] != "#":
                partes = linea_strip.split(";")
                id_paq = int(partes[0])
                
                if id_paq in dict_cupos:
                    partes[5] = str(dict_cupos[id_paq])
                    linea_modificada = ";".join(partes) + "\n"
                    f_escritura.write(linea_modificada)
                else:
                    f_escritura.write(linea)
                
                leyendo_primera_linea = False
            else:
                f_escritura.write(linea)
        
        f_lectura.close()
        f_escritura.close()
        
        # Reemplazar archivo original
        f_lectura = open(nombre_temp, "rt", encoding="utf-8")
        f_escritura = open(ARCHIVO_PAQUETES, "wt", encoding="utf-8")
        
        for linea in f_lectura:
            f_escritura.write(linea)
        
        print("Cupos actualizados correctamente.")
        
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as e:
        print(f"Error: {e}")
    finally:
        try:
            f_lectura.close()
        except:
            pass
        try:
            f_escritura.close()
        except:
            pass

def mostrar_provincias_interactivo():
    f_paquetes = None
    provincias_vistas = []
    
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        leyendo_primera_linea = False
        
        for linea in f_paquetes:
            linea = linea.strip()
            
            if linea == "#PAQUETE":
                leyendo_primera_linea = True
                continue
            
            if leyendo_primera_linea and linea != "" and linea[0] != "#":
                provincia = linea.split(";")[1]
                
                if provincia not in provincias_vistas:
                    provincias_vistas.append(provincia)
                
                leyendo_primera_linea = False
        
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as e:
        print(f"Error: {e}")
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    
    return provincias_vistas

def mostrar_destinos_provincia_interactivo(provincia_buscada):
    f_paquetes = None
    destinos = []
    
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        leyendo_primera_linea = False
        
        for linea in f_paquetes:
            linea = linea.strip()
            
            if linea == "#PAQUETE":
                leyendo_primera_linea = True
                continue
            
            if leyendo_primera_linea and linea != "" and linea[0] != "#":
                partes = linea.split(";")
                provincia = partes[1]
                
                if provincia.lower() == provincia_buscada.lower():
                    destinos.append([int(partes[0]), partes[2]])
                
                leyendo_primera_linea = False
        
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as e:
        print(f"Error: {e}")
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    
    return destinos

def cargar_paquete_completo_por_id(id_buscado):
    paquete = None
    f_paquetes = None
    
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        linea = f_paquetes.readline()
        seccion_actual = ""
        
        while linea:
            linea = linea.strip()
            
            if len(linea) > 0:
                if len(linea) >= 8 and linea[0:8] == "#PAQUETE":
                    if paquete:
                        break
                    paquete = {}
                    seccion_actual = "paquete"
                
                elif len(linea) >= 12 and linea[0:12] == "#FIN_PAQUETE":
                    if paquete and paquete.get('id') == id_buscado:
                        break
                    paquete = None
                    seccion_actual = ""
                
                elif linea[0] == "#" and paquete is not None:
                    seccion_actual = linea[1:].lower()
                    if seccion_actual not in ["excursion_base", "paquete"]:
                        paquete[seccion_actual] = []
                
                elif seccion_actual != "" and paquete is not None:
                    partes = linea.split(";")
                    
                    if seccion_actual == "paquete":
                        id_str, prov, dest, dur, precio_str, cupo_str = partes
                        id_paq = int(id_str)
                        
                        if id_paq != id_buscado:
                            paquete = None
                            seccion_actual = ""
                            linea = f_paquetes.readline()
                            continue
                        
                        paquete["id"] = id_paq
                        paquete["provincia"] = prov
                        paquete["destino"] = dest
                        paquete["duracion"] = dur
                        paquete["precio_base"] = float(precio_str)
                        paquete["cupo"] = int(cupo_str)
                    
                    elif seccion_actual == "transporte" or seccion_actual == "alojamiento":
                        nombre = partes[0]
                        precio = float(partes[1])
                        if len(partes) > 2:
                            desc = partes[2]
                        else:
                            desc = ""
                        paquete[seccion_actual].append(
                            {"nombre": nombre, "precio": precio, "desc": desc}
                        )
                    
                    elif seccion_actual == "excursion_base":
                        nombre, precio = partes[0], float(partes[1])
                        paquete[seccion_actual] = {"nombre": nombre, "precio": precio}
                    
                    elif seccion_actual == "excursiones_adicionales":
                        nombre, precio = partes[0], float(partes[1])
                        paquete[seccion_actual].append({"nombre": nombre, "precio": precio})
                    
                    elif seccion_actual == "fechas":
                        nombre_fecha, valor_fecha = partes[0], partes[1]
                        paquete[seccion_actual].append({"nombre": nombre_fecha, "fecha": valor_fecha})
            
            linea = f_paquetes.readline()
        
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except (ValueError, IndexError) as e:
        print(f"Error de formato: {e}")
    except OSError as e:
        print(f"Error: {e}")
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    
    return paquete

def normalizar_cadena_simple(cadena):
    cadena = cadena.lower()
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    }
    for acentuada, sin_acento in reemplazos.items():
        cadena = cadena.replace(acentuada, sin_acento)
    return cadena

def cumple_filtros_busqueda(paquete_basico, filtros):
    if 'texto_buscar' in filtros and filtros['texto_buscar']:
        texto_normalizado = normalizar_cadena_simple(filtros['texto_buscar'])
        destino_normalizado = normalizar_cadena_simple(paquete_basico['destino'])
        provincia_normalizada = normalizar_cadena_simple(paquete_basico['provincia'])
        
        if texto_normalizado not in destino_normalizado and texto_normalizado not in provincia_normalizada:
            return False
    
    if 'precio_max' in filtros and paquete_basico['precio_base'] > filtros['precio_max']:
        return False
    
    return True

def buscar_recursivo_en_archivo(archivo, filtros, estado):
    linea = archivo.readline()
    
    if not linea:
        if not estado['encontrado']:
            print("\n--- No se encontraron mas resultados. ---")
        return
    
    linea = linea.strip()
    
    if linea == "#PAQUETE":
        estado['leyendo_primera'] = True
        buscar_recursivo_en_archivo(archivo, filtros, estado)
        return
    
    if estado['leyendo_primera'] and linea != "" and linea[0] != "#":
        partes = linea.split(";")
        paquete_basico = {
            'id': int(partes[0]),
            'provincia': partes[1],
            'destino': partes[2],
            'precio_base': float(partes[4]),
            'cupo': int(partes[5])
        }
        
        if cumple_filtros_busqueda(paquete_basico, filtros):
            print("\n--- Paquete Encontrado ---")
            print(f"ID: {paquete_basico['id']} - {paquete_basico['destino']}, {paquete_basico['provincia']}")
            print(f"Precio Base: ${paquete_basico['precio_base']:.2f} | Cupo: {paquete_basico['cupo']}")
            
            estado['encontrado'] = True
            continuar = input("Desea buscar el siguiente? (s/n): ").lower().strip()
            
            if continuar != "s":
                return
        
        estado['leyendo_primera'] = False
    
    buscar_recursivo_en_archivo(archivo, filtros, estado)

def iniciar_busqueda_recursiva():
    limpiar_consola()
    print("--- BUSQUEDA DE PAQUETES ---")
    print("Deje en blanco lo que no quiera filtrar.")
    
    filtros = {}
    
    texto_filtro = input("Ingrese Destino o Provincia a buscar: ").strip()
    if texto_filtro:
        filtros['texto_buscar'] = texto_filtro
    
    try:
        precio_max_str = input("Ingrese precio maximo base (o 0 para no filtrar): ").strip()
        if precio_max_str:
            precio_max = float(precio_max_str)
            if precio_max > 0:
                filtros['precio_max'] = precio_max
    except ValueError:
        print("Precio maximo invalido, no se filtrara por precio.")
    
    f_paquetes = None
    try:
        f_paquetes = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        estado = {'encontrado': False, 'leyendo_primera': False}
        buscar_recursivo_en_archivo(f_paquetes, filtros, estado)
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as e:
        print(f"Error: {e}")
    finally:
        try:
            f_paquetes.close()
        except NameError:
            pass
    
    input("\nPresione Enter para volver al menu...")

def mostrar_detalles_paquete(paquete):
    limpiar_consola()
    print("=" * 70)
    print(f"DETALLES DEL PAQUETE ID: {paquete['id']} - {paquete['destino']}, {paquete['provincia']}")
    print(f"Duracion: {paquete['duracion']} | Cupo actual: {paquete['cupo']}")
    print(f"Precio Base: ${paquete['precio_base']:.2f}")

    for seccion, titulo in [('transporte', 'Transporte'), ('alojamiento', 'Alojamiento')]:
        if paquete.get(seccion):
            print(f"\n--- Opciones de {titulo} ---")
            for i, opcion in enumerate(paquete[seccion]):
                print(f"   {i+1}. {opcion['nombre']} (+${opcion['precio']:.2f})")
                if opcion.get('desc'):
                    print(f"     Descripcion: {opcion['desc']}")

    if paquete.get('fechas'):
        print("\n--- Fechas ---")
        for i, opcion in enumerate(paquete['fechas']):
            print(f"   {i+1}. {opcion['nombre']}: {opcion['fecha']}")

    excursion_base = paquete.get('excursion_base')
    if excursion_base and 'nombre' in excursion_base and 'precio' in excursion_base:
        print(f"\n--- Excursion Incluida ---")
        print(f"   - {excursion_base['nombre']} (+${excursion_base['precio']:.2f})")

    excursiones_adicionales = paquete.get('excursiones_adicionales')
    if excursiones_adicionales:
        print("\n--- Excursiones Adicionales (Opcionales) ---")
        for i, opcion in enumerate(excursiones_adicionales):
            print(f"   {i+1}. {opcion['nombre']} (+${opcion['precio']:.2f})")

    print("=" * 70)

def gestionar_vista_de_paquetes():
    provincias = mostrar_provincias_interactivo()
    
    if not provincias:
        print("\nNo hay paquetes cargados.")
        input("Presione Enter...")
        return
    
    salir_vista = False
    while not salir_vista:
        limpiar_consola()
        print("--- VER PAQUETES (Paso 1: Provincia) ---")
        for i, prov in enumerate(provincias):
            print(f"   {i+1}. {prov}")
        print("\n   0. Volver al Menu Principal")
        
        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                salir_vista = True
                continue
            
            if 1 <= nro_prov <= len(provincias):
                provincia_elegida = provincias[nro_prov - 1]
                destinos = mostrar_destinos_provincia_interactivo(provincia_elegida)
                
                ver_paquetes = True
                while ver_paquetes:
                    limpiar_consola()
                    print(f"--- PAQUETES EN {provincia_elegida.upper()} ---")
                    for i, dest in enumerate(destinos):
                        print(f"   {i+1}. {dest[1]}")
                    print("\n   0. Volver a Provincias")
                    
                    nro_paq_str = input("\nSeleccione el Nro del Paquete para ver detalles: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            ver_paquetes = False
                            continue
                        
                        if 1 <= nro_paq <= len(destinos):
                            id_elegido = destinos[nro_paq - 1][0]
                            paquete = cargar_paquete_completo_por_id(id_elegido)
                            if paquete:
                                mostrar_detalles_paquete(paquete)
                                input("\nPresione Enter para volver a la lista de paquetes...")
                            else:
                                print("Error: No se pudo cargar el paquete.")
                                input("...")
                        else:
                            print("Error: Numero de paquete no valido.")
                            input("...")
                    except ValueError:
                        print("Error: Ingrese un numero.")
                        input("...")
            else:
                print("Error: Numero de provincia no valido.")
                input("...")
        except ValueError:
            print("Error: Ingrese un numero.")
            input("...")

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
            prompt = prompt + ", 0 para ninguna): " if permite_ninguno else prompt + "): "
            opcion_num_str = input(prompt)
            opcion_num = int(opcion_num_str)

            if permite_ninguno and opcion_num == 0:
                opcion_seleccionada = None
                opcion_valida = True
            elif 1 <= opcion_num <= len(lista_opciones):
                opcion_seleccionada = lista_opciones[opcion_num - 1]
                opcion_valida = True
            else:
                print("Error: Numero fuera de rango.")
        except ValueError:
            print("Error: Ingrese un numero valido.")

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
            print("No quedan mas opciones por agregar.")
            break
        
        for i, opcion in enumerate(opciones_disponibles):
            print(f"   {i+1}. {opcion.get('nombre', opcion)} (+${opcion['precio']:.2f})")
        
        print("\n   0. Terminar seleccion de excursiones")

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
                print("Error: Numero fuera de rango.")
        except ValueError:
            print("Error: Ingrese un numero valido.")

    print("\nExcursiones seleccionadas:")
    if not opciones_seleccionadas:
        print(" - Ninguna")
    else:
        for excursion in opciones_seleccionadas:
            print(f" - {excursion['nombre']} (+${excursion['precio']:.2f})")

    return opciones_seleccionadas

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
        if f_reservas:
            f_reservas.close()

def gestionar_reserva(matriz_cupos):
    limpiar_consola()
    print("--- REALIZAR UNA RESERVA ---")

    provincias = mostrar_provincias_interactivo()
    if not provincias:
        print("\nNo hay paquetes para reservar.")
        input("Presione Enter para volver...")
        return

    paquete_elegido = None
    id_elegido = None
    salir_seleccion = False

    while not salir_seleccion:
        limpiar_consola()
        print("--- REALIZAR UNA RESERVA (Paso 1: Provincia) ---")
        for i, prov in enumerate(provincias):
            print(f"   {i+1}. {prov}")
        print("\n   0. Volver al Menu Principal")

        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                return

            if 1 <= nro_prov <= len(provincias):
                provincia_elegida = provincias[nro_prov - 1]
                destinos = mostrar_destinos_provincia_interactivo(provincia_elegida)

                seleccionar_paquete = True
                while seleccionar_paquete:
                    limpiar_consola()
                    print(f"--- REALIZAR UNA RESERVA (Paso 2: Paquete en {provincia_elegida.upper()}) ---")
                    for i, dest in enumerate(destinos):
                        cupo = obtener_cupo_de_matriz(matriz_cupos, dest[0])
                        print(f"   {i+1}. {dest[1]} (Cupo: {cupo})")
                    print("\n   0. Volver a Provincias")

                    nro_paq_str = input("\nSeleccione el Nro del Paquete a reservar: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            seleccionar_paquete = False
                            continue

                        if 1 <= nro_paq <= len(destinos):
                            id_elegido = destinos[nro_paq - 1][0]
                            seleccionar_paquete = False
                            salir_seleccion = True
                        else:
                            print("Error: Numero de paquete no valido.")
                            input("...")
                    except ValueError:
                        print("Error: Ingrese un numero.")
                        input("...")
            else:
                print("Error: Numero de provincia no valido.")
                input("...")
        except ValueError:
            print("Error: Ingrese un numero.")
            input("...")

    if id_elegido:
        cupo_disponible = obtener_cupo_de_matriz(matriz_cupos, id_elegido)
        
        if cupo_disponible <= 0:
            print(f"\nLo sentimos, no hay cupo disponible.")
            input("\nPresione Enter para volver al menu...")
            return

        #  Cargar el paquete completo SOLO cuando se va a reservar
        paquete_elegido = cargar_paquete_completo_por_id(id_elegido)
        
        if not paquete_elegido:
            print("\nError al cargar el paquete.")
            input("\nPresione Enter para volver al menu...")
            return

        mostrar_detalles_paquete(paquete_elegido)
        
        opcion_transporte = seleccionar_opcion("Transporte", paquete_elegido.get('transporte', []))
        opcion_alojamiento = seleccionar_opcion("Alojamiento", paquete_elegido.get('alojamiento', []))
        opcion_fecha = seleccionar_opcion("fecha", paquete_elegido.get('fechas', []))

        if not opcion_transporte or not opcion_alojamiento or not opcion_fecha:
            print("\nError: Debe seleccionar transporte, alojamiento y fecha para continuar.")
            input("\nPresione Enter para volver al menu...")
            return
        
        excursiones_adicionales_elegidas = []
        excursiones_adicionales = paquete_elegido.get('excursiones_adicionales')
        
        if excursiones_adicionales:
            agregar_adicional = input("\nDesea agregar excursiones adicionales? (si/no): ").strip().lower()
            while agregar_adicional not in ["si", "no"]:
                print("Respuesta no valida. Por favor, ingrese 'si' o 'no'.")
                agregar_adicional = input("Desea agregar excursiones adicionales? (si/no): ").strip().lower()
            
            if agregar_adicional == "si":
                excursiones_adicionales_elegidas = seleccionar_multiples_opciones("Excursion Adicional", excursiones_adicionales)

        conf = input("\nConfirma la reserva? (si/no): ").strip().lower()
        while conf not in ["si", "no"]:
            print("Respuesta no valida. Por favor, ingrese 'si' o 'no'.")
            conf = input("Confirma la reserva? (si/no): ").strip().lower()

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
                precio_final = precio_final * 1.20
                print(f"Por ser '{opcion_fecha['nombre']}', se aplica un recargo del 20%.")

            print(f"PRECIO FINAL: ${precio_final:.2f}")

            nombre_cliente = input("Ingrese su nombre completo para la reserva: ").strip()
            if not nombre_cliente:
                print("\nReserva cancelada: el nombre no puede estar vacio.")
            else:
                ticket = obtener_siguiente_ticket()
                
                #  Actualizar cupo en la matriz
                actualizar_cupo_en_matriz(matriz_cupos, id_elegido, -1)
                
                opciones_elegidas = {
                    'transporte': opcion_transporte,
                    'alojamiento': opcion_alojamiento,
                    'excursiones_adicionales': excursiones_adicionales_elegidas
                }

                registrar_reserva_en_archivo(ticket, paquete_elegido, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final)

                print(f"\nReserva confirmada con exito!")
                print(f"Su numero de ticket es: {str(ticket).zfill(8)}")
                print("Se ha descontado un cupo del paquete.")
                
                #  Guardar cambios en el archivo
                guardar_cupos_en_archivo(matriz_cupos)
        else:
            print("\nReserva no confirmada.")

        input("\nPresione Enter para volver al menu...")

def gestionar_cancelacion(matriz_cupos):
    limpiar_consola()
    print("--- CANCELAR UNA RESERVA ---")
    
    try:
        ticket_a_cancelar_str = input("Ingrese el numero de ticket de la reserva a cancelar (o 0 para volver): ")
        ticket_a_cancelar = int(ticket_a_cancelar_str)
        if ticket_a_cancelar == 0:
            return
    except ValueError:
        print("Error: El ticket debe ser un numero.")
        input("\nPresione Enter...")
        return

    f_lectura = None
    f_escritura = None
    reserva_encontrada = False
    reserva_ya_cancelada = False
    id_paquete_a_reponer = -1

    try:
        # Leer línea por línea y escribir en archivo temporal
        f_lectura = open(ARCHIVO_RESERVAS, "rt", encoding='utf-8')
        f_escritura = open("temp_reservas.txt", "wt", encoding='utf-8')

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
        
        f_lectura.close()
        f_escritura.close()
    
    except FileNotFoundError:
        print("Aun no existen reservas para cancelar.")
        input("\nPresione Enter...")
        return
    except OSError as e:
        print(f"Error al leer el archivo de reservas: {e}")
        input("\nPresione Enter...")
        return
    finally:
        try:
            f_lectura.close()
        except:
            pass
        try:
            f_escritura.close()
        except:
            pass

    if reserva_encontrada and not reserva_ya_cancelada:
        #  Actualizar cupo en la matriz
        cupo_repuesto = actualizar_cupo_en_matriz(matriz_cupos, id_paquete_a_reponer, +1)
        
        if cupo_repuesto:
            guardar_cupos_en_archivo(matriz_cupos)

        #  Reemplazar archivo original
        try:
            f_lectura = open("temp_reservas.txt", "rt", encoding='utf-8')
            f_escritura = open(ARCHIVO_RESERVAS, "wt", encoding='utf-8')
            
            for linea in f_lectura:
                f_escritura.write(linea)
            
            f_lectura.close()
            f_escritura.close()
            
            print(f"\nReserva del ticket {str(ticket_a_cancelar).zfill(8)} cancelada con exito!")
            if cupo_repuesto:
                print("Se ha restaurado y guardado un cupo al paquete correspondiente.")
            else:
                print("ADVERTENCIA: No se encontro el paquete original para reponer el cupo.")

        except OSError as e:
            print(f"Error al guardar los cambios en el archivo de reservas: {e}")
        finally:
            try:
                f_lectura.close()
            except:
                pass
            try:
                f_escritura.close()
            except:
                pass
    
    elif not reserva_encontrada:
        print("Error: No se encontro ninguna reserva con ese numero de ticket.")
    elif reserva_ya_cancelada:
        print("Esa reserva ya habia sido cancelada anteriormente.")

    input("\nPresione Enter para volver al menu...")

def solicitar_opcion_menu_recursivo():
    opcion_str = input("Seleccione una opcion: ")
    
    try:
        opcion_num = int(opcion_str)
        
        if 1 <= opcion_num <= 5:
            return opcion_num
        else:
            print("\nError: Opcion no valida.")
            input("\nPresione Enter para continuar...")
            return solicitar_opcion_menu_recursivo()
            
    except ValueError:
        print("\nError: Por favor, ingrese solo numeros.")
        input("\nPresione Enter para continuar...")
        return solicitar_opcion_menu_recursivo()

def mostrar_menu_principal(matriz_cupos):
    salir = False
    while not salir:
        limpiar_consola()
        print("--- MENU PRINCIPAL ---")
        print("1. Ver Paquetes Turisticos")
        print("2. Buscar Paquete por Criterios")
        print("3. Realizar una Reserva")
        print("4. Cancelar una Reserva")
        print("5. Guardar Cambios y Salir")
        
        opcion = solicitar_opcion_menu_recursivo()

        if opcion == 1:
            gestionar_vista_de_paquetes()
        elif opcion == 2:
            iniciar_busqueda_recursiva()
        elif opcion == 3:
            gestionar_reserva(matriz_cupos)
        elif opcion == 4:
            gestionar_cancelacion(matriz_cupos)
        elif opcion == 5:
            guardar_cupos_en_archivo(matriz_cupos)
            print("\nDatos guardados correctamente.")
            input("Presione Enter para salir...")
            salir = True

salir_del_sistema = False
while not salir_del_sistema:
    limpiar_consola()
    print("--- SISTEMA DE GESTION TURISTICA ---")
    print("1. Iniciar Sesion")
    print("2. Registrar Nuevo Usuario")
    print("3. Salir")
    opcion_inicio = input("Seleccione una opcion: ")

    if opcion_inicio == '1':
        if realizar_login():
            limpiar_consola()
            print("Acceso concedido!")
            
            # CARGA SOLO LA MATRIZ DE CUPOS (NO todos los paquetes)
            matriz_cupos = cargar_matriz_cupos()
            
            if matriz_cupos is not None:
                if len(matriz_cupos) == 0:
                    print("ADVERTENCIA: No hay paquetes definidos en el archivo.")
                else:
                    print(f"Matriz cargada: {len(matriz_cupos)} paquetes encontrados.")
                mostrar_menu_principal(matriz_cupos)
            else:
                print("Error grave al cargar la matriz de cupos. No se puede continuar.")
                input("Presione Enter para salir.")

            salir_del_sistema = True
        else:
            print("\nUsuario o contrasena incorrectos.")
            input("Presione Enter para continuar...")

    elif opcion_inicio == '2':
        registrar_usuario()
        input("\nPresione Enter para volver al menu de inicio...")

    elif opcion_inicio == '3':
        print("\nGracias por usar el sistema.")
        salir_del_sistema = True

    else:
        print("\nOpcion no valida. Por favor, intente de nuevo.")
        input("\nPresione Enter para continuar...")