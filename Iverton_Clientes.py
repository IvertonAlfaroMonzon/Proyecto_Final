import json   #nos servira para guardar todos los datos si cerramos el sistema y lo volvemos a abrir, en una lista generada dentro del json
import os     #permitira interactuar directamente con el sistema operativo despues
import sys    #servira para interactuar con la interpretacion de python mas tarde para detectar el ejecutable (.exe)  :v

if getattr(sys, 'frozen', False): # Verificamos si el programa se está ejecutando como un archivo .exe empaquetado
    CARPETA_BASE = os.path.dirname(sys.executable)     # Si es un .exe, obtenemos la carpeta donde está guardado el ejecutable
else:
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))  # Si se esta ejecutando el código normal en VS Code, usamos la carpeta del script

ARCHIVO_DATOS = os.path.join(CARPETA_BASE, "taller_datos.json") # Unimos la ruta de la carpeta con el nombre del archivo, para que se guarde siempre ahí

def cargar_datos():  # Creamos la estructura básica que debe tener nuestra base de datos si está vacía o es nueva
    datos_vacios = {"clientes": {}, "vehiculos": {}, "mecanicos": {}, "servicios": {}, "repuestos": {}, "ordenes": {}, "contador": 1}
    if not os.path.exists(ARCHIVO_DATOS):   # Revisamos si el archivo JSON realmente existe en la computadora
        return datos_vacios  # Si no existe, por ejemplo, la primera vez que se abre el programa, devolvemos la estructura vacía
    try:     # Si el archivo existe, lo abrimos en modo lectura ("r") y con codificación UTF-8 para que acepte la "ñ" y tildes
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:    # Convertimos el texto del archivo JSON en un diccionario de Python
            datos = json.load(f)   
            for clave in datos_vacios.keys():  #hacemos una revisión extra, si por alguna razon al archivo le falta una parte, la creamos vacia
                if clave not in datos:
                    datos[clave] = datos_vacios[clave]
            return datos   # Devolvemos los datos listos para que el programa los use
    except:
        return datos_vacios   # Si el archivo se daño, con esto evitamos que el programa explote, y devolvemos los datos vacíos

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:   # Abrimos el archivo JSON en modo escritura ("w") para actualizar la información
        json.dump(datos, f, indent=4, ensure_ascii=False)  # Guardamos el diccionario convirtiéndolo a texto JSON. 
                            # indent=4 hace que el archivo sea legible y ensure_ascii=False permite guardar tildes y la "ñ"
def listar_clientes(datos):
    print("\n--- LISTA DE CLIENTES ---")
    if not datos["clientes"]:
        print("No hay clientes registrados.")    # Verificamos si el diccionario de clientes está vacío
        return
    for c in datos["clientes"].values():   # Recorremos solo los valores (la información) de cada cliente registrado
        print(f"ID: {c['id_cliente']} | Nombre: {c['nombre']} | Teléfono: {c['telefono']} | Email: {c['email']}")

def listar_vehiculos(datos):
    print("\n--- LISTA DE VEHÍCULOS ---")
    if not datos["vehiculos"]:
        print("No hay vehículos registrados.")  # Verificamos si hay vehículos en el archivo de datos(o sea, en el JSON)
        return
    for v in datos["vehiculos"].values():  #Aqui hay dos casos, antes el archivo fue creado con "anios" en vez de años por tema de programacion, pero lo cambie xD
        año_vehiculo = v.get("año", v.get("anio", "Desconocido")) #si no existe (porque es un registro viejo), busca "anio". Si no encuentra ninguna, dice "Desconocido"
        
        print(f"Placa: {v['placa']} | {v['marca']} {v['modelo']} ({año_vehiculo}) | Dueño ID: {v['id_cliente']}")
        #Se muestran todos los datos en pantalla
def listar_mecanicos(datos):
    print("\n--- LISTA DE MECÁNICOS ---")  #revisa la lista de mecanicos para ver si esta vacia o no
    if not datos["mecanicos"]:
        print("No hay mecánicos registrados.")
        return
    for m in datos["mecanicos"].values(): #recorremos los datos de cada mecanico y los mostramos en pantalla
        print(f"ID: {m['id_mecanico']} | Nombre: {m['nombre']} | Especialidad: {m['especialidad']}")

def registrar_cliente(datos):
    print("\n--- REGISTRAR CLIENTE (Escriba 0 para regresar) ---")  
    id_c = input("ID del Cliente: ").strip()   # Pedimos el ID. Usamos .strip() por si el usuario escribe espacios en blanco sin querer
    if id_c == "0": return  # Si el usuario escribe "0", salimos de la funcion y volvemos al menu
    if not id_c: return print("Error: El ID es obligatorio.")   # validacion: el ID no puede estar vacio
    if id_c in datos["clientes"]: return print("Error: Ya existe un cliente con ese ID.")  #validacion 2: no podemos tener dos clientes con el mismo ID
    
    nombre = input("Nombre: ").strip()#pide el resto de datos uno por uno
    if nombre == "0": return
    telefono = input("Teléfono: ").strip()
    if telefono == "0": return
    email = input("Email: ").strip()
    if email == "0": return
    direccion = input("Dirección: ").strip()
    if direccion == "0": return  # guardamos toda la informacion del cliente en el diccionario principal

    datos["clientes"][id_c] = {  
        "id_cliente": id_c, "nombre": nombre, "telefono": telefono,
        "email": email, "direccion": direccion, "vehiculos": []
    }
    guardar_datos(datos)   # llamamos a la funcion para que se escriba en el archivo json
    print("✔ Cliente registrado exitosamente.") #mensaje para indicar que si funciono xD

def registrar_vehiculo(datos):
    print("\n--- REGISTRAR VEHÍCULO (Escriba 0 para regresar) ---")
    placa = input("Placa: ").strip().upper()  # pedimos la placa y la convertimos a mayusculas para mantener un formato unico
    if placa == "0": return   # validamos que la placa no este vacia
    if not placa: return print("Error: La placa es obligatoria.")
    if placa in datos["vehiculos"]: return print("Error: Ya existe un vehículo con esa placa.")   # revisamos que no exista otro vehiculo con la misma placa
    
    marca = input("Marca: ").strip()  
    if marca == "0": return
    modelo = input("Modelo: ").strip()
    if modelo == "0": return
    año = input("Año: ").strip()   #se pide el resto de los datos del vehiculo
    if año == "0": return
    color = input("Color: ").strip()
    if color == "0": return
    id_cliente = input("ID del Cliente dueño: ").strip()# pedimos el id del dueño para poder asociarlo
    if id_cliente == "0": return

    if id_cliente not in datos["clientes"]:  # verificamos que el cliente exista antes de guardar el vehiculo
        return print("Error: El cliente no existe. Regístrelo primero.")

    datos["vehiculos"][placa] = {  # guardamos los datos del vehiculo en el diccionario principal
        "placa": placa, "marca": marca, "modelo": modelo,
        "año": año, "color": color, "id_cliente": id_cliente
    }
    if id_cliente in datos["clientes"]:    # agregamos la placa a la lista de vehiculos del cliente dueño
        datos["clientes"][id_cliente]["vehiculos"].append(placa)
    guardar_datos(datos)     # guardamos todo en el archivo json(nuestro archivo de datos)
    print("✔ Vehículo registrado exitosamente.")

def registrar_mecanico(datos):
    print("\n--- REGISTRAR MECÁNICO (Escriba 0 para regresar) ---")
    id_m = input("ID del Mecánico: ").strip()  # pedimos el id del mecanico
    if id_m == "0": return  # validamos que el id no este vacio
    if not id_m: return print("Error: El ID es obligatorio.")
    if id_m in datos["mecanicos"]: return print("Error: Ya existe un mecánico con ese ID.")  #revisamos que no exista otro mecanico con el mismo id
    
    nombre = input("Nombre: ").strip()
    if nombre == "0": return
    especialidad = input("Especialidad: ").strip()  #pedimos los demas datos del mecanico
    if especialidad == "0": return
    telefono = input("Teléfono: ").strip()
    if telefono == "0": return

    datos["mecanicos"][id_m] = {
        "id_mecanico": id_m, "nombre": nombre,  # guardamos la informacion en el diccionario principal
        "especialidad": especialidad, "telefono": telefono
    }
    guardar_datos(datos)  # actualizamos el archivo json
    print("✔ Mecánico registrado exitosamente.")