import os
import Iverton_Clientes
import Ordenes_Daniel
import Marlon_Estados                #importamos todos los archivos complementos que sirven para la ejecucion del sistema
import Valeri_Costos

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')      #se encarga de limpiar la pantalla cada vez que se llama a la funcion

def mostrar_presentacion():
    limpiar_pantalla()
    print("="*60)
    print("      SISTEMA DE ADMINISTRACIÓN DE TALLER AUTOMOTRIZ")
    print("                 Ctrl Z Corporation")
    print("="*60)
    print("\nIntegrantes del Proyecto:")
    print(" - Iverton Ivan Alfaro Monzon")
    print(" - Daniel Alejandro Tema Lopez") 
    print(" - Marlon Alberto TigÜilá castro")             #primer pantalla que muestra la informacion de los integrantes
    print(" - Valerí Hoxame De leon De leon")
    print("\n" + "="*60)
    print("1. Continuar al Sistema")
    print("2. Salir")
    
    opcion = input("\nSeleccione una opción: ").strip() # pedimos al usuario que elija una opcion y quitamos los espacios en blanco
    if opcion == "1":
        return True   # si elige 1 devolvemos verdadero para que el programa principal arranque
    elif opcion == "2":
        print("Saliendo del sistema... ¡Hasta luego!")  # si elige 2 mostramos un mensaje de despedida y devolvemos falso para que no arranque
        return False
    else:
        print("Opción inválida.")   # si escribe cualquier otra cosa, avisamos del error y volvemos a llamar a la funcion
        input("Presione Enter para intentar de nuevo...")
        return mostrar_presentacion()

def menu_principal(datos):
    while True:     # usamos un bucle infinito para que el menu se muestre una y otra vez hasta que el usuario decida salir
        limpiar_pantalla()
        print("="*50)
        print("          MENÚ PRINCIPAL - TALLER AUTOMOTRIZ")
        print("="*50)
        print("1. Gestión de Clientes y Vehículos")
        print("2. Gestión de Servicios y Repuestos")
        print("3. Gestión de Órdenes de Trabajo")
        print("4. Registrar Pagos")
        print("5. Consultar Historial de Vehículo")
        print("6. Guardar Datos Manualmente")
        print("7. Salir del Sistema")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-7): ").strip()  # pedimos la opcion al usuario
        
        if opcion == "1":   # dependiendo de lo que escriba, llamamos a la funcion correspondiente
            menu_clientes(datos)
        elif opcion == "2":
            menu_servicios(datos)
        elif opcion == "3":
            menu_ordenes(datos)
        elif opcion == "4":
            Valeri_Costos.registrar_pago(datos)   # llamamos a la funcion de pagos del archivo de valeri
            input("\nPresione Enter para continuar...")   # hacemos una pausa para que el usuario pueda leer el resultado antes de limpiar la pantalla
        elif opcion == "5":   
            Valeri_Costos.consultar_historial(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "6":   # guardamos manualmente los datos en el json
            Iverton_Clientes.guardar_datos(datos)
            print("✔ Datos guardados.")   
            input("\nPresione Enter para continuar...")
        elif opcion == "7":
            print("Saliendo del sistema... ¡Hasta luego!")# si elige 7 rompemos el bucle y salimos del sistema
            break
        else:
            print("Opción inválida.")   # si escribe una opcion que no existe, avisamos del error
            input("Presione Enter para intentar de nuevo...")

def menu_clientes(datos):
    while True: # bucle para mostrar el menu hasta que el usuario decida regresar
        limpiar_pantalla()
        print("--- GESTIÓN DE CLIENTES Y VEHÍCULOS ---")
        print("1. Registrar Cliente")
        print("2. Registrar Vehículo")
        print("3. Registrar Mecánico")
        print("4. Ver lista de Clientes")
        print("5. Ver lista de Vehículos")
        print("6. Ver lista de Mecánicos")
        print("0. Regresar al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ").strip()  # pedimos la opcion al usuario
        if opcion == "1":
            Iverton_Clientes.registrar_cliente(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            Iverton_Clientes.registrar_vehiculo(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            Iverton_Clientes.registrar_mecanico(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            Iverton_Clientes.listar_clientes(datos)
            input("\nPresione Enter para continuar...")  # evaluamos la opcion y llamamos a las funciones del archivo de iverton_clientes
        elif opcion == "5":
            Iverton_Clientes.listar_vehiculos(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "6":
            Iverton_Clientes.listar_mecanicos(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":  # si elige 0 rompemos el bucle y regresamos al menu principal
            break
        else:
            print("Opción inválida.")   # si la opcion no es valida mostramos error
            input("Presione Enter para intentar de nuevo...")

def menu_servicios(datos):
    while True:   #mismo bucle para que muestre las opciones hasta que el usuario decida regresar
        limpiar_pantalla()
        print("--- GESTIÓN DE SERVICIOS Y REPUESTOS ---")
        print("1. Registrar Servicio")
        print("2. Registrar Repuesto")
        print("3. Ver lista de Servicios")
        print("4. Ver lista de Repuestos")
        print("0. Regresar al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ").strip()  # pedimos la opcion al usuario otra vez
        if opcion == "1":
            Ordenes_Daniel.registrar_servicio(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            Ordenes_Daniel.registrar_repuesto(datos)
            input("\nPresione Enter para continuar...")  # evaluamos la opcion y llamamos a las funciones del archivo de daniel
        elif opcion == "3":
            Ordenes_Daniel.listar_servicios(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            Ordenes_Daniel.listar_repuestos(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":  # si elige 0 rompemos el bucle y volvemos al menu principal
            break
        else:   
            print("Opción inválida.")   # si la opcion no existe, mostramos un aviso de error
            input("Presione Enter para intentar de nuevo...")

def menu_ordenes(datos):
    while True:   #mismo bucle que sirve para mantener el menu abierto hasta que el usuario quiera regresar
        limpiar_pantalla()
        print("--- GESTIÓN DE ÓRDENES DE TRABAJO ---")
        print("1. Crear Orden")
        print("2. Asignar Mecánico a Orden")
        print("3. Agregar Servicio a Orden")
        print("4. Agregar Repuesto a Orden")
        print("5. Cambiar Estado de Orden")
        print("6. Ver lista de Órdenes")
        print("7. Ver detalle de una Orden")
        print("0. Regresar al Menú Principal")
        
        opcion = input("\nSeleccione una opción: ").strip()  #pedimos la opcion al usuario de nuevo
        if opcion == "1":
            Ordenes_Daniel.crear_orden(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            Marlon_Estados.asignar_mecanico_orden(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            Marlon_Estados.agregar_servicio_orden(datos)  #se evalua la opcion y se muestra el menu que corresponde al archivo de Marlon
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            Marlon_Estados.agregar_repuesto_orden(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "5":
            Marlon_Estados.actualizar_estado_reparacion(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "6":
            Ordenes_Daniel.listar_ordenes(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "7":
            Marlon_Estados.ver_detalle_orden(datos)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":   #si vuelve a elegir 0, se rompe el bucle y regresa al menu principal
            break
        else:
            print("Opción inválida.")# si la opcion no existe, se muestra un aviso de error
            input("Presione Enter para intentar de nuevo...")

if __name__ == "__main__":  # esta linea comprueba que el archivo se este ejecutando directamente y no siendo importado
    if mostrar_presentacion():   # llamamos a la pantalla de inicio para ver si el usuario quiere continuar
        datos_globales = Iverton_Clientes.cargar_datos()   # si el usuario presiona 1, cargamos los datos guardados en el archivo json
        menu_principal(datos_globales)  # arrancamos el menu principal pasandole los datos para que el sistema empiece a funcionar