import datetime

Servicios = {
    1: {"nombre": "Afinacion menor", "precio": 1500},
    2: {"nombre": "Afinacion Mayor", "precio": 3000},
    3: {"nombre": "Ajuste de Afinacion", "precio": 2500},
    4: {"nombre": "Cambio de Aceite", "precio": 500},
    5: {"nombre": "Alineacion y balanceo de ruedas", "precio": 850},
    6: {"nombre": "Enderezado", "precio": 300},
    7: {"nombre": "Pulidor de rayadura", "precio": 400},
    8: {"nombre": "Cambio de piezas", "precio": 450},
    9: {"nombre": "Sustitucion de vidrios rotos", "precio": 600},
    10: {"nombre": "Polarizacion", "precio": 1200}
}
notas = {}
notas_canceladas = set()

while True:
    print("Menu:")
    print("1. Ingresar nueva nota")
    print("2. Consultas y Reportes")
    print("3. Cancelar una nota")
    print("4. Recuperar una nota")
    print("5. Salir")
    
    opcion = input("Seleccione una opción (1/2/3/4/5): ").strip()

    if opcion == "1":
        Nombre_Cliente = input("Introducir el nombre completo del Cliente: ")
        if not Nombre_Cliente.strip():
            break

        fecha_nota = input("Dame la fecha en este formato: dd/mm/aaaa: ")
        try:
            fecha_procesada = datetime.datetime.strptime(fecha_nota, '%d/%m/%Y').date()
        except ValueError:
            print("Formato de fecha incorrecto. Introduce la fecha en el formato dd/mm/aaaa.")
            continue

        while True:
            ServicioR = input("Selecciona el servicio que podremos ofrecerle (1-10): ")
            if ServicioR.isdigit():
                ServicioR = int(ServicioR)
                if ServicioR in Servicios:
                    servicio_elegido = Servicios[ServicioR]
                    print(f"Ha seleccionado el servicio: {servicio_elegido['nombre']}")
                    print(f"Precio: ${servicio_elegido['precio']}")
                    break
                else:
                    print("Servicio no válido. Por favor, elija un número del 1 al 10.")
            else:
                print("Entrada no válida. Por favor, ingrese un número del 1 al 10.")

        nueva_clave = max(notas.keys(), default=0) + 1
        notas[nueva_clave] = (Nombre_Cliente, fecha_procesada, ServicioR)

    elif opcion == "2":
        while True:
            print("\nSubmenu - Consultas y Reportes:")
            print("1. Consultar nota por folio")
            print("2. Consultar Nota por Periodo de Fecha")
            print("3. Regresar al menú principal")
            
            opcion_consultas = input("Seleccione una opción (1/2/3): ").strip()

            if opcion_consultas == "1":
                folio = input("Ingrese el folio de la nota a consultar (Son numero enteros y empieza desde el Num.1): ")
                if folio.isdigit():
                    folio = int(folio)
                    if folio in notas and folio not in notas_canceladas:
                        nombre, fecha, servicio, nombre_servicio, precio_servicio = notas[folio]
                        print(f"Datos de la nota {folio}:")
                        print(f"Nombre del cliente: {nombre}")
                        print(f"Fecha: {fecha}")
                        print(f"Servicio: {nombre_servicio} ")
                        print(f"Precio del servicio: ${precio_servicio}")
                    else:
                        print("La nota no existe o está cancelada.")
                else:
                    print("Entrada no válida. El folio debe ser un número entero.")

            elif opcion_consultas == "2":
                fecha_inicio = input("Ingrese la fecha de inicio en formato dd/mm/aaaa: ")
                fecha_fin = input("Ingrese la fecha de fin en formato dd/mm/aaaa: ")
                try:
                    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y').date()
                    fecha_fin = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y').date()
                except ValueError:
                    print("Formato de fecha incorrecto. Introduce las fechas en el formato dd/mm/aaaa.")
                    continue
                notas_en_periodo = []
                for folio, (nombre, fecha, _, _, _) in notas.items():
                    if fecha_inicio <= fecha <= fecha_fin:
                        notas_en_periodo.append((folio, nombre, fecha))
                if notas_en_periodo:
                    print("\nNotas en el período especificado:")
                    print("Folio", "Nombre Cliente", "Fecha")
                    for folio, nombre, fecha in notas_en_periodo:
                        print(folio, nombre, fecha.strftime('%d/%m/%Y'))
                else:
                    print("\nNo hay notas emitidas para el período especificado.")

            elif opcion_consultas == "3":
                break
            else:
                print("Opción no válida. Seleccione 1, 2 o 3.")

    elif opcion == "3":
        folio_cancelar = input("Ingrese el folio de la nota a cancelar: ")
        if folio_cancelar.isdigit():
            folio_cancelar = int(folio_cancelar)
            if folio_cancelar in notas and folio_cancelar not in notas_canceladas:
                nombre, fecha, servicio, nombre_servicio, precio_servicio = notas[folio_cancelar]
                print(f"Datos de la nota {folio_cancelar} a cancelar:")
                print(f"Nombre del cliente: {nombre}")
                print(f"Fecha: {fecha}")
                print(f"Servicio: {nombre_servicio} ")
                print(f"Precio del servicio: ${precio_servicio}")

                confirmacion = input("¿Desea cancelar esta nota? (Sí/No): ").strip().lower()
                if confirmacion == "si":
                    notas_canceladas.add(folio_cancelar)
                    print(f"Nota {folio_cancelar} ha sido cancelada.")
                else:
                    print(f"Nota {folio_cancelar} no ha sido cancelada.")
            else:
                print("El folio no corresponde a una nota existente o ya está cancelada.")
        else:
            print("Entrada no válida. El folio debe ser un número entero.")
    elif opcion == "4":
        print("Notas actualmente canceladas:")
        notas_canceladas_tabla = [(folio, nombre) for folio, (nombre, _, _, _, _) in notas.items() if folio in notas_canceladas]
        if notas_canceladas_tabla:
            print("Folio", "Nombre Cliente")
            for folio, nombre in notas_canceladas_tabla:
                print(folio, nombre)
            
            folio_recuperar = input("Ingrese el folio de la nota que desea recuperar o 'No' para cancelar: ").strip()
            if folio_recuperar.lower() == "no":
                print("No se ha recuperado ninguna nota.")
            elif folio_recuperar.isdigit():
                folio_recuperar = int(folio_recuperar)
                if folio_recuperar in notas and folio_recuperar in notas_canceladas:
                    nombre, fecha, servicio, nombre_servicio, precio_servicio = notas[folio_recuperar]
                    print(f"Detalle de la nota {folio_recuperar} a recuperar:")
                    print(f"Nombre del cliente: {nombre}")
                    print(f"Fecha: {fecha}")
                    print(f"Servicio: {nombre_servicio} ")
                    print(f"Precio del servicio: ${precio_servicio}")

                    confirmacion = input("¿Desea recuperar esta nota? (Sí/No): ").strip().lower()
                    if confirmacion == "si":
                        notas_canceladas.remove(folio_recuperar)
                        print(f"Nota {folio_recuperar} ha sido recuperada.")
                    else:
                        print(f"Nota {folio_recuperar} no ha sido recuperada.")
                else:
                    print("El folio no corresponde a una nota cancelada.")
            else:
                print("Entrada no válida. El folio debe ser un número entero.")

    elif opcion == "5":
        confirmacion_salir = input("¿Está seguro de que desea salir? (Sí/No): ").strip().lower()
        if confirmacion_salir == "si":
            break
