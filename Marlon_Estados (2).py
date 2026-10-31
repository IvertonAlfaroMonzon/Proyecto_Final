
from Iverton_Clientes import guardar_datos   # Importa la función 'guardar_datos' desde el archivo/módulo 'Iverton_Clientes'


ESTADOS = ["Recibida", "En diagnóstico", "En reparación", "Finalizada", "Entregada"]   # Lista constante que define los estados válidos por los que puede pasar una orden
    

def ver_detalle_orden(datos):    # Función para visualizar toda la información detallada de una orden específica
    print("\n--- VER DETALLE DE ORDEN ---")
    
    num = input("Número de Orden: ").strip()    # Solicita el número de orden y elimina espacios en blanco al inicio o final (.strip)
   
    if num == "0": return    # Si el usuario ingresa "0", se cancela la acción y sale de la función
    
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")    # Verifica si el número de orden no existe en el diccionario; si no está, muestra error y sale
    
    
    o = datos["ordenes"][num]   # Se extrae la orden específica en la variable 'o' para acortar el código al imprimir

    print(f"\n--- ORDEN #{o['numero']} ---")      # Imprime los datos principales de la orden
    print(f"Placa: {o['placa']}")
    
    print(f"Mecánico: {o['mecanico_id'] if o['mecanico_id'] else 'Sin asignar'}")  # Operador ternario: muestra el ID del mecánico si tiene uno, sino muestra 'Sin asignar'
    print(f"Estado: {o['estado']}")
    print("Servicios:")
    
    for s in o["servicios"]: print(f" - {s}")   # Recorre y muestra en pantalla todos los servicios que tiene la orden
    print("Repuestos:")
    
    for r in o["repuestos"]: print(f" - {r['codigo_repuesto']} x{r['cantidad']}")    # Recorre y muestra el código y la cantidad de cada repuesto asignado a la orden


def asignar_mecanico_orden(datos):   # Función para asignarle un mecánico a una orden existente
    print("\n--- ASIGNAR MECÁNICO (Escriba 0 para regresar) ---")
    num = input("Número de Orden: ").strip()
    if num == "0": return
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")
    
    
    print("Mecánicos disponibles:")   # Muestra en pantalla todos los mecánicos registrados en la base de datos
    for m in datos["mecanicos"].keys(): print(f" - {m}")
    
    mec = input("ID del Mecánico: ").strip()    # Solicita el ID del mecánico deseado
    if mec == "0": return
    
    if mec not in datos["mecanicos"]: return print("Error: Mecánico no existe.")   # Verifica que el mecánico ingresado exista realmente en el sistema

   
    datos["ordenes"][num]["mecanico_id"] = mec    # Asigna el ID del mecánico a la orden
    
    guardar_datos(datos)  # Guarda los datos actualizados utilizando la función importada
    print("✔ Mecánico asignado.")


def agregar_servicio_orden(datos):  # Función para agregar un servicio de reparación o mantenimiento a una orden
    print("\n--- AGREGAR SERVICIO A ORDEN (Escriba 0 para regresar) ---")
    num = input("Número de Orden: ").strip()
    if num == "0": return
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")

    
    print("Servicios disponibles:")  # Muestra los servicios disponibles registrados en el sistema
    for s in datos["servicios"].keys(): print(f" - {s}")
    
    cod = input("Código del Servicio: ").strip().upper()   # Pide el código del servicio y lo convierte a mayúsculas (.upper)
    if cod == "0": return
    
    if cod not in datos["servicios"]: return print("Error: Servicio no existe.")  # Verifica que el código de servicio sea válido

    
    if cod not in datos["ordenes"][num]["servicios"]:   # Comprueba que el servicio no esté ya registrado dentro de esa misma orden
        
        datos["ordenes"][num]["servicios"].append(cod)    # Agrega (append) el servicio a la lista de servicios de la orden
        guardar_datos(datos)
        print("✔ Servicio agregado a la orden.")


def agregar_repuesto_orden(datos):   # Función para añadir repuestos a una orden y descontarlos del inventario
    print("\n--- AGREGAR REPUESTO A ORDEN (Escriba 0 para regresar) ---")
    num = input("Número de Orden: ").strip()
    if num == "0": return
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")

    
    print("Repuestos disponibles:")     # Muestra los repuestos disponibles en la base de datos
    for r in datos["repuestos"].keys(): print(f" - {r}")
    cod = input("Código del Repuesto: ").strip().upper()
    if cod == "0": return
    if cod not in datos["repuestos"]: return print("Error: Repuesto no existe.")
    
    
    try:   # Manejo de errores (try/except) para asegurar que el usuario ingrese un número entero en la cantidad
        cant = int(input("Cantidad: "))
    except ValueError:
        return print("Error: Cantidad inválida.")

    
    if datos["repuestos"][cod]["stock"] < cant:   # Verifica si la cantidad solicitada es mayor al inventario (stock) disponible
        return print("Error: Stock insuficiente.")

    
    datos["repuestos"][cod]["stock"] -= cant   # Resta la cantidad solicitada del stock total del inventario
    encontrado = False
    
    for item in datos["ordenes"][num]["repuestos"]:   #Recorre la lista de repuestos de la orden para ver si este repuesto ya había sido agregado antes
        if item["codigo_repuesto"] == cod:
           
            item["cantidad"] += cant    # Si ya estaba, simplemente le suma la nueva cantidad
            encontrado = True
            break
    
    if not encontrado:   # Si el repuesto no estaba previamente en la orden, lo agrega como un diccionario nuevo
        datos["ordenes"][num]["repuestos"].append({"codigo_repuesto": cod, "cantidad": cant})
    
    guardar_datos(datos)   # Guarda los cambios de la orden y la reducción del stock
    print("✔ Repuesto agregado y stock actualizado.")


def actualizar_estado_reparacion(datos):   # Función para cambiar la etapa de progreso de una orden
    print("\n--- ACTUALIZAR ESTADO DE ORDEN (Escriba 0 para regresar) ---")
    num = input("Número de Orden: ").strip()
    if num == "0": return
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")

    
    print(f"Estados válidos: {ESTADOS}") # Muestra al usuario cuáles son las únicas opciones válidas de estado
    estado = input("Nuevo estado: ").strip()
    if estado == "0": return
    
    if estado not in ESTADOS: return print("Error: Estado inválido.") # Valida que el estado ingresado coincida exactamente con uno de los elementos de la lista 'ESTADOS'

    
    datos["ordenes"][num]["estado"] = estado   # Actualiza el valor del estado en la orden
    guardar_datos(datos)
    print("✔ Estado actualizado.")