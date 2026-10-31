from Iverton_Clientes import guardar_datos #importa la funcion para guardar los dato
from datetime import datetime # Importar la funcion para obtener la fecha y hora

def listar_servicios(datos):   #Muestra todos los servicios 
    print("\n--- LISTA DE SERVICIOS ---")
    if not datos["servicios"]:  #si no hay servicios, muestre el mensaje 
        print("No hay servicios registrados.")      
        return
    for s in datos["servicios"].values():# recorre los servicios y los muestra
        print(f"Código: {s['codigo']} | {s['nombre']} | Mano de Obra: ${s['mano_obra']:.2f} | Precio: ${s['precio']:.2f}")

def listar_repuestos(datos): # muestra todos los respuesto
    print("\n--- LISTA DE REPUESTOS ---")
    if not datos["repuestos"]:       # si no hay repuestos,muestra un mensaje
        print("No hay repuestos registrados.")
        return
    for r in datos["repuestos"].values() :# recorre los repuestos y los muestra
        print(f"Código: {r['codigo']} | {r['nombre']} | Precio: ${r['precio']:.2f} | Stock: {r['stock']}")

def listar_ordenes(datos): #Muestra todas las ordenes 
    print("\n--- LISTA DE ÓRDENES ---")
    if not datos["ordenes"]:# si no hay ordenes, muestra un mensaje
        print("No hay órdenes registradas.")
        return
    for o in datos["ordenes"].values():   # recorre las ordenes y muetsra la informacion
        mec = o['mecanico_id'] if o['mecanico_id'] else "Sin asignar" # si no hay mecanico, indica que esta sin asignar
        print(f"Orden #{o['numero']} | Placa: {o['placa']} | Mecánico: {mec} | Estado: {o['estado']} | Fecha: {o['fecha_creacion']}")

def registrar_servicio(datos):
    print("\n--- REGISTRAR SERVICIO (Escriba 0 para regresar) ---")
    codigo = input("Código del Servicio: ").strip().upper()       # solicita el codigo
    if codigo == "0": return
    if not codigo: return print("Error: Código obligatorio.")   # valida el codigo
    if codigo in datos["servicios"]: return print("Error: Ya existe un servicio con ese código.")
    
    nombre = input("Nombre del Servicio: ").strip() # solicita el nombre 
    if nombre == "0": return                        # solicita la descripcion
    descripcion = input("Descripción: ").strip()    
    if descripcion == "0": return
    try:
        mano_obra = float(input("Costo Mano de Obra: "))  # convierte a numero
        precio = float(input("Costo Repuesto/Servicio: "))  #convierte a numero
    except ValueError:
        return print("Error: Los costos deben ser números.")

    datos["servicios"][codigo] = { # Guarda la información del servicio en el diccionario
        "codigo": codigo, "nombre": nombre, "descripcion": descripcion,
        "mano_obra": mano_obra, "precio": precio
    }
    guardar_datos(datos) # Actualiza el archivo donde se almacenan los datos.
    print("✔ Servicio registrado exitosamente.")

def registrar_repuesto(datos): # Permite registrar un nuevo repuesto con su precio y stock
    print("\n--- REGISTRAR REPUESTO (Escriba 0 para regresar) ---")
    codigo = input("Código del Repuesto: ").strip().upper()
    if codigo == "0": return
    if not codigo: return print("Error: Código obligatorio.") # Comprueba que el código sea válido y no esté repetido
    if codigo in datos["repuestos"]: return print("Error: Ya existe un repuesto con ese código.")
    
    nombre = input("Nombre del Repuesto: ").strip() # Solicita el nombre del repuesto.
    if nombre == "0": return
    try:       # Convierte el precio y el stock a sus tipos de datos correspondientes.
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
    except ValueError:
        return print("Error: Precio y stock deben ser numéricos.")

    datos["repuestos"][codigo] = {        # Registra el repuesto con todos sus datos.
        "codigo": codigo, "nombre": nombre, "precio": precio, "stock": stock
    }
    guardar_datos(datos) # Guarda los cambios realizados
    print("✔ Repuesto registrado exitosamente.")

def crear_orden(datos): # Crea una nueva orden de trabajo para un vehículo.
    print("\n--- CREAR ORDEN DE TRABAJO (Escriba 0 para regresar) ---")
    if not datos["vehiculos"]:
        return print("Error: No hay vehículos registrados.")
    
    print("Vehículos disponibles:")  # Muestra las placas de los vehículos disponibles.
    for p in datos["vehiculos"].keys(): print(f" - {p}")
    placa = input("Ingrese la Placa del vehículo: ").strip().upper()  # Solicita la placa del vehículo para la orden.
    if placa == "0": return
    if placa not in datos["vehiculos"]: return print("Error: Vehículo no encontrado.")

    print("Mecánicos disponibles:") # Muestra los mecánicos que pueden asignarse a la orden.
    for m in datos["mecanicos"].keys(): print(f" - {m}")
    mecanico = input("Ingrese ID del Mecánico (Deje vacío si no asignará aún): ").strip()# Permite asignar un mecánico o dejar la orden pendiente de asignación.
    if mecanico == "0": return
    if mecanico != "" and mecanico not in datos["mecanicos"]:
        return print("Error: Mecánico no encontrado.")

    if "contador" not in datos: datos["contador"] = 1  # genera un numero consecutivo para identificar la orden 
    numero = datos["contador"]
    datos["contador"] += 1
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M") #obtiene la fecha y la hora en que se crea la orden         

    datos["ordenes"][str(numero)] = {            # registra la orden con su informacion inicial
        "numero": numero, "placa": placa, "mecanico_id": mecanico,
        "estado": "Recibida", "servicios": [], "repuestos": [], "pagos": [],
        "fecha_creacion": fecha_actual, "fecha_finalizacion": None, "diagnostico": ""
    }
    guardar_datos(datos)         # guarda ka nueva orden en el archivo de datos
    print(f"✔ Orden #{numero} creada exitosamente. (Fecha: {fecha_actual})")