from Iverton_Clientes import guardar_datos
from datetime import datetime


def listar_servicios(datos):
    """Muestra los servicios que ofrece el taller."""
    print("\n--- LISTA DE SERVICIOS ---")           # Primero revisamos si hay servicios registrados

    
    if not datos.get("servicios"):
        print("No hay servicios registrados.")
        return

    
    for s in datos["servicios"].values(): # Mostramos los datos de cada servicio
        print(f"Código: {s['codigo']} | {s['nombre']} | Mano de Obra: ${s['mano_obra']:.2f} | Precio: ${s['precio']:.2f}")


def listar_repuestos(datos):
    """Muestra los repuestos disponibles en el inventario."""
    print("\n--- LISTA DE REPUESTOS ---")

    
    if not datos.get("repuestos"):
        print("No hay repuestos registrados.") # Comprobamos que existan repuestos para mostrar
        return

    
    for r in datos["repuestos"].values():
        print(f"Código: {r['codigo']} | {r['nombre']} | Precio: ${r['precio']:.2f} | Stock: {r['stock']}")


def listar_ordenes(datos):
    """Muestra las órdenes de trabajo registradas."""    # Recorremos el inventario para mostrar el precio y las existencias
    print("\n--- LISTA DE ÓRDENES ---")                    

    if not datos.get("ordenes"):
        print("No hay órdenes registradas.")
        return

    
    for o in datos["ordenes"].values(): # Mostramos la información de cada orden

       
        mec = o.get('mecanico_id') if o.get('mecanico_id') else "Sin asignar"     # Si todavía no tiene mecánico, mostramos que está sin asignar

        print(f"Orden #{o['numero']} | Placa: {o['placa']} | Mecánico: {mec} | Estado: {o.get('estado')} | Fecha: {o.get('fecha_creacion')}")


def registrar_servicio(datos):
    """Permite agregar un nuevo servicio al taller."""
    print("\n--- REGISTRAR SERVICIO (Escriba 0 para regresar) ---")

    
    codigo = input("Código del Servicio: ").strip().upper()

    if codigo == "0": return
    if not codigo: return print("Error: Código obligatorio.")       # Pedimos el código del servicio

    
    if codigo in datos.get("servicios", {}): return print("Error: Ya existe un servicio con ese código.")

    nombre = input("Nombre del Servicio: ").strip()
    if nombre == "0": return

    descripcion = input("Descripción: ").strip()
    if descripcion == "0": return            # Evitamos que se repita un código que ya existe
   
    try:
        mano_obra = float(input("Costo Mano de Obra: "))
        precio = float(input("Costo Repuesto/Servicio: "))
    except ValueError:
        return print("Error: Los costos deben ser números.") # Solicitamos los costos y comprobamos que sean números

    
    if mano_obra < 0 or precio < 0:
        return print("Error: Los costos no pueden ser negativos.")   # No permitimos ingresar cantidades negativas

    
    datos.setdefault("servicios", {})[codigo] = {
        "codigo": codigo, "nombre": nombre, "descripcion": descripcion,
        "mano_obra": mano_obra, "precio": precio
    }

    guardar_datos(datos)
    print("✔️ Servicio registrado exitosamente.") # Guardamos el nuevo servicio en los datos del taller


def registrar_repuesto(datos):
    """Permite agregar nuevos repuestos al inventario."""
    print("\n--- REGISTRAR REPUESTO (Escriba 0 para regresar) ---")

    codigo = input("Código del Repuesto: ").strip().upper()

    if codigo == "0": return
    if not codigo: return print("Error: Código obligatorio.")

    
    if codigo in datos.get("repuestos", {}): return print("Error: Ya existe un repuesto con ese código.")

    nombre = input("Nombre del Repuesto: ").strip()        # Revisamos que el código no esté registrado anteriorment
    if nombre == "0": return

    
    try:
        precio = float(input("Precio: "))
        stock = int(input("Stock inicial: "))
    except ValueError:
        return print("Error: Precio y stock deben ser numéricos.")          # Pedimos el precio y la cantidad inicial del repuesto

    
    if precio < 0 or stock < 0:
        return print("Error: El precio y el stock no pueden ser negativos.")   # Verificamos que los valores ingresados sean válidos

    
    datos.setdefault("repuestos", {})[codigo] = {
        "codigo": codigo, "nombre": nombre, "precio": precio, "stock": stock
    }

    guardar_datos(datos)
    print("✔️ Repuesto registrado exitosamente.")      # Agregamos el repuesto al inventario


def crear_orden(datos):
    """Crea una nueva orden de trabajo para un vehículo."""
    print("\n--- CREAR ORDEN DE TRABAJO (Escriba 0 para regresar) ---")

    
    if not datos.get("vehiculos"):
        return print("Error: No hay vehículos registrados.")

    print("Vehículos disponibles:")
    for p in datos["vehiculos"].keys():
        print(f" - {p}")

    placa = input("Ingrese la Placa del vehículo: ").strip().upper()      # Antes de crear una orden, debe existir al menos un vehículo

    if placa == "0": return

    
    if placa not in datos["vehiculos"]: return print("Error: Vehículo no encontrado.")        # Comprobamos que la placa esté registrada

    print("Mecánicos disponibles:")
    for m in datos.get("mecanicos", {}).keys():
        print(f" - {m}")

    
    mecanico = input("Ingrese ID del Mecánico (Deje vacío si no asignará aún): ").strip()

    if mecanico == "0": return

    if mecanico != "" and mecanico not in datos.get("mecanicos", {}):
        return print("Error: Mecánico no encontrado.")              # El mecánico puede asignarse ahora o dejarse pendiente

    
    if "contador" not in datos:
        datos["contador"] = 1

    numero = datos["contador"]
    datos["contador"] += 1                                        # Generamos un número diferente para cada nueva orden

   
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")       # Guardamos la fecha y hora en que se crea la orden

    
    datos.setdefault("ordenes", {})[str(numero)] = {
        "numero": numero, "placa": placa, "mecanico_id": mecanico,
        "estado": "Recibida", "servicios": [], "repuestos": [], "pagos": [],
        "fecha_creacion": fecha_actual, "fecha_finalizacion": None, "diagnostico": ""        # Creamos la orden con sus listas vacías y su estado inicial
    }

    guardar_datos(datos)
    print(f"✔️ Orden #{numero} creada exitosamente. (Fecha: {fecha_actual})")