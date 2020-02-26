print("------------------------------------------------------------")
print("                        PROBLEMA 2                          ")
print("                   CALCULADOR DE GASOLINA                   ")
print("------------------------------------------------------------ \n")

capacidad = int(input("     Ingrese cuantos galones de combustible le caben al automovil:\n         "))
porcentaje = input("     Ingrese en porcentaje la indicación del medidor del tanque de gasolina:\n      (Completo, 3/4, 1/2, 1/4)\n          ")
millasxgalon = int(input("     Ingrese cuantas millas por galon tiene su auto:\n            "))

if porcentaje == "Completo":
    porcentaje2 = .100
elif porcentaje == "3/4":
    porcentaje2 = .75
elif porcentaje == "1/2":
    porcentaje2 = .50
elif porcentaje == "1/4":
    porcentaje2 = .25




millasquealcanza = float(capacidad*porcentaje2*millasxgalon)

print("Usted puede recorrer ",millasquealcanza," millas.")

if millasquealcanza < 200:
    print("Consigue Gasolina!")
else:
    print("Seguro Proceder")