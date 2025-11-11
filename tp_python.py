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
    arch = None  # Definir arch antes del try
    try:
        arch = open(ARCHIVO_CONTADOR_TICKET, "rt")
        contenido = arch.read(100)
        if contenido:
            ultimo_ticket = int(contenido)
        arch.close()
    except (FileNotFoundError, ValueError):
        ultimo_ticket = 0
    except OSError as mensaje:
        print(f"Error al leer contador: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

    siguiente_ticket = ultimo_ticket + 1
    arch = None  # Reiniciar arch
    try:
        arch = open(ARCHIVO_CONTADOR_TICKET, "wt")
        arch.write(str(siguiente_ticket))
        arch.close()
    except OSError as mensaje:
        print(f"Error al escribir contador: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

    return siguiente_ticket

def realizar_login():
    print("--- Bienvenido/a al Sistema de Paquetes Turisticos ---")
    usuario_ingresado = input("Usuario: ")
    contrasena_ingresada = input("Contrasena: ")
    acceso_concedido = False
    arch = None
    
    try:
        arch = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
        linea = arch.readline()
        while linea:
            try:
                usuario_archivo, contrasena_archivo = linea.strip().split(";")
                if usuario_ingresado == usuario_archivo and contrasena_ingresada == contrasena_archivo:
                    acceso_concedido = True
                    break
            except ValueError:
                pass
            linea = arch.readline()
        arch.close()
    except FileNotFoundError:
        print(f"\nADVERTENCIA: No se encontro '{ARCHIVO_USUARIOS}'. Puede registrar un usuario.")
    except OSError as mensaje:
        print(f"\nERROR: No se pudo leer el archivo '{ARCHIVO_USUARIOS}'. {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass
    
    return acceso_concedido

def registrar_usuario():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    usuario_valido = False
    nuevo_usuario = ""
    arch = None
    
    while not usuario_valido:
        nuevo_usuario = input("Ingrese su nuevo nombre de usuario: ").strip()
        if not nuevo_usuario:
            print("Error: El nombre de usuario no puede estar vacio.")
            continue

        usuario_existe = False
        try:
            arch = open(ARCHIVO_USUARIOS, "rt", encoding='utf-8')
            linea = arch.readline()
            while linea:
                try:
                    if linea.strip().split(';')[0].lower() == nuevo_usuario.lower():
                        usuario_existe = True
                        break
                except (ValueError, IndexError):
                    pass
                linea = arch.readline()
            arch.close()
        except FileNotFoundError:
            pass
        finally:
            try:
                if arch and not arch.closed:
                    arch.close()
            except NameError:
                pass

        if usuario_existe:
            print("Error: Ese nombre de usuario ya esta en uso.")
        else:
            usuario_valido = True

    nueva_contrasena = input("Ingrese su nueva contrasena: ")
    arch = None
    
    try:
        arch = open(ARCHIVO_USUARIOS, "at", encoding='utf-8')
        arch.write(f"{nuevo_usuario};{nueva_contrasena}\n")
        arch.close()
        print("\nUsuario registrado con exito!")
    except OSError as mensaje:
        print(f"\nERROR: No se pudo registrar el usuario. {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

def obtener_cupo_por_id(id_paquete):
    """Lee el archivo y retorna SOLO el cupo del paquete solicitado"""
    cupo = 0
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        leyendo_primera = False
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                partes = linea_strip.split(";")
                try:
                    if int(partes[0]) == id_paquete:
                        cupo = int(partes[5])
                        break
                except (ValueError, IndexError):
                    pass # Ignora línea mal formada
                leyendo_primera = False
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        pass
    except (ValueError, IndexError):
        pass
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass
    
    return cupo

def actualizar_cupo_en_archivo(id_paquete, incremento):
    """Actualiza el cupo de UN paquete sin cargar todo el archivo"""
    arch_lectura = None
    arch_escritura = None
    try:
        arch_lectura = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        arch_escritura = open("temp_paquetes.txt", "wt", encoding="utf-8")
        
        leyendo_primera = False
        
        linea = arch_lectura.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
                arch_escritura.write(linea)
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    partes = linea_strip.split(";")
                    if int(partes[0]) == id_paquete:
                        partes[5] = str(int(partes[5]) + incremento)
                        arch_escritura.write(";".join(partes) + "\n")
                    else:
                        arch_escritura.write(linea)
                except (ValueError, IndexError):
                    arch_escritura.write(linea) # Escribe línea mal formada tal cual
                leyendo_primera = False
            else:
                arch_escritura.write(linea)
            
            linea = arch_lectura.readline()
        
        arch_lectura.close()
        arch_escritura.close()
        
        # Reemplazar archivo original
        arch_lectura = open("temp_paquetes.txt", "rt", encoding="utf-8")
        arch_escritura = open(ARCHIVO_PAQUETES, "wt", encoding="utf-8")
        
        linea = arch_lectura.readline()
        while linea:
            arch_escritura.write(linea)
            linea = arch_lectura.readline()
        
        arch_lectura.close()
        arch_escritura.close()
        
        print("Cupo actualizado correctamente.")
        
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except OSError as mensaje:
        print("Error al procesar archivo:", mensaje)
    finally:
        try:
            if arch_lectura and not arch_lectura.closed:
                arch_lectura.close()
        except NameError:
            pass
        try:
            if arch_escritura and not arch_escritura.closed:
                arch_escritura.close()
        except NameError:
            pass

def mostrar_provincias_sin_repetir():
    """Muestra provincias SIN almacenarlas en lista"""
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        print("\n--- PROVINCIAS DISPONIBLES ---")
        numero = 1
        leyendo_primera = False
        provincia_anterior = ""
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    provincia = linea_strip.split(";")[1]
                    if provincia != provincia_anterior:
                        print(f"   {numero}. {provincia}")
                        provincia_anterior = provincia
                        numero = numero + 1
                except IndexError:
                    pass # Ignora línea mal formada
                leyendo_primera = False
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        print("No se encontro el archivo de paquetes.")
    except OSError as mensaje:
        print(f"Error: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

def obtener_provincia_por_numero(numero_seleccionado):
    """Retorna la provincia en la posición indicada SIN cargar lista"""
    provincia_encontrada = ""
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        numero_actual = 0
        leyendo_primera = False
        provincia_anterior = ""
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    provincia = linea_strip.split(";")[1]
                    if provincia != provincia_anterior:
                        numero_actual = numero_actual + 1
                        if numero_actual == numero_seleccionado:
                            provincia_encontrada = provincia
                            break
                        provincia_anterior = provincia
                except IndexError:
                    pass
                leyendo_primera = False
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        pass
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass
    
    return provincia_encontrada

def mostrar_destinos_de_provincia(provincia_buscada):
    """Muestra destinos de una provincia SIN almacenarlos en lista"""
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        print(f"\n--- PAQUETES EN {provincia_buscada.upper()} ---")
        numero = 1
        leyendo_primera = False
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    partes = linea_strip.split(";")
                    provincia = partes[1]
                    
                    if provincia.lower() == provincia_buscada.lower():
                        id_paq = partes[0]
                        destino = partes[2]
                        cupo = partes[5]
                        print(f"   {numero}. {destino} (ID: {id_paq}, Cupo: {cupo})")
                        numero = numero + 1
                except (IndexError, ValueError):
                    pass
                leyendo_primera = False
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as mensaje:
        print(f"Error: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

def obtener_id_paquete_por_posicion(provincia_buscada, posicion_seleccionada):
    """Retorna el ID del paquete en la posición indicada SIN cargar lista"""
    id_encontrado = 0
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        posicion_actual = 0
        leyendo_primera = False
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    partes = linea_strip.split(";")
                    provincia = partes[1]
                    
                    if provincia.lower() == provincia_buscada.lower():
                        posicion_actual = posicion_actual + 1
                        if posicion_actual == posicion_seleccionada:
                            id_encontrado = int(partes[0])
                            break
                except (IndexError, ValueError):
                    pass
                leyendo_primera = False
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        pass
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass
    
    return id_encontrado

def cargar_paquete_por_id(id_buscado):
    """Carga UN SOLO paquete específico"""
    paquete = None
    arch = None
    
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        linea = arch.readline()
        seccion_actual = ""
        
        while linea:
            linea_strip = linea.strip()
            
            if len(linea_strip) > 0:
                if len(linea_strip) >= 8 and linea_strip[0:8] == "#PAQUETE":
                    if paquete:
                        break
                    paquete = {}
                    seccion_actual = "paquete"
                
                elif len(linea_strip) >= 12 and linea_strip[0:12] == "#FIN_PAQUETE":
                    if paquete and paquete.get('id') == id_buscado:
                        break
                    paquete = None
                    seccion_actual = ""
                
                elif linea_strip[0] == "#" and paquete is not None:
                    seccion_actual = linea_strip[1:].lower()
                    if seccion_actual not in ["excursion_base", "paquete"]:
                        paquete[seccion_actual] = []
                
                elif seccion_actual != "" and paquete is not None:
                    partes = linea_strip.split(";")
                    
                    if seccion_actual == "paquete":
                        try:
                            id_str = partes[0]
                            id_paq = int(id_str)
                            
                            if id_paq != id_buscado:
                                paquete = None
                                seccion_actual = ""
                                linea = arch.readline()
                                continue
                            
                            paquete["id"] = id_paq
                            paquete["provincia"] = partes[1]
                            paquete["destino"] = partes[2]
                            paquete["duracion"] = partes[3]
                            paquete["precio_base"] = float(partes[4])
                            paquete["cupo"] = int(partes[5])
                        except (ValueError, IndexError):
                            paquete = None # Paquete mal formado
                            seccion_actual = ""
                    
                    elif seccion_actual in ["transporte", "alojamiento", "excursiones_adicionales", "fechas"]:
                        try:
                            if seccion_actual == "transporte" or seccion_actual == "alojamiento":
                                nombre = partes[0]
                                precio = float(partes[1])
                                desc = partes[2] if len(partes) > 2 else ""
                                paquete[seccion_actual].append(
                                    {"nombre": nombre, "precio": precio, "desc": desc}
                                )
                            elif seccion_actual == "excursiones_adicionales":
                                nombre = partes[0]
                                precio = float(partes[1])
                                paquete[seccion_actual].append({"nombre": nombre, "precio": precio})
                            elif seccion_actual == "fechas":
                                nombre_fecha = partes[0]
                                valor_fecha = partes[1]
                                paquete[seccion_actual].append({"nombre": nombre_fecha, "fecha": valor_fecha})
                        except (ValueError, IndexError):
                            pass # Ignora sub-item mal formado
                    
                    elif seccion_actual == "excursion_base":
                        try:
                            nombre = partes[0]
                            precio = float(partes[1])
                            paquete[seccion_actual] = {"nombre": nombre, "precio": precio}
                        except (ValueError, IndexError):
                             pass
            
            linea = arch.readline()
        
        arch.close()
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except (ValueError, IndexError) as mensaje:
        print(f"Error de formato: {mensaje}")
    except OSError as mensaje:
        print(f"Error: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass
    
    return paquete

def normalizar_cadena(cadena):
    cadena = cadena.lower()
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
    }
    for acentuada, sin_acento in reemplazos.items():
        cadena = cadena.replace(acentuada, sin_acento)
    return cadena

def buscar_paquetes_por_criterios():
    limpiar_consola()
    print("--- BUSQUEDA DE PAQUETES ---")
    print("Deje en blanco lo que no quiera filtrar.")
    
    texto_buscar = input("Ingrese Destino o Provincia a buscar: ").strip()
    precio_max = 0
    
    try:
        precio_max_str = input("Ingrese precio maximo base (o 0 para no filtrar): ").strip()
        if precio_max_str:
            precio_max = float(precio_max_str)
    except ValueError:
        print("Precio invalido, no se filtrara por precio.")
    
    arch = None
    try:
        arch = open(ARCHIVO_PAQUETES, "rt", encoding="utf-8")
        
        leyendo_primera = False
        encontrado = False
        
        linea = arch.readline()
        while linea:
            linea_strip = linea.strip()
            
            if linea_strip == "#PAQUETE":
                leyendo_primera = True
            elif leyendo_primera and linea_strip != "" and linea_strip[0] != "#":
                try:
                    partes = linea_strip.split(";")
                    id_paq = int(partes[0])
                    provincia = partes[1]
                    destino = partes[2]
                    precio_base = float(partes[4])
                    cupo = int(partes[5])
                    
                    cumple_filtro = True
                    
                    if texto_buscar:
                        texto_norm = normalizar_cadena(texto_buscar)
                        destino_norm = normalizar_cadena(destino)
                        provincia_norm = normalizar_cadena(provincia)
                        
                        if texto_norm not in destino_norm and texto_norm not in provincia_norm:
                            cumple_filtro = False
                    
                    if precio_max > 0 and precio_base > precio_max:
                        cumple_filtro = False
                    
                    if cumple_filtro:
                        print("\n--- Paquete Encontrado ---")
                        print(f"ID: {id_paq} - {destino}, {provincia}")
                        print(f"Precio Base: ${precio_base:.2f} | Cupo: {cupo}")
                        encontrado = True
                        
                        continuar = input("Desea buscar el siguiente? (s/n): ").lower().strip()
                        if continuar != "s":
                            break
                except (ValueError, IndexError):
                    pass # Ignora línea mal formada
                leyendo_primera = False
            
            linea = arch.readline()
        
        if not encontrado:
            print("\n--- No se encontraron paquetes con esos criterios. ---")
        
        arch.close()
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except OSError as mensaje:
        print(f"Error: {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
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
    salir_vista = False
    
    while not salir_vista:
        limpiar_consola()
        mostrar_provincias_sin_repetir()
        print("\n   0. Volver al Menu Principal")
        
        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                salir_vista = True
                continue
            
            provincia_elegida = obtener_provincia_por_numero(nro_prov)
            
            if provincia_elegida:
                ver_paquetes = True
                while ver_paquetes:
                    limpiar_consola()
                    mostrar_destinos_de_provincia(provincia_elegida)
                    print("\n   0. Volver a Provincias")

                    nro_paq_str = input("\nSeleccione el Nro del Paquete para ver detalles: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            ver_paquetes = False
                            continue
                        
                        id_elegido = obtener_id_paquete_por_posicion(provincia_elegida, nro_paq)
                        
                        if id_elegido > 0:
                            paquete = cargar_paquete_por_id(id_elegido)
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
    arch = None
    try:
        arch = open(ARCHIVO_RESERVAS, "at", encoding='utf-8')
        fecha_hoy = datetime.date.today()
        fecha_reserva = f"{fecha_hoy.day}/{fecha_hoy.month}/{fecha_hoy.year}"

        detalles = f"Transporte: {opciones_elegidas['transporte']['nombre']} | Alojamiento: {opciones_elegidas['alojamiento']['nombre']}"
        lista_excursiones = opciones_elegidas.get('excursiones_adicionales')
        if lista_excursiones:
            nombres_excursiones = ", ".join([exc['nombre'] for exc in lista_excursiones])
            detalles += f" | Extras: [{nombres_excursiones}]"

        fecha_nombre = opcion_fecha['nombre'] if opcion_fecha and 'nombre' in opcion_fecha else 'N/A'

        linea = f"{ticket};{paquete['id']};{paquete['destino']};{nombre_cliente};{fecha_reserva};{fecha_nombre};{precio_final:.2f};ACTIVA;{detalles}\n"
        arch.write(linea)
        arch.close()
    except OSError as mensaje:
        print(f"\nERROR: No se pudo guardar la reserva. {mensaje}")
    finally:
        try:
            if arch and not arch.closed:
                arch.close()
        except NameError:
            pass

def gestionar_reserva():
    limpiar_consola()
    print("--- REALIZAR UNA RESERVA ---")

    paquete_elegido = None
    id_elegido = 0
    salir_seleccion = False

    while not salir_seleccion:
        limpiar_consola()
        print("--- REALIZAR UNA RESERVA (Paso 1: Provincia) ---")
        mostrar_provincias_sin_repetir()
        print("\n   0. Volver al Menu Principal")

        nro_prov_str = input("\nSeleccione el Nro de la Provincia: ")
        try:
            nro_prov = int(nro_prov_str)
            if nro_prov == 0:
                return

            provincia_elegida = obtener_provincia_por_numero(nro_prov)
            
            if provincia_elegida:
                seleccionar_paquete = True
                while seleccionar_paquete:
                    limpiar_consola()
                    print(f"--- REALIZAR UNA RESERVA (Paso 2: Paquete en {provincia_elegida.upper()}) ---")
                    mostrar_destinos_de_provincia(provincia_elegida)
                    print("\n   0. Volver a Provincias") 
                    
                    nro_paq_str = input("\nSeleccione el Nro del Paquete a reservar: ")
                    try:
                        nro_paq = int(nro_paq_str)
                        if nro_paq == 0:
                            seleccionar_paquete = False
                            continue

                        id_elegido = obtener_id_paquete_por_posicion(provincia_elegida, nro_paq)
                        
                        if id_elegido > 0:
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

    # --- CONTINUACIÓN DE LA LÓGICA DE RESERVA ---

    if id_elegido > 0:
        cupo_disponible = obtener_cupo_por_id(id_elegido)
        
        if cupo_disponible <= 0:
            print(f"\nLo sentimos, no hay cupo disponible.")
            input("\nPresione Enter para volver al menu...")
            return

        paquete_elegido = cargar_paquete_por_id(id_elegido)
        
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
                
                actualizar_cupo_en_archivo(id_elegido, -1)
                
                opciones_elegidas = {
                    'transporte': opcion_transporte,
                    'alojamiento': opcion_alojamiento,
                    'excursiones_adicionales': excursiones_adicionales_elegidas
                }

                registrar_reserva_en_archivo(ticket, paquete_elegido, nombre_cliente, opcion_fecha, opciones_elegidas, precio_final)

                print(f"\nReserva confirmada con exito!")
                print(f"Su numero de ticket es: {str(ticket).zfill(8)}")
                print("Se ha descontado un cupo del paquete.")
        else:
            print("\nReserva no confirmada.")

        input("\nPresione Enter para volver al menu...")

def gestionar_cancelacion():
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

    arch_lectura = None
    arch_escritura = None
    reserva_encontrada = False
    reserva_ya_cancelada = False
    id_paquete_a_reponer = 0

    try:
        arch_lectura = open(ARCHIVO_RESERVAS, "rt", encoding='utf-8')
        arch_escritura = open("temp_reservas.txt", "wt", encoding='utf-8')

        linea = arch_lectura.readline()
        while linea:
            try:
                partes = linea.strip().split(';')
                ticket_actual = int(partes[0])

                if ticket_actual == ticket_a_cancelar:
                    reserva_encontrada = True
                    if partes[7].upper() == "CANCELADA":
                        reserva_ya_cancelada = True
                        arch_escritura.write(linea)
                    else:
                        partes[7] = "CANCELADA"
                        id_paquete_a_reponer = int(partes[1])
                        linea_modificada = ";".join(partes) + "\n"
                        arch_escritura.write(linea_modificada)
                else:
                    arch_escritura.write(linea)
            
            except (ValueError, IndexError):
                arch_escritura.write(linea)
            
            linea = arch_lectura.readline()
        
        arch_lectura.close()
        arch_escritura.close()
    
    except FileNotFoundError:
        print("Aun no existen reservas para cancelar.")
        input("\nPresione Enter...")
        return
    except OSError as mensaje:
        print(f"Error al leer el archivo de reservas: {mensaje}")
        input("\nPresione Enter...")
        return
    finally:
        try:
            if arch_lectura and not arch_lectura.closed:
                arch_lectura.close()
        except NameError:
            pass
        try:
            if arch_escritura and not arch_escritura.closed:
                arch_escritura.close()
        except NameError:
            pass

    if reserva_encontrada and not reserva_ya_cancelada:
        actualizar_cupo_en_archivo(id_paquete_a_reponer, +1)

        try:
            arch_lectura = open("temp_reservas.txt", "rt", encoding='utf-8')
            arch_escritura = open(ARCHIVO_RESERVAS, "wt", encoding='utf-8')
            
            linea = arch_lectura.readline()
            while linea:
                arch_escritura.write(linea)
                linea = arch_lectura.readline()
            
            arch_lectura.close()
            arch_escritura.close()
            
            print(f"\nReserva del ticket {str(ticket_a_cancelar).zfill(8)} cancelada con exito!")
            print("Se ha restaurado un cupo al paquete correspondiente.")

        except OSError as mensaje:
            print(f"Error al guardar los cambios en el archivo de reservas: {mensaje}")
        finally:
            try:
                if arch_lectura and not arch_lectura.closed:
                    arch_lectura.close()
            except NameError:
                pass
            try:
                if arch_escritura and not arch_escritura.closed:
                    arch_escritura.close()
            except NameError:
                pass
    
    elif not reserva_encontrada:
        print("Error: No se encontro ninguna reserva con ese numero de ticket.")
    elif reserva_ya_cancelada:
        print("Esa reserva ya habia sido cancelada anteriormente.")

    input("\nPresione Enter para volver al menu...")

def solicitar_opcion_menu():
    opcion_str = input("Seleccione una opcion: ")
    
    try:
        opcion_num = int(opcion_str)
        
        if 1 <= opcion_num <= 5:
            return opcion_num
        else:
            print("\nError: Opcion no valida.")
            input("\nPresione Enter para continuar...")
            return solicitar_opcion_menu()
            
    except ValueError:
        print("\nError: Por favor, ingrese solo numeros.")
        input("\nPresione Enter para continuar...")
        return solicitar_opcion_menu()

def mostrar_menu_principal():
    salir = False
    while not salir:
        limpiar_consola()
        print("--- MENU PRINCIPAL ---")
        print("1. Ver Paquetes Turisticos")
        print("2. Buscar Paquete por Criterios")
        print("3. Realizar una Reserva")
        print("4. Cancelar una Reserva")
        print("5. Salir")
        
        opcion = solicitar_opcion_menu()

        if opcion == 1:
            gestionar_vista_de_paquetes()
        elif opcion == 2:
            buscar_paquetes_por_criterios()
        elif opcion == 3:
            gestionar_reserva()
        elif opcion == 4:
            gestionar_cancelacion()
        elif opcion == 5:
            print("\nGracias por usar el sistema.")
            input("Presione Enter para salir...")
            salir = True

# PROGRAMA PRINCIPAL
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
            input("Presione Enter para continuar...")
            mostrar_menu_principal()
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
