import json
import os
import math
from datetime import datetime

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taller_datos.json")
IMPUESTO = 0.12
ESTADOS = ["Recibida", "En diagnóstico", "En reparación", "Finalizada", "Entregada"]


def pedir(mensaje):
    while not (v := input(mensaje).strip()):
        print("Este campo no puede quedar vacío.")
    return v


def pedir_numero(mensaje, cero=True):
    while True:
        try:
            v = float(input(mensaje).replace(",", "."))
            if math.isfinite(v) and v >= 0 and (v > 0 or cero):
                return round(v, 2)
        except ValueError:
            pass
        print("Ingresa un número válido.")


class Orden:
    def __init__(self, id_orden, placa):
        self.id = id_orden
        self.placa = placa
        self.servicios, self.repuestos = [], []
        self.estado, self.pagado, self.total = ESTADOS[0], False, 0.0
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calcular(self):
        sub = sum(s["costo"] for s in self.servicios) + \
              sum(r["precio"] * r["cantidad"] for r in self.repuestos)
        self.total = round(sub * (1 + IMPUESTO), 2)
        return sub, self.total

    def pagar(self, monto):
        if self.pagado:
            raise ValueError("Esta orden ya está pagada.")
        _, total = self.calcular()
        if monto < total:
            raise ValueError(f"Pago insuficiente. Total: Q{total:.2f}.")
        self.pagado = True
        return round(monto - total, 2)

    def cambiar_estado(self, nuevo):
        if nuevo not in ESTADOS:
            raise ValueError("Estado inválido.")
        self.estado = nuevo

    def to_dict(self):
        return {"id": self.id, "placa": self.placa, "servicios": self.servicios,
                "repuestos": self.repuestos, "estado": self.estado,
                "pagado": self.pagado, "total": self.total, "fecha": self.fecha}


class Taller:
    def __init__(self):
        self.vehiculos, self.ordenes = {}, {}
        if os.path.exists(ARCHIVO):
            try:
                d = json.load(open(ARCHIVO, encoding="utf-8"))
                self.vehiculos = {v: [] for v in d.get("vehiculos", [])}
                for o in d.get("ordenes", []):
                    orden = Orden(o["id"], o["placa"])
                    orden.servicios, orden.repuestos = o["servicios"], o["repuestos"]
                    orden.estado = o["estado"] if o["estado"] in ESTADOS else ESTADOS[0]
                    orden.pagado, orden.total = o["pagado"], o["total"]
                    orden.fecha = o["fecha"]
                    self.ordenes[orden.id] = orden
                    self.vehiculos.setdefault(orden.placa, []).append(orden)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Advertencia al cargar datos: {e}")

    def guardar(self):
        d = {"vehiculos": list(self.vehiculos),
             "ordenes": [o.to_dict() for o in self.ordenes.values()]}
        tmp = ARCHIVO + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        os.replace(tmp, ARCHIVO)

    def registrar_vehiculo(self, placa):
        placa = placa.strip().upper()
        if placa in self.vehiculos:
            raise ValueError("Ese vehículo ya está registrado.")
        self.vehiculos[placa] = []
        self.guardar()

    def crear_orden(self, placa):
        placa = placa.strip().upper()
        if placa not in self.vehiculos:
            raise ValueError("No existe un vehículo con esa placa.")
        numero = len(self.ordenes) + 1
        while f"OT-{numero:04d}" in self.ordenes:
            numero += 1
        orden = Orden(f"OT-{numero:04d}", placa)
        self.ordenes[orden.id] = orden
        self.vehiculos[placa].append(orden)
        self.guardar()
        return orden

    def buscar(self, id_orden):
        orden = self.ordenes.get(id_orden.strip().upper())
        if not orden:
            print("No se encontró esa orden.")
        return orden


def mostrar(orden):
    sub, total = orden.calcular()
    print(f"\n{'='*44}\nOrden: {orden.id} | Placa: {orden.placa} | {orden.fecha}")
    print(f"Estado: {orden.estado} | Pagada: {'Sí' if orden.pagado else 'No'}\n{'-'*44}")
    print("Servicios:", *(f"  - {s['nombre']}: Q{s['costo']:.2f}" for s in orden.servicios), sep="\n")
    print("Repuestos:", *(f"  - {r['nombre']} x{r['cantidad']}: Q{r['precio']*r['cantidad']:.2f}"
                          for r in orden.repuestos), sep="\n")
    print(f"{'-'*44}\nSubtotal: Q{sub:.2f} | Impuesto: Q{sub*IMPUESTO:.2f} | TOTAL: Q{total:.2f}\n{'='*44}")


def ejecutar():
    t = Taller()
    while True:
        print("""
1.Registrar vehículo  2.Crear orden  3.Agregar servicio  4.Agregar repuesto
5.Cambiar estado      6.Ver costo    7.Registrar pago    8.Historial vehículo
9.Ver todas          10.Ver vehículos 0.Salir""")
        op = input("Opción: ").strip()
        try:
            if op == "0":
                t.guardar(); print("¡Hasta pronto!"); break
            elif op == "1":
                t.registrar_vehiculo(pedir("Placa: ")); print("Vehículo registrado.")
            elif op == "2":
                print(f"Orden creada: {t.crear_orden(pedir('Placa: ')).id}")
            elif op == "3":
                o = t.buscar(pedir("N° orden: "))
                if o and not o.pagado:
                    o.servicios.append({"nombre": pedir("Servicio: "),
                                        "costo": pedir_numero("Costo (Q): ")})
                    t.guardar(); print("Servicio agregado.")
            elif op == "4":
                o = t.buscar(pedir("N° orden: "))
                if o and not o.pagado:
                    o.repuestos.append({"nombre": pedir("Repuesto: "),
                                        "precio": pedir_numero("Precio (Q): "),
                                        "cantidad": int(pedir_numero("Cantidad: ")) or 1})
                    t.guardar(); print("Repuesto agregado.")
            elif op == "5":
                o = t.buscar(pedir("N° orden: "))
                if o:
                    print("\n".join(f"{i}.{e}" for i, e in enumerate(ESTADOS, 1)))
                    o.cambiar_estado(ESTADOS[int(pedir("Estado: ")) - 1])
                    t.guardar(); print(f"Estado: {o.estado}")
            elif op == "6":
                o = t.buscar(pedir("N° orden: "))
                if o: mostrar(o)
            elif op == "7":
                o = t.buscar(pedir("N° orden: "))
                if o:
                    mostrar(o)
                    print(f"Cambio: Q{o.pagar(pedir_numero('Monto recibido (Q): ')):.2f}")
                    t.guardar()
            elif op == "8":
                placa = pedir("Placa: ").strip().upper()
                if placa not in t.vehiculos:
                    raise ValueError("Vehículo no encontrado.")
                if not t.vehiculos[placa]:
                    print("Sin órdenes registradas.")
                for o in t.vehiculos[placa]:
                    mostrar(o)
            elif op == "9":
                for o in t.ordenes.values(): mostrar(o)
            elif op == "10":
                for p, os_ in t.vehiculos.items(): print(f"- {p} | Órdenes: {len(os_)}")
            else:
                print("Opción inválida.")
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    ejecutar()