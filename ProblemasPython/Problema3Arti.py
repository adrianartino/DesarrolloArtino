print("------------------------------------------------------------")
print("                        PROBLEMA 3                          ")
print("                 Que carne magra es mejor?                  ")
print("------------------------------------------------------------\n")
print("")

precioA = float(input("   Ingrese el precio por libra del paquete A:\n        "))
porA = float(input("   Ingrese el porcentaje magro del paquete A:\n        "))

precioB = float(input("\n   Ingrese el precio por libra del paquete B:\n        "))
porB = float(input("   Ingrese el porcentaje magro del paquete B:\n        "))

floatporA = float(porA/100)
floatporB = float(porB/100)

costoA = precioA/floatporA
costoB = precioB/floatporB

print("-------------------------------------------------------------\n")
print("El costo por libra del paquete A es de: ",costoA," pesos.")
print("El costo por libra del paquete B es de: ",costoB," pesos.")

if costoA > costoB:
    print("El paquete B es mejor")
else:
    print("El paquete A es mejor")
