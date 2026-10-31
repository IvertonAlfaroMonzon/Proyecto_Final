from Iverton_Clientes import guardar_datos    

def calcular_costos(datos, numero):     #Esta funcion calcula el costo total de una orden de trabajo.
    if str(numero) not in datos["ordenes"]: return None      #Verificamos que el numero de orden exista antes de continuar.
    orden = datos["ordenes"][str(numero)]      #Obtenemos los datos correspondientes a la orden solicitada.
    subtotal_servicios = sum(datos["servicios"][c]["mano_obra"] + datos["servicios"][c]["precio"] for c in orden["servicios"] if c in datos["servicios"])       #Sumamos la mano de obra y el precio de cada servicio registrado.
    subtotal_repuestos = sum(datos["repuestos"][r["codigo_repuesto"]]["precio"] * r["cantidad"] for r in orden["repuestos"] if r["codigo_repuesto"] in datos["repuestos"])       #Calculamos el costo de los repuestos segun su precio y cantidad.
    subtotal = subtotal_servicios + subtotal_repuestos      #Unimos los subtotales para obtener el costo antes de impuestos.
    impuesto = subtotal * 0.13    #Aplicamos el impuesto del 13 por ciento al subtotal.
    return subtotal + impuesto         #Devolvemos el total final que debe pagar el cliente.

def registrar_pago(datos):      #Esta funcion permite registrar un pago para una orden existente.
    print("\n--- REGISTRAR PAGO (Escriba 0 para regresar) ---")    #Primero revisamos si hay algun registro de pago 
    num = input("Número de Orden: ").strip()
    if num == "0": return
    if num not in datos["ordenes"]: return print("Error: Orden no encontrada.")        

    total = calcular_costos(datos, num)
    if total is None: return print("Error al calcular costos.")
    
    pagado = sum(p["monto"] for p in datos["ordenes"][num]["pagos"])
    saldo = total - pagado     #Calculamos cuanto ha pagado el cliente y cuanto queda pendiente.
    print(f"Total: ${total:.2f} | Pagado: ${pagado:.2f} | Saldo: ${saldo:.2f}")

    try:
        monto = float(input("Monto a pagar: "))
    except ValueError:
        return print("Error: Monto inválido.")

    if monto <= 0 or monto > saldo + 0.01:      #Validamos que el monto sea positivo y no supere el saldo pendiente.
        return print("Error: Monto inválido o excede el saldo.")      #Solicitamos el monto que el cliente desea abonar.

    metodo = input("Método (Efectivo/Tarjeta): ").strip()          #aca nos muestra que metodo de pago deseamos cancelar por el servicio
    if metodo == "0": return

    datos["ordenes"][num]["pagos"].append({"monto": monto, "metodo": metodo, "fecha": "2024"})      #Guardamos los datos del pago y actualizamos el archivo de información.
    guardar_datos(datos)
    print("✔ Pago registrado exitosamente.")        #en cuarto punto nos muestra que su pago fue exitoso

def consultar_historial(datos):       #Esta funcion muestra las ordenes y los pagos asociados a una placa.
    print("\n--- HISTORIAL DE VEHÍCULO (Escriba 0 para regresar) ---")    #Aca mostramos cuantos vehiculos 
    placa = input("Ingrese la Placa: ").strip().upper()
    if placa == "0": return
    if placa not in datos["vehiculos"]: return print("Error: Vehículo no encontrado.")      #aca nos muestra que no fue encontrado este el vehiculo del cliente

    print(f"\n--- Historial de {placa} ---")     
    encontrado = False
    for num, o in datos["ordenes"].items():
        if o["placa"] == placa:
            encontrado = True
            total = calcular_costos(datos, num) or 0
            pagado = sum(p["monto"] for p in o["pagos"])
            print(f"Orden #{num} | Estado: {o['estado']} | Total: ${total:.2f} | Pagado: ${pagado:.2f}")
    if not encontrado:
        print("No hay órdenes para este vehículo.")       